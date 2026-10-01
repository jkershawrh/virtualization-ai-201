#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import socket
import sys
import uuid
from datetime import datetime, timezone
from urllib.request import Request, urlopen


def build_request(note: str) -> dict:
    return {
        "schema_version": "virtualization-ai.redhat-intel.com/qualification-request/v1",
        "correlation_id": str(uuid.uuid4()),
        "guest": {
            "name": os.getenv("VM_NAME", socket.gethostname()),
            "namespace": os.getenv("VM_NAMESPACE", "virtualization-ai-201"),
        },
        "task": "classify-operations-note",
        "note": note,
        "allowed_categories": ["application", "capacity", "connectivity", "unknown"],
    }


def main() -> None:
    note = " ".join(sys.argv[1:]).strip() or "The application reaches Service DNS, then stops at the model boundary."
    payload = build_request(note)
    endpoint = os.getenv("ADAPTER_URL", "http://virtualization-ai-201-adapter:8080/api/v1/qualify")
    body = json.dumps(payload, separators=(",", ":")).encode()
    receipt = {
        "correlation_id": payload["correlation_id"],
        "guest": f'{payload["guest"]["namespace"]}/{payload["guest"]["name"]}',
        "request_sha256": hashlib.sha256(json.dumps(payload, separators=(",", ":"), sort_keys=True).encode()).hexdigest(),
        "created_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    }
    print(json.dumps({"guest_request_receipt": receipt}, indent=2), file=sys.stderr)
    request = Request(endpoint, body, {"Content-Type": "application/json"}, method="POST")
    with urlopen(request, timeout=10) as response:
        print(json.dumps(json.loads(response.read()), indent=2))


if __name__ == "__main__":
    main()
