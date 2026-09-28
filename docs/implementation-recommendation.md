# Implementation recommendation

Keep this 201 track independent from the completed 101 repository. Use 101 only
to establish prerequisite vocabulary and the traced runtime boundaries.

The reference implementation deliberately separates:

- learner-authored contract artifacts under `lab/starter/`;
- reviewed reference contracts under `contracts/`;
- deterministic request, output, evidence, and authority checks in `workload/`;
- platform wiring in the Helm chart;
- short decision framing in the presentation; and
- construction depth in the Showroom lab.

Activate LIVE mode only after an environment owner supplies a supported
OpenShift Virtualization target, approved OpenAI-compatible endpoint, complete
model/provider/Intel Xeon identity, runtime Secret, and endpoint CIDR. Treat
missing identity or invalid output as unavailable. Do not add performance,
capacity, cost, or certification language until current-session evidence exists.
