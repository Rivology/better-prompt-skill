# Check judge brief

You judge rewritten prompts. Each item in your batch file shows a user's original request, a short note on their
situation, and one rewritten prompt (labelled with an id). You never learn which version of the rewriting skill wrote
it, and the order is shuffled.

For every item, answer each check listed for it with `pass`, `fail` or `na`, and give a reason of at most 15 words.
The universal checks are defined in `checks.md` (read it first). Case checks are written out in the item.

- Judge the prompt as a message the user would send to Claude: would it lead Claude to what this user wanted?
- `na` only where the check's own wording says it may not apply. When in doubt between pass and fail, choose fail
  and say what's missing.
- Length is not a merit. A long prompt passes U6 only if the task needs it.
- Judge each item on its own; don't compare items.

Write one JSON object to `verdict.json` in your folder and check that it loads with `python3 -m json.tool`:

```json
{"r017": {"U1": ["pass", "keeps it a list of prompts"], "U3": ["na", "nothing existing changes"], "C1": ["fail", "decides lecture mode itself"]}}
```

Open nothing except `checks.md`, `batch.md` and `verdict.json`.
