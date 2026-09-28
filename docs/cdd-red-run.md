# Contract-driven development RED receipt

Observed on 2026-09-28 before reference implementation work, after bootstrap
commit `ade0cde`.

Command:

```text
python3 -m unittest discover -s tests -v
```

Result: **expected failure** (`1` failing, `4` passing).

The request and both response examples already passed their JSON Schema tests.
The construction gate failed because these learner-facing implementation assets
did not yet exist:

- `workload/app.py`
- `workload/vm_client.py`
- `charts/virtualization-ai-201/templates/adapter.yaml`
- `charts/virtualization-ai-201/templates/networkpolicy.yaml`
- `showroom/content/modules/ROOT/pages/03-author.adoc`

This is the intentional CDD RED state. It proves the contract and acceptance
test existed before the implementation. Later GREEN results must satisfy this
same test; this receipt grants no deployment, certification, or promotion
authority.
