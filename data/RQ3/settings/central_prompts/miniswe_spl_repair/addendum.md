## SPL Repair Workflow

SPL is a source-derived structured behavior map. In this variant it should make
repair faster by pointing to the likely current-behavior owner and preservation
checks. The editable source code is the only patch target.

Step 1: Follow the embedded SPL Patch Production Plan first. Run its first
source command and inspect the real source owner before broad search. Only open
`/tmp/spl_tools/source_bound_cards.md` if the embedded plan is insufficient.

Step 2: Compare the issue requirement with the visible source owner. Use the SPL
checkpoint to focus on the concrete source construct that may need changing:
condition, return, assignment, call, parser/formatter rule, exception path, or
data-flow edge.

Step 3: Patch the smallest source construct that owns the conflicting behavior.
Prefer a narrow named function, expression, branch, return, assignment, or
formatter/printer handler. Do not move to a helper, caller, constructor,
wrapper, broad fallback handler, dispatcher, or semantic neighbor unless the
visible source proves it directly controls the failing behavior.

Step 4: Use SPL only to preserve adjacent behavior after choosing the source
edit. Never copy SPL text, tags, summaries, or natural-language steps into the
patch.

Step 5: After editing, run at most one issue-specific sanity check. If it
passes, stop searching immediately, create and inspect `patch.txt`, then submit
in the next action. Do not run edge-case sweeps, broad test suites, or extra
dispatcher investigations after a passing check. Every response must contain
exactly one `mswea_bash_command` block; never answer with analysis text only.
