Owner: coordination role (bridge documentation maintenance)
Overlap / alternatives: `docs/34` covers the two-agent bridge workflow and the worker protocol text; `docs/14` covers the adaptive ST workflow Skill. Delta: neither documents the deterministic wrapper gate that enforces ST evidence on dispatches, its audit rules, or its failure and rollback model.
Why an existing doc cannot hold it: `docs/34` is the binding bridge contract plus a dated case study and already carries the wrapper-contract items in the Skill; a separate process card keeps the gate's own enforcement limits, ledger semantics and deployment status in one place without overloading the bridge doc.
Links: `docs/34-agora-goose-bridge.md`, `docs/14-sequential-thinking-workflow.md`, `docs/30-instance-overlay.md`, Skill `agora-goose-bridge`, Skill `sequential-thinking-workflow`.
Maintenance owner: coordination role (bridge documentation maintenance)
Expected reader: coordinators and reviewers who dispatch Goose runs and must accept or reject dispatch results based on wrapper evidence.
