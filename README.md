# better-prompt

A Claude skill that turns a rough prompt into the strongest prompt for reaching the goal behind it. It follows
Anthropic's current prompting guidance and the Claude Code methods senior engineers use.

- `SKILL.md` and `references/` are the live version (see `VERSION`). The claude.ai loader fetches them each time it
  runs, so the uploaded skill never needs re-uploading.
- `rsi/` is the improvement loop: real uses are labelled from what happened next, bad ones become test cases, and a
  change goes live only if it passes a blind, held-out check (see `rsi/README.md`). Real prompts and results are
  private and never stored in this repo.
- `research/` holds the dated, sourced notes the references are built from.
