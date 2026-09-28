# Source-bound immutable release

`.github/workflows/release-images.yml` accepts an exact 40-character source
revision. It refuses dispatch or checkout drift, reruns the project gates, and
builds the presentation and adapter for `linux/amd64` without cache.

For each image the workflow retains a complete vulnerability inventory, blocks
every HIGH or CRITICAL finding whether fixable or not, generates an SPDX JSON
SBOM, publishes a commit-specific GHCR candidate only after the gate passes,
deletes the local tag and proves an exact-digest pull, verifies architecture and
source-revision labels, signs with GitHub OIDC, attaches SPDX and provenance
attestations, verifies the expected workflow identity, and retains evidence for
90 days. Every external GitHub Action is pinned to a full commit SHA.

`publish=false` performs validation, build, scan, and SBOM gates without
changing GHCR. Publication does not certify the lab or prove live OpenShift,
model placement, capacity, reclaim, registry approval, rollback, or promotion.

## Published candidate receipt

Run
[`36477467751`](https://github.com/jkershawrh/virtualization-ai-201/actions/runs/36477467751)
completed successfully from exact revision
`7928d13b9b00820e81f6c96ec047e3c22ec26e3f` on 2026-09-28.

| Component | Immutable digest | Complete Grype inventory | SPDX packages |
| --- | --- | --- | ---: |
| Adapter | `sha256:f17a7cc9c708e58186bd38878630dc563b853f78e1535be3435c0c8aec34eedb` | 0 CRITICAL, 0 HIGH, 6 MEDIUM | 32 |
| Presentation | `sha256:9f58d0a74d58201156547d21be2bc8a6b30f9d00619206dcce337d03e0ea4569` | 0 CRITICAL, 0 HIGH, 4 MEDIUM | 26 |

The workflow verified each exact-digest pull, source-revision label, GitHub OIDC
signature, SPDX attestation, and custom provenance attestation. The retained
factory receipts under `handoff/evidence/` bind those claims to the downloaded
workflow evidence hashes. They do not claim Launchpad certification or a live
OpenShift result.
