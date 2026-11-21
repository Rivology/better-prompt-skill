# Judging rubric for better-prompt rewrites

You are comparing two replies, each produced by a version of a "prompt improver" for the same rough prompt.
Each reply has an improved prompt plus a short explanation. Judge mainly the **improved prompt**: if the
user sent it to Claude, which one would get them closer to what they actually wanted?

Score each response 1–10 on each dimension:

- **goal**: states the real goal and why, so Claude can make good trade-offs.
- **context**: supplies or asks for what Claude can't see (files, facts, audience, preferences) via clear
  placeholders or sensible stated defaults; asks an interview question route when the request is too open.
- **verification**: defines done with a check Claude can actually run or report, suited to the task type,
  and asks for evidence.
- **scope**: makes scope and constraints explicit (ambitious vs. minimal), phrased positively with reasons.
- **right_sized**: as long as the task needs and no longer. Penalize padding, needless headings/XML on small
  tasks, outdated tricks (ALL CAPS, "think step by step", "don't be lazy"), and heavy rewriting of a prompt
  that was already strong.
- **faithful**: keeps the user's facts and intent; doesn't invent requirements the user didn't imply.

Then pick a **winner** (1, 2, or "tie" if they're truly equivalent). The winner is the one whose
improved prompt would produce the better result for the user, not the one that's longer or fancier.
Don't let position or length sway you.

Output format: one JSON object keyed by the pair id in each file's heading (e.g. "p007"):

```json
{
  "p007": {"winner": 1, "scores1": {"goal": 8, "context": 7, "verification": 9, "scope": 7, "right_sized": 8, "faithful": 9},
          "scores2": {"goal": 6, "context": 6, "verification": 5, "scope": 6, "right_sized": 9, "faithful": 9},
          "note": "one sentence: the decisive difference, and any weakness both share"}
}
```
