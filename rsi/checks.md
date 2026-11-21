# The checks a rewrite is judged on

Each check is a yes/no question about one rewrite. A judge answers `pass`, `fail` or `na` (doesn't apply to this
request), with a one-line reason. They come from what actually went wrong in real uses (see `README.md`), not from
a general idea of a good prompt. Holistic 1–10 prompt scores were retired by the old loop because they didn't predict
results (52% agreement on 21 pairs, 2026-10-28). Binary checks tied to observed failures are easier to calibrate and
to read.

Universal checks (asked of every rewrite):

- **U1 deliverable**: the rewrite asks for the same kind of deliverable the user asked for: a list stays a list,
  advice stays advice, a new thing stays new rather than a change to an existing one, and a follow-up keeps the
  deliverable of the request it refines.
- **U2 owner-choices**: every choice that changes what gets built, which the user didn't settle and which can't be
  found in their files, is put to the user (a question or options), rather than decided silently. Reasonable defaults
  for small details, marked as assumptions, pass.
- **U3 protect-what-works** (`na` unless the request changes something that already exists and works): the prompt
  protects it: it records a baseline or the current behaviour, changes it in steps that each leave it working, and
  checks the old main path still works at the end.
- **U4 bar** (`na` unless the user names a quality bar, a reference or an example to match): the prompt turns the bar
  into a concrete side-by-side comparison against that reference that decides when the work is done.
- **U5 done**: the prompt ends with a "Done when" that Claude can actually check, and it asks for evidence.
- **U6 right-size**: the length and machinery fit the task: a small task gets a few sentences; headings, stages,
  progress files and subagents appear only where the work is long or multi-part.
- **U7 faithful**: it keeps the user's facts and intent and adds no requirement the user didn't imply.
- **U8 leverage** (`na` for short one-shot tasks): for long, agentic or multi-session work, it picks the Claude Code
  methods that fit (an interview or plan first when the request is open, a progress file, a verifier in its own
  context or `/goal`, subagents only for independent parts) and leaves out ones that don't.

Case checks: each case in the bank can add one or two checks of its own, written from that real use's failure,
e.g. "treats 'sometimes through lecture' as an open question or as conversation, not as a separate lecture mode".
