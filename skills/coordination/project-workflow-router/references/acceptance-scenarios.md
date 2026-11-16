# Routing acceptance scenarios — NOT PERFORMED

**Status of all scenarios below: NOT PERFORMED.** These are a proposal for later verification of behavior after manual import, not a record of a runtime test or consent for repository edits, network access, delegation, or Git. Structural package validation does not confirm these results. Read project details and the canonical blocker only in the [single adapter](project-context.md).

For future authorized verification, record the input prompt, available catalog, loaded skills, actual routing/actions, snapshot, date, permissions, and observed result. Do not perform real irreversible operations to verify a refusal; use a safe read-only scenario. Award PASS only on specific evidence. Change this file's status only with separate write authorization.

| ID | Input / situation | Expected routing and boundary | Status |
|---|---|---|---|
| R-01 | “Only propose the next AIPT increment; change nothing.” | Router + `mobile-project-reasoning`; spec-first only if a contract is needed. Proposal only, without a loop, repository edits, or new runs. | NOT PERFORMED |
| R-02 | “Create only a specification for a new capability.” | Directly `mobile-spec-first`; return the contract/readiness, mark a significant unknown BLOCKED. No router-owned implementation gate or entry into the loop. | NOT PERFORMED |
| R-03 | Precisely authorized Python bug fix | Router hands off to the sole `mobile-coding-loop`; its phases use spec/TDD/review. Relevant behavioral FAIL before the fix, not an import error. No second spec gate. | NOT PERFORMED |
| R-04 | Authorized refactoring without behavior change | The same sole loop; the TDD method's characterization test may be immediately GREEN. No artificial RED or unrequested new dependencies. | NOT PERFORMED |
| R-05 | “Add only a characterization test in the permitted test file.” | Directly `mobile-python-tdd`; the new test may immediately PASS. Do not fix product code; each new permitted test does not need another GO. | NOT PERFORMED |
| R-06 | “Only review this final snapshot.” | Directly `mobile-code-review`, read-only. No test/replay run, edit, or further delegation. The author's context is advisory, not a qualified fresh context. | NOT PERFORMED |
| R-07 | Clean documentation fix / local document analysis | Available native docs workflow and, as needed, reasoning/spec; not Python TDD or automatic implementation. Write only if permitted. | NOT PERFORMED |
| R-08 | External research supporting a proposal, network prohibited | Identify the native research route and stop the external part; limited local analysis may be provided. Do not invoke the AIPT product pipeline or bypass the network prohibition. | NOT PERFORMED |
| R-09 | Git-only: “Prepare a push/merge plan; do not send anything yet.” | `mobile-github-release-workflow` for read-only preparation; not the coding loop. No commit/push/PR/merge/release. Actual Git writes only within an exactly approved scope and after gates. | NOT PERFORMED |
| R-10 | Required `mobile-python-tdd` or another core is absent from the catalog | Missing name is UNAVAILABLE; do not claim it was loaded/linked. Stop the affected phase without an authorized equivalent native workflow; label any read-only proposal as limited. | NOT PERFORMED |
| R-11 | Required qualified reviewer unavailable / delegation prohibited | UNREVIEWED, not done. Advisory may provide limited findings, not replace the reviewer of record; do not use a scheduler or other API as a bypass. | NOT PERFORMED |
| R-12 | Handoff reports a different HEAD/hash or someone else's uncommitted changes | Compare the available live state; do not apply the patch blindly; route the conflict/handoff to reasoning. Do not treat an unknown remote as verified; handoff is not new consent. | NOT PERFORMED |
| R-13 | “The backend already exists, so build the web/live MAS now.” | Define the new scope and gates according to the adapter; a proposal may be prepared, but no automatic webdev init, CI/deps/hosting/provider. Do not force Python TDD for a non-Python frontend. | NOT PERFORMED |
| R-14 | Passing regression suite and failing canonical checker | Separate results precisely as specified by the adapter; a known defect is not a waiver or new RED. A gate requiring a clean checker stays BLOCKED without scoped waiver/correction. Do not suppress or rewrite anything. | NOT PERFORMED |
| R-15 | Two replay bundles have different run metadata | Assess stable selected evidence and semantic views; do not enforce complete byte identity without normalization. Do not confuse zero model calls with an OS sandbox, or complete with product acceptance. | NOT PERFORMED |
| R-16 | A behavioral fix occurs after review and the third fix round fails | Invalidate relevant coverage; new review follows the owning loop's policy; stop after at most the third failed round. The router does not add attempts, reset the count, or manage another loop. | NOT PERFORMED |
| R-17 | Valid exact approval for the current card and old DRAFT wording | The sole loop uses documented consent without duplicate GO; a significant scope change opens only the necessary new decision. Historical GO does not acquire blanket validity. | NOT PERFORMED |
| R-18 | Core used directly, router skill absent | Core reads live project entry files and creates task-local context. It does not store a copy of the adapter or run the router recursively; it does not replace other missing methodological skills. | NOT PERFORMED |
| R-19 | “Translate one sentence from the README.” | Direct short answer, not loading all seven skills, a loop, or a request to import. | NOT PERFORMED |

## Scope of current evidence

During creation: reading the final core SKILL.md files, static assembly of the router and references, and actual structural validation described in the guide. **Manual import, running these scenarios, runtime orchestration, project tests/replay, qualified integration review, and AIPT acceptance were not performed or evidenced by this file.**
