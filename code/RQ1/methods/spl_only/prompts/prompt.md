Task:
Reconstruct one complete executable Python class from the SPL input.

SPL Concept:
- SPL is the only program representation in this condition.
- SPL is a code-derived structured natural-language view of a class.
- Each inline card has a `### Function:` header followed by that method's `[DEFINE_WORKER]` block.
- `[INPUTS]` and `[OUTPUTS]` describe contracts.
- `[COMMAND]`, `[CONDITION]`, `[RETURN]`, `[ALTERNATIVE_FLOW]`, and `[EXCEPTION_FLOW]` describe implementation checkpoints.
- `<SPL>name</SPL>` references another method with its own worker block.
- `<REF>name</REF>` marks a variable, parameter, field, or intermediate value reference.

SPL Reconstruction Workflow:
Step 1: Scan all `[DEFINE_WORKER]` blocks to infer class name, constructor, field assignments, method names, method signatures, and return behavior.

Step 2: Build a class-level behavior map:
- fields and shared state from `self.<name>` references and COMMAND RESULT values;
- method contracts from `[INPUTS]` and `[OUTPUTS]`;
- call graph from `<SPL>` references;
- data flow from `<REF>` references and COMMAND RESULT values;
- branch and exception behavior from alternative and exception flows.

Step 3: Implement each method from its checkpoints:
- main flow becomes the normal statement order;
- alternative flows become conditional branches when their condition is supported;
- exception flows become try/except or explicit raise only when required;
- referenced values become local variables, fields, calls, or returned values.

Step 4: Use the simplest valid Python implementation when formatting, style, or exact variable names are omitted.

Step 5: Do not invent unrelated behavior that is not supported by the SPL contract.

Reconstruction Rules:
- Identify the class, constructor, fields, methods, dependencies, return values, and error behavior described by SPL.
- Preserve cross-method calls, field usage, control flow, data flow, return values, and exceptions.
- Output only the complete Python class implementation.
- Do not use markdown fences and do not explain.

SPL Input:

{spl_inline}
