# Prompting Claude well (distilled; last refreshed 2026-10-28)

Sources: Anthropic's "Best practices for Claude Code" (code.claude.com/docs/en/best-practices),
Anthropic's "Prompting best practices" for current models
(platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices),
and community guides (Ilia Karelin, "How to Prompt Like an Anthropic Engineer"; Austin Marchese's
video "The ONLY 4 Things You Need To Prompt Like An Anthropic Engineer").

## The core idea

Claude is like a brilliant new colleague with no context. It can read your code and the web on its own,
so a good prompt mostly supplies what it **can't** see: your goal, your preferences, your definition of
done, and facts that live only in your head.

**Colleague test:** if you handed the prompt to a smart coworker with no context, would they know what
to do and when they're finished? If not, Claude won't either.

## The checklist (what a strong prompt contains)

1. **Goal + why.** What you want and what it's for. The reason lets Claude generalize and make the
   right trade-offs ("this will be read aloud by text-to-speech, so no ellipses" beats "NEVER use ellipses").
2. **Specifics Claude can't find.** Name the file/folder, describe the symptom, paste the error,
   attach the screenshot, `@`-mention the file. Hand things over instead of describing them.
3. **Definition of done + a check to run.** Something that comes back pass/fail: a test, a build,
   a linter, a script, a screenshot next to the mockup. "Run the auth tests after and keep going until
   they pass." Ask for **evidence** (the command and its output), not just "it works".
4. **Scope.** Claude reads requests conservatively and builds the smallest thing that fits. If you want
   more, say "be ambitious: empty/error states, keyboard nav, not just the layout". If you want minimal,
   say "only change what's needed; no new libraries; don't refactor surrounding code".
5. **Preferences between reasonable options.** If you care which approach, library, or pattern, say so
   ("follow the pattern in HotDogWidget.php").
6. **Constraints, stated positively, with reasons.** Say what to do rather than what not to do.
7. **Output format.** Exactly what you want back: file, table, prose, length, where to save it.
8. **Process, only when it matters.** For larger work: explore → plan → implement → verify.
   For bugs: reproduce with a failing test first, then fix.

## Examples

| Instead of | Try |
|---|---|
| fix the login bug | users report login fails after the session times out. look at token refresh in src/auth/, write a failing test that reproduces it, then fix it |
| add a calendar widget | follow the pattern in HotDogWidget.php and build a calendar widget that lets you pick a month and page between years. no new libraries |
| create an analytics dashboard | create an analytics dashboard. include as many relevant features and interactions as possible; go beyond the basics to a fully-featured implementation |

## When you don't know what you want yet

Don't force a spec. Ask Claude to interview you:
"I want to add rate limiting to the public API but haven't thought it through. Interview me until you
could write the spec, then write it to SPEC.md." Then build from SPEC.md in a fresh session.

## Structure tricks (use when the prompt is big)

- **XML tags** separate instructions from data: `<context>`, `<instructions>`, `<example>`, `<document>`.
- **Long material first, question last** (can improve quality noticeably on 20k+ token inputs).
- **Quote first:** for long documents, ask Claude to pull relevant quotes before answering.
- **Examples:** 3–5 varied ones in `<example>` tags are the strongest way to set format and tone.
- **Role:** one line ("You are a senior Python reviewer") focuses tone, mostly useful in system prompts.
- **Match style:** prompt in prose if you want prose back; markdown-heavy prompts get markdown-heavy answers.

## Research tasks

Define what a successful answer looks like, ask for verification across multiple sources, ask for
citations, and say how recent the information must be.

## Coding-specific guardrails (add only when relevant)

- "Investigate the relevant files before answering; don't speculate about code you haven't opened."
- "Write a general solution, not one that only passes the tests. If a test looks wrong, tell me instead of working around it."
- "Keep it minimal: no extra files, abstractions, or error handling for cases that can't happen."
- Reviews: "report gaps that affect correctness and skip style" (a reviewer asked to find problems always finds something).

## Things you can stop doing (outdated advice)

- ALL CAPS / IMPORTANT / NEVER everywhere → current models follow plain wording; emphasis makes them over-apply the rule.
- "think hard", "be thorough" → effort level is the real control (`ultrathink` still works for one turn).
- "don't be lazy, keep going until done" → causes over-work; give a check to pass instead.
- Describing your whole file layout → Claude reads the repo itself; only write what isn't in there.

## Making "done" stick

Ask for evidence (the command and its output, a screenshot) rather than "it works". For long runs, put the
check in a `/goal` condition: one measurable end state, how Claude proves it, and what must not change on the
way. For building whole apps or features, see `project-building.md`.

## Steering once it's running

Watch the first minute. `Esc` the moment it drifts. After two failed corrections, `/clear` and write
one better prompt that folds in what you learned, instead of a third correction.

## Beyond single prompts

If you've typed the same instructions twice, make it a skill (a folder with SKILL.md) or put the
fact in CLAUDE.md. Keep CLAUDE.md short: commands to run, conventions, gotchas.
