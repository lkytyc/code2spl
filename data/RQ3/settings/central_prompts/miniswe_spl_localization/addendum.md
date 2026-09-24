## SPL Localization Workflow

SPL is a source-derived structured behavior map. In this variant it should
reduce localization steps, not add a second investigation. The embedded SPL
Patch Production Plan names a source-bound owner, a first source command, and a
small edit focus.

Step 1: Follow the embedded SPL Patch Production Plan first. Run its first
source command before broad repository search. Only open
`/tmp/spl_tools/source_bound_cards.md` if the embedded plan is insufficient.

Step 2: Map one SPL checkpoint to visible source code. Use the SPL text to ask a
concrete source question about a condition, return, assignment, call,
parser/formatter rule, exception path, or data-flow edge.

Step 3: If the mapped source owns the issue behavior, edit the smallest source
construct there. Use secondary/context cards only when the primary source
visibly cannot control the issue.

Step 4: After editing, run at most one issue-specific sanity check. If it
passes, stop searching immediately. Then create and inspect `patch.txt`; do not
run edge-case sweeps, broad test suites, or dispatcher investigations once the
diff directly addresses the issue.

Step 5: Submit immediately in the next action after `patch.txt` looks
plausible. Every response must still contain exactly one `mswea_bash_command`
block; never answer with analysis text only.
