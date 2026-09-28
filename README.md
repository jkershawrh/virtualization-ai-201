# Virtualization + AI 201

Build and qualify a VM-to-AI application contract on Red Hat OpenShift
Virtualization. This is a separate level-201 scope: the completed
[`virtualization-ai-foundations`](https://github.com/jkershawrh/virtualization-ai-foundations)
101 track is an upstream prerequisite, and its learner evidence is not copied or
accepted as construction work here.

The learner authors and qualifies:

- versioned request, response, evidence, and OpenAPI contracts;
- a correlation-aware client that executes inside a VirtualMachine;
- a runtime Secret reference without any Secret value in source or the guest;
- an OpenShift Service and allow-list NetworkPolicy;
- a validation adapter with `LIVE`, `REHEARSAL`, and `OFFLINE` source states;
- healthy and model-unavailable fail-closed behavior;
- a redacted evidence map, human acceptance decision, and cleanup receipt.

The model is advisory. It cannot call tools, mutate the VM or cluster, qualify
its own output, certify the lab, or approve promotion.

## Experience

- A concise seven-scene Red Hat × Intel pre-lab presentation preserves the
  Triforce cadence: tension, causal architecture, two-condition proof,
  mechanisms, evidence payoff, and one guided handoff.
- A separate 75–90 minute Showroom lab starts in `lab/starter/`; learners must
  replace intentional TODOs and run the local qualification gate.
- `docs/cdd-red-run.md` records the intentional failing test run that preceded
  the reference implementation.

## Verify

Requirements: Node.js 22+, Python 3.9+, Helm 3, and Playwright Chromium.

```sh
npm ci
python3 -m pip install --requirement requirements-test.txt
npm run check
npm run test:visual
npm audit --audit-level=high
```

## Run locally

Start the adapter in default `REHEARSAL` mode:

```sh
ADAPTER_PORT=8089 ADAPTER_MODE=rehearsal python3 -m workload.app
```

Then start the presentation:

```sh
npm run dev -- --host 127.0.0.1 --port 5173
```

The browser uses the typed adapter only when it reports qualifying `LIVE`
evidence. Otherwise it displays checked-in, visibly labeled rehearsal data.

## Deploy the reference runtime

The default chart is secret-free and uses rehearsal mode:

```sh
helm upgrade --install virtualization-ai-201 charts/virtualization-ai-201 \
  --namespace virtualization-ai-201 --create-namespace \
  --set vm.sshAuthorizedKey='ssh-ed25519 REPLACE_AT_RUNTIME'
```

For LIVE mode, an environment owner must create the runtime Secret outside
source control and supply its name plus an approved model endpoint CIDR. The
chart projects the Secret only into the adapter, never into the VM or
presentation.

## Immutable factory candidates

GitHub Actions run
[`36477467751`](https://github.com/jkershawrh/virtualization-ai-201/actions/runs/36477467751)
published exact-source, Linux/AMD64 candidates from revision
`7928d13b9b00820e81f6c96ec047e3c22ec26e3f`:

- adapter: `ghcr.io/jkershawrh/virtualization-ai-201-adapter@sha256:f17a7cc9c708e58186bd38878630dc563b853f78e1535be3435c0c8aec34eedb`
- presentation: `ghcr.io/jkershawrh/virtualization-ai-201-presentation@sha256:9f58d0a74d58201156547d21be2bc8a6b30f9d00619206dcce337d03e0ea4569`

Both candidates passed complete Grype 0.97.1 inventories with zero HIGH and
zero CRITICAL findings. The adapter inventory contains six MEDIUM findings and
the presentation inventory four. SPDX SBOMs, GitHub OIDC signatures, custom
provenance attestations, SBOM attestations, and exact-digest verification are
retained for 90 days. `charts/virtualization-ai-201/values.published.yaml`
selects only these digests.

The proposed Launchpad handoff remains non-certified, non-orderable, and capped
at zero workshop seats until its independent live gates pass.

## Evidence boundary

No factory check claims a live OpenShift journey, supported-version result,
capacity measurement, certified reclaim, Launchpad certification, orderability,
or promotion. The immutable release workflow can build, fully scan, publish,
sign, attest, and verify source-bound Linux/AMD64 candidates; Launchpad must
independently qualify them and the live environment.
