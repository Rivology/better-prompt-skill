# The better-prompt improvement loop (v2, 2026-11-21)

## Why v2

The first loop (`rsi.py`, kept on River's Mac) was careful about statistics but measured the wrong thing. It judged
finished work from short, one-shot writing and visual tasks. Meanwhile, most real uses (84 of 178) were overhauls of a
live system, and most of the uses that went badly failed in ways those tests can't show:

- the rewrite made a choice that was the user's, or changed the deliverable;
- an overhaul broke a working app;
- a quality bar was named but never turned into a check.

Only 17% of uses had any recorded outcome, and the loop hadn't kept a change by itself since 2026-11-02. The full
audit is kept with the project files, outside this public repo.

v2 is designed around one idea: **learn from real use, and judge each change on the same kinds of request that real
use brings.**

## The loop

```
real use ──log──▶ uses ──label (weekly, from transcripts)──▶ cases ──▶ cycle ──▶ keep / reject ──▶ publish
   ▲                                                                              │
   └──────────────────────── north star: share of uses that went badly, per version ┘
```

1. **Log every use** (`loop.py log`): the rough prompt, the full rewrite and the session id.
2. **Label from what happened next** (`briefs/labeler.md`). The weekly run reads the user's next messages in that
   session and labels the use `accepted`, `intent`, `scope`, `broke`, `bar`, `abandoned` or `unknown`, quoting the
   user's words. Asking the user directly got an answer 17% of the time; transcripts can label most uses.
3. **A bad label becomes a case.** Each case holds the real request, a note on the situation and one or two yes/no
   checks written from the failure. Uses that went well become *guard* cases, so the loop can't over-correct.
   Cases are split into train and held-out by a hash of the use id.
4. **A cycle tests one change** (`LOOP.md`):
   - two rewriters replay the cases with the live skill (A) and the candidate (B);
   - two blind judges answer the checks in `checks.md` for every rewrite;
   - `loop.py score` unblinds the result and applies the keep rule.
5. **Keep rule** (in `loop.py`; changing it is the user's decision):
   - on held-out cases, B's check pass rate is higher with p ≤ 0.05 (paired sign-flip test);
   - no universal check falls by more than 10 points;
   - guard cases get no worse by more than 0.05;
   - B's rewrites are at most 1.3 times as long (a guard against judges rewarding length);
   - a check counts only where the two judges agree at least 70% of the time;
   - **independent guard:** two more judges, who never see `checks.md`, compare A and B side by side on the
     holistic rubric (`briefs/pairwise_rubric.md`, written for the first loop), each seeing the pair in the other
     order. If they prefer A (mean below 0, p ≤ 0.10), the change is rejected. This rule was added on 2026-11-21,
     after it caught v22, which passed the checks but lost to v21 on this guard (see `CHANGELOG.md`).
6. **North star** (`loop.py northstar`): the share of labelled real uses that went badly, per version. This is the
   number that should fall over time. Everything else is a stand-in for it.

## What's deliberately different from v1

| v1 | v2 | Why |
|---|---|---|
| Synthetic one-shot tasks, executed and judged 1–10 | Real requests, judged on yes/no checks from real failures | Real use is mostly overhauls and agentic work, which one-shot execution can't show |
| Holistic prompt rubric, retired after it didn't predict results | Narrow binary checks, two judges, agreement measured | Checks tied to observed failures can be validated and read |
| An outcome check costing 1–6M tokens per cycle | About 8 agents per cycle: 4 rewriters and 4 judge batches | Weekly cycles become affordable |
| Outcome asked of the user (17% answered) | Outcome read from the transcript | More labels |
| p ≤ 0.10 on about 12 tasks | p ≤ 0.05 on held-out, plus guard and length rules | Fewer lucky keeps |
| Lived only in `~/.claude` | Code and briefs in this repo; private data in `$BP_DATA` | Versioned and reviewable, without publishing anyone's prompts |

v1's outcome machinery (executing prompts on fixture apps with hidden tests) is still the right tool for the
expensive question, whether better prompts produce better work. It becomes a monthly or on-demand check, not the
weekly gate.

## Files

- `loop.py`: logging, import of v1 data, harvesting, labels to cases, prepare, blind, score, northstar, lint.
- `checks.md`: the universal checks.
- `briefs/`: rewriter, judge and labeler briefs.
- `LOOP.md`: how to run a cycle by hand or from the weekly task.
- `scheduled/`: proposed prompts for the weekly and monthly tasks.
- `bench/`: synthetic request sets for side-by-side checks: the first loop's project and showcase tests, and 10
  requests set inside a Claude project, written by an independent agent.
- `briefs/pairwise_rubric.md`: the independent judges' rubric, written for the first loop.
- Private, never committed: `$BP_DATA/` (default `~/better-prompt-runs/rsi2/`), holding `uses.jsonl`,
  `labels.jsonl`, `cases.jsonl`, `history.jsonl` and `runs/`.
