# spl-code-understanding

Use this skill when a task asks for behavior-oriented code understanding, bug
localization, cross-function flow tracing, impact analysis, or code modification
where the responsible file/function is not already obvious.

Do not use this skill for README edits, ordinary documentation updates,
formatting-only work, spelling fixes, a clearly specified one-line config
change, or a simple edit in an explicitly named file.

Core rules:

- Do not request repository-wide SPL generation.
- Do not use Codex itself to generate SPL.
- The SPL service uses the existing configured SPL generator.
- SPL is semantic navigation and current-behavior explanation, not source truth.
- Verify important SPL-derived conclusions against current source code.
- Do not edit code based on stale SPL.
- Tests are stronger runtime evidence than static SPL interpretation.

Recommended workflow:

1. Start with lightweight native inspection: directory shape, exact errors,
   symbols, tests, and obvious file names.
2. If the task remains behavior-oriented, ambiguous, branch-heavy, or
   cross-function, call `spl_understand`.
3. Keep the first call small: at most 5 candidates and generation budget 3,
   unless the task explicitly needs more.
4. Treat `spl_understand` output as candidate evidence. Open the returned
   `file_path` and source line range before relying on it.
5. Use `spl_expand` only when callers, callees, or one-hop flow context is
   needed. Default depth is 1; never expand the whole call graph.
6. Before editing, identify the smallest source responsibility in real code.
7. After source edits, run relevant tests when possible and call `spl_refresh`
   with the changed files if the SPL tool is available.
8. If SPL is missing, over budget, stale, unsupported, or failing, continue with
   native search and source reading.

For SWE-bench style experiments:

- Native condition: do not call SPL.
- SPL Forced condition: call `spl_understand` after lightweight native search.
- SPL Auto condition: call SPL only when the trigger conditions above apply.
- The SPL Generator must not receive the issue text, gold patch, failing
  expected output, or fixed code. The service should only send function source
  and static context to the existing generator.

Final answers should distinguish SPL evidence, source evidence, and test
evidence when that distinction matters.
