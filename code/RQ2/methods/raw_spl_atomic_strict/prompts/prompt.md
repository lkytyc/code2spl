{official_prompt}

## SPL source-bound analysis control

{spl_control}

## Atomic function source + SPL cards

{spl_inline}

Follow the official dependence definition exactly. The SPL cards are an
auto-generated semantic description of the code and are evidence for its
intended behavior, but they are not guaranteed correct; when an SPL description
and the numbered source disagree, the source is the ground truth. Derive every
reported variable instance and line number from the numbered source code.
For information flow, compute the complete
bidirectional dependence component around the queried instance. Do not report a
query instance unless that numbered line defines or updates it, and do not
report an object used only as a method-call receiver unless the object's value
itself participates in the computed flow. A receiver initialized from another
object's data-returning call carries that returned value and must remain in the
flow; a root I/O handle initialized only from an external stream does not.
Return only the exact JSON object
required by the official prompt, with no prose or markdown.
