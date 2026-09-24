## SPL Localization + Repair Workflow

SPL is a source-derived structured behavior map. In this variant it is used once
as a compact owner-to-patch controller, not as two separate localization and
repair investigations. The embedded SPL Patch Production Plan is the main SPL
artifact to follow.

Step 1: Follow the embedded SPL Patch Production Plan first. Run its first
source command and inspect that real source owner. Do not open every SPL card;
open `/tmp/spl_tools/source_bound_cards.md` only if the primary owner is visibly
wrong.

Step 2: Map one SPL checkpoint to visible source, then turn it into one source
question about a condition, return, assignment, call, parser/formatter rule,
exception path, or data-flow edge.

Step 3: If the visible source owner can control the issue behavior, edit there
immediately. Prefer a narrow named function, expression, branch, return,
assignment, or formatter/printer handler. If the primary owner cannot control
the behavior, inspect at most one narrow sibling or the listed secondary owner
before broader search.

Step 4: Patch the smallest mapped source construct and use SPL only to preserve
nearby behavior. Do not rewrite broad helpers, constructors, wrappers, callers,
dispatchers, broad fallback handlers, or unrelated semantic neighbors.

Step 5: After editing, run at most one issue-specific sanity check. If that
check passes, stop searching immediately; create and inspect `patch.txt`, then
submit in the next action. Do not run edge-case sweeps, broad test suites, or
extra dispatcher investigations after a passing check. Every response must
contain exactly one `mswea_bash_command` block; never answer with analysis text
only.
