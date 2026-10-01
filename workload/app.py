from __future__ import annotations

import hashlib
import json
import os
import threading
import uuid
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


REQUEST_VERSION = "virtualization-ai.redhat-intel.com/qualification-request/v1"
RESPONSE_VERSION = "virtualization-ai.redhat-intel.com/qualification-response/v1"
EVIDENCE_VERSION = "virtualization-ai.redhat-intel.com/evidence-record/v1"
ALLOWED_CATEGORIES = {"application", "capacity", "connectivity", "unknown"}
FORBIDDEN_KEYS = {"api_key", "apikey", "password", "secret", "token"}
EVIDENCE: dict[str, dict] = {}
EVIDENCE_LOCK = threading.Lock()


class ContractError(ValueError):
    pass


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def canonical_sha256(value: object) -> str:
    encoded = json.dumps(value, separators=(",", ":"), sort_keys=True).encode()
    return hashlib.sha256(encoded).hexdigest()


def contains_forbidden_key(value: object) -> bool:
    if isinstance(value, dict):
        return any(str(key).lower() in FORBIDDEN_KEYS or contains_forbidden_key(item) for key, item in value.items())
    if isinstance(value, list):
        return any(contains_forbidden_key(item) for item in value)
    return False


def validate_request(payload: object) -> dict:
    if not isinstance(payload, dict):
        raise ContractError("request must be a JSON object")
    expected = {"schema_version", "correlation_id", "guest", "task", "note", "allowed_categories"}
    if set(payload) != expected:
        raise ContractError("request fields do not match the v1 contract")
    if contains_forbidden_key(payload):
        raise ContractError("secret-bearing fields are forbidden")
    if payload["schema_version"] != REQUEST_VERSION or payload["task"] != "classify-operations-note":
        raise ContractError("unsupported contract version or task")
    try:
        uuid.UUID(str(payload["correlation_id"]))
    except ValueError as exc:
        raise ContractError("correlation_id must be a UUID") from exc
    guest = payload["guest"]
    if not isinstance(guest, dict) or set(guest) != {"name", "namespace"}:
        raise ContractError("guest must contain only name and namespace")
    if not all(isinstance(guest[key], str) and 0 < len(guest[key]) <= 63 for key in guest):
        raise ContractError("guest identity is invalid")
    note = payload["note"]
    if not isinstance(note, str) or not 0 < len(note) <= 1000:
        raise ContractError("note must contain 1 to 1000 characters")
    categories = payload["allowed_categories"]
    if not isinstance(categories, list) or set(categories) != ALLOWED_CATEGORIES or len(categories) != 4:
        raise ContractError("allowed_categories must contain the complete v1 enumeration")
    return payload


def configuration() -> dict[str, str]:
    return {
        "mode": os.getenv("ADAPTER_MODE", "rehearsal").lower(),
        "endpoint": os.getenv("MODEL_ENDPOINT", ""),
        "model": os.getenv("MODEL_ID", ""),
        "provider": os.getenv("MODEL_PROVIDER", ""),
        "hardware": os.getenv("MODEL_HARDWARE", ""),
        "api_key": os.getenv("MODEL_API_KEY", ""),
    }


def rehearsal_advisory(note: str) -> dict[str, str]:
    lowered = note.lower()
    if any(word in lowered for word in ("dns", "route", "connect", "service", "boundary")):
        category = "connectivity"
    elif any(word in lowered for word in ("memory", "cpu", "capacity", "quota")):
        category = "capacity"
    elif any(word in lowered for word in ("application", "process", "error")):
        category = "application"
    else:
        category = "unknown"
    return {
        "category": category,
        "summary": "Representative contract output for rehearsal; no live model participation is claimed.",
        "rationale": "The deterministic fixture demonstrates response validation and evidence correlation only.",
    }


def model_completion_url(endpoint: str) -> str:
    normalized = endpoint.rstrip("/")
    if normalized.endswith("/v1"):
        return f"{normalized}/chat/completions"
    return normalized


def call_live_model(payload: dict, config: dict[str, str]) -> dict[str, str]:
    missing = [key for key in ("endpoint", "model", "provider", "hardware", "api_key") if not config[key]]
    if missing:
        raise ContractError(f"live identity is incomplete: {', '.join(missing)}")
    prompt = {
        "task": payload["task"],
        "allowed_categories": payload["allowed_categories"],
        "note": payload["note"],
        "required_output": {"category": "enum", "summary": "string", "rationale": "string"},
    }
    body = json.dumps({
        "model": config["model"],
        "messages": [
            {"role": "system", "content": "Return one JSON object only. Do not propose or execute actions."},
            {"role": "user", "content": json.dumps(prompt, separators=(",", ":"))},
        ],
        "temperature": 0,
    }).encode()
    request = Request(
        model_completion_url(config["endpoint"]), body,
        {"Authorization": f"Bearer {config['api_key']}", "Content-Type": "application/json"},
        method="POST",
    )
    timeout_seconds = int(os.getenv("MODEL_TIMEOUT_SECONDS", "90"))
    with urlopen(request, timeout=timeout_seconds) as response:
        result = json.loads(response.read())
    content = result["choices"][0]["message"]["content"]
    advisory = json.loads(content)
    if set(advisory) != {"category", "summary", "rationale"}:
        raise ContractError("model output fields do not match the response contract")
    if advisory["category"] not in ALLOWED_CATEGORIES:
        raise ContractError("model output category is outside the allowed set")
    if not all(isinstance(advisory[key], str) and advisory[key] for key in advisory):
        raise ContractError("model output contains an empty or non-string value")
    return advisory


