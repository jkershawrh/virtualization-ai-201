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
