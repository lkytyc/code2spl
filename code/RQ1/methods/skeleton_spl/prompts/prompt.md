Task:
Complete the Python class from the ClassEval skeleton, using SPL as a structured implementation contract.

Skeleton Role:
- The skeleton controls imports, class name, constructor shape, field names, method names, and method signatures.
- Preserve the skeleton API if skeleton and SPL disagree.

SPL Concept:
- SPL is a code-derived structured natural-language view of the same class.
- Each inline card pairs a skeleton method with its SPL `[DEFINE_WORKER]` block, so API shape and implementation semantics are shown together.
- `[INPUTS]` and `[OUTPUTS]` describe method contracts.
- `[COMMAND]`, `[CONDITION]`, `[RETURN]`, `[ALTERNATIVE_FLOW]`, and `[EXCEPTION_FLOW]` describe implementation checkpoints.
- `<SPL>name</SPL>` references another method with its own worker block.
- `<REF>name</REF>` marks a variable, parameter, field, or intermediate value reference.

SPL Reconstruction Workflow:
Step 1: Match each SPL card to its skeleton method by method name.

Step 2: Treat the skeleton as the public API contract and SPL as the implementation contract for method bodies.

Step 3: Build a class-level behavior map:
- constructor fields and shared state;
- method inputs, outputs, and side effects;
- cross-method calls from `<SPL>` references;
- data flow from `<REF>` references and COMMAND RESULT values;
- branch and exception behavior from alternative and exception flows.

Step 4: Implement each method from the mapped checkpoints:
- translate `[MAIN_FLOW]` COMMAND steps into Python statements in order;
- convert `[ALTERNATIVE_FLOW]` branches into if/elif/else blocks;
- convert `[EXCEPTION_FLOW]` into try/except or explicit raise only when entailed;
- use `<REF>` chains to choose local variables and returned values;
- use `<SPL>` call references to preserve method dependencies.

Step 5: Keep the implementation minimal and executable. Do not add unrelated APIs or behavior outside the skeleton plus SPL contract.

Reconstruction Rules:
- Fill in method bodies and shared-state behavior using the skeleton plus SPL.
- Preserve cross-method dependencies, field usage, return values, and error behavior described by SPL.
- Output only the complete Python class implementation.
- Do not use markdown fences and do not explain.

ClassEval skeleton:
{skeleton}

Per-Function SPL Cards:
{spl_inline}