def unavailable_response(payload: dict, evidence_id: str, source_state: str, failure_class: str, message: str) -> dict:
    return {
        "schema_version": RESPONSE_VERSION,
        "correlation_id": payload["correlation_id"],
        "outcome": "MODEL_UNAVAILABLE",
        "source_state": source_state,
        "ai_participated": False,
        "failure": {"class": failure_class, "message": message[:240]},
        "validation": "FAIL_CLOSED",
        "authority": "HUMAN_REVIEW_REQUIRED",
        "evidence_id": evidence_id,
    }


def qualify(payload: object, condition: str = "healthy") -> tuple[dict, dict]:
    request_payload = validate_request(payload)
    evidence_id = str(uuid.uuid4())
    config = configuration()
    mode = config["mode"]
    response: dict

    if condition == "unavailable" or mode == "offline":
        response = unavailable_response(
            request_payload, evidence_id, "OFFLINE" if mode == "offline" else "REHEARSAL",
            "offline" if mode == "offline" else "connection",
            "The declared model boundary is unavailable; no advisory output was created.",
        )
    elif mode == "live":
        try:
            advisory = call_live_model(request_payload, config)
            response = {
                "schema_version": RESPONSE_VERSION,
                "correlation_id": request_payload["correlation_id"],
                "outcome": "QUALIFIED",
                "source_state": "LIVE",
                "ai_participated": True,
                "advisory": advisory,
                "model": {"id": config["model"], "provider": config["provider"], "hardware": config["hardware"]},
                "validation": "PASS",
                "authority": "HUMAN_REVIEW_REQUIRED",
                "evidence_id": evidence_id,
            }
        except ContractError as exc:
            response = unavailable_response(request_payload, evidence_id, "OFFLINE", "identity", str(exc))
        except (HTTPError, URLError, TimeoutError, KeyError, ValueError, json.JSONDecodeError) as exc:
            failure_class = "timeout" if isinstance(exc, TimeoutError) else "connection"
            response = unavailable_response(request_payload, evidence_id, "LIVE", failure_class, "The live model call failed closed.")
    else:
        response = {
            "schema_version": RESPONSE_VERSION,
            "correlation_id": request_payload["correlation_id"],
            "outcome": "QUALIFIED",
            "source_state": "REHEARSAL",
            "ai_participated": False,
            "advisory": rehearsal_advisory(request_payload["note"]),
            "model": {"id": "rehearsal-fixture", "provider": "fixture", "hardware": "not-observed"},
            "validation": "PASS",
            "authority": "HUMAN_REVIEW_REQUIRED",
            "evidence_id": evidence_id,
        }

    evidence = {
        "schema_version": EVIDENCE_VERSION,
        "evidence_id": evidence_id,
        "correlation_id": request_payload["correlation_id"],
        "guest": f'{request_payload["guest"]["namespace"]}/{request_payload["guest"]["name"]}',
        "request_sha256": canonical_sha256(request_payload),
        "service": "virtualization-ai-201-adapter:8080",
        "source_state": response["source_state"],
        "outcome": response["outcome"],
        "ai_participated": response["ai_participated"],
        "model_id": response.get("model", {}).get("id"),
        "validation": response["validation"],
        "authority": response["authority"],
        "created_at": utc_now(),
    }
    with EVIDENCE_LOCK:
        EVIDENCE[evidence_id] = evidence
    return response, evidence


class Handler(BaseHTTPRequestHandler):
    server_version = "virtualization-ai-201/1"

    def send_json(self, status: int, value: object) -> None:
        encoded = json.dumps(value, separators=(",", ":")).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def do_GET(self) -> None:  # noqa: N802
        if self.path == "/healthz":
            config = configuration()
            self.send_json(200, {
                "status": "ok", "mode": config["mode"].upper(),
                "live_identity_complete": all(config[key] for key in ("endpoint", "model", "provider", "hardware", "api_key")),
                "authority": "HUMAN_REVIEW_REQUIRED",
            })
            return
        if self.path.startswith("/api/v1/evidence/"):
            evidence_id = self.path.rsplit("/", 1)[-1]
            with EVIDENCE_LOCK:
                evidence = EVIDENCE.get(evidence_id)
            self.send_json(200 if evidence else 404, evidence or {"error": "evidence not found"})
            return
        self.send_json(404, {"error": "not found"})

    def do_POST(self) -> None:  # noqa: N802
        if self.path not in ("/api/v1/qualify", "/api/v1/qualify?condition=unavailable"):
            self.send_json(404, {"error": "not found"})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length <= 0 or length > 16384:
                raise ContractError("request body length is invalid")
            payload = json.loads(self.rfile.read(length))
            condition = "unavailable" if self.path.endswith("condition=unavailable") else self.headers.get("X-Qualification-Condition", "healthy")
            response, _ = qualify(payload, condition)
            self.send_json(200, response)
        except (ContractError, json.JSONDecodeError) as exc:
            self.send_json(400, {"error": str(exc), "validation": "REJECTED"})

    def log_message(self, format: str, *args: object) -> None:
        print(f'{self.address_string()} - {format % args}')


def main() -> None:
    port = int(os.getenv("ADAPTER_PORT", "8080"))
    ThreadingHTTPServer(("0.0.0.0", port), Handler).serve_forever()


if __name__ == "__main__":
    main()
