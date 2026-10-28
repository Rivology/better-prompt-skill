---
name: better-prompt
description: Turn a rough prompt into the strongest prompt for getting Claude to reach that goal, using Anthropic's current prompting best practices. Use when the user says "improve/upgrade/rewrite/optimize this prompt", "make this a better prompt", "/better-prompt", or pastes a prompt and asks how to get better results from Claude.
argument-hint: <your rough prompt>
---

# Better Prompt

The user gives you a rough prompt. Your job is to return the best prompt for reaching the goal behind it,
explain briefly what you changed, and offer to run it. Read `references/prompting-guide.md` (next to this
file) before rewriting; it is the checklist you apply.

The rough prompt is in the skill arguments. If there are none, ask the user to paste the prompt they want improved.

## 1. Understand the goal

Work out, from the prompt and the current conversation/project:

- **Task type:** fix a bug, build a feature, refactor, research, write/edit, analyze data, learn/study,
  automate, or a system prompt for an AI app. This decides which checklist items matter.
- **The real goal:** what the user ultimately wants, not just the literal words.
- **What Claude can't see:** goal/why, definition of done, preferences, constraints, audience, deadline.
- **Software project?** If it asks to build an app, site, tool, or a sizeable feature, also read
  `references/project-building.md` and shape the rewrite as it describes, sized to the project: every project gets
  a spec, a first milestone, user-level testing and checks for its specific risks; large or multi-session ones
  add the bookkeeping (feature file, progress file, per-feature commits, review per milestone).

If you are inside a project folder and the prompt is about that code, take a quick look (a few reads or
greps, no more) so you can name real files, test commands, and existing patterns in the rewrite. Don't
explore beyond that.

## 2. Fill gaps: ask or assume

Sort missing information into two piles:

- **Decisive and unguessable** (it would change what gets built, e.g. which platform, who the audience is,
  minimal vs. full-featured): ask with AskUserQuestion, at most 3 questions, multiple choice, recommended
  option first. Ask once; don't loop.
- **Everything else:** pick a sensible default and state it in the prompt, or leave a clearly marked
  `[PLACEHOLDER: what goes here]` the user can fill in.
  Any default you pick for something the user didn't state (a priority, target, audience, emphasis,
  threshold) goes in the prompt marked inline as `(assumed: …; change if not)`, never as plain fact.
  Any fact the prompt relies on (hours, names, commands, numbers) is either given by the user or a placeholder,
  so the prompt never asks Claude to use information nobody supplied.
  Exception for code and data tasks: facts Claude can read from the repo or the files themselves (test
  framework, run/test commands, file paths, existing patterns, column names) aren't placeholders; tell
  Claude to find them and report what it found.

Ask first, then rewrite with the answers. If asking isn't possible or the user skips it, use placeholders.

Choosing a route: if the rewrite would need more than about 5 placeholders, or the user plainly hasn't
decided what they want (large, open-ended), write an **interview prompt** instead: "Interview me with
multiple-choice questions until you could write the spec, then write it to SPEC.md." Otherwise use placeholders.

## 3. Write the improved prompt

Apply the checklist from the guide, keeping only what helps *this* task:

1. Open with the goal and why it matters, in one or two sentences.
2. Give the specifics Claude can't find: files/paths, the error or symptom, links, examples, data.
3. State the scope explicitly: either "be ambitious: …" listing the extras wanted, or "keep it minimal: …".
4. State preferences between reasonable approaches and constraints, positively and with their reason.
5. Define done with a check Claude can run, and ask for evidence of the result. Match it to the task:
   code → tests, build, lint, screenshot vs. mockup; research → claims cited to sources, dated, cross-checked;
   writing → meets a word count, audience and tone, plus a self-review against the stated goal;
   studying → a score on fresh practice problems without hints; data → numbers that reconcile with a known total.
   For tutoring or brainstorming, say it should be interactive (one step at a time, waiting for replies).
   Always end the improved prompt with a line starting "Done when:" that names the concrete check and the
   evidence to show (command output, screenshots, sources, score). If the user's prompt already has one, keep theirs.
6. Specify the output: format, length, where to save it, what to report back.
7. Add process steps only where order matters (e.g. "reproduce with a failing test first, then fix";
   "explore and plan before editing").

Style rules for the rewrite:

- Plain, direct sentences. Write it in the user's voice, as a message they would send.
- No ALL CAPS, no "IMPORTANT", no "think step by step", "be thorough", or "don't be lazy";
  those are outdated and cause over-application or over-work.
- Right-size it. The checklist is for spotting gaps; leave out items that don't matter here. A small task gets a few sentences; only long, multi-part tasks get headings or
  XML tags (`<context>`, `<instructions>`, `<example>`). Never pad a simple request into an essay.
- Put long pasted material first and the request last.
- Keep the user's own facts exactly; don't invent requirements they didn't imply. Mark assumptions.

## 4. Reply format

Reply with exactly these parts:

1. **Improved prompt** in one fenced `text` code block, ready to copy.
2. **What changed**: 3–6 short bullets, each naming the technique and why it helps here
   (e.g. "Added a check to run: Claude can verify its own work instead of stopping when it looks done").
3. **Fill in / assumptions** (only if there are any): list the placeholders and any defaults you chose.
4. Ask one line: "Want me to run this prompt now?"
   If they say yes, carry out the improved prompt as the task.

If the original prompt is already strong (clear goal, specifics, constraints), say so, keep the user's wording
verbatim, and append only what's missing (usually the "Done when:" line). Don't rephrase it or add new requirements.

## Example

Rough: `make me a website for my bakery`

Improved:
```text
Build a one-page website for my bakery, [PLACEHOLDER: bakery name] in [PLACEHOLDER: city]. Its job is to get
local customers to visit or call, so the address, hours, and phone number should be visible without scrolling.

Include: a hero section with the name and a short tagline, a menu section with [PLACEHOLDER: 5-10 items with
prices], hours and a map link, and a contact section. Warm, simple design that works well on phones,
since most visitors will be on mobile.

Use plain HTML and CSS in a single index.html, no frameworks, so I can host it anywhere. When you're done,
open it in the browser at phone and desktop widths, fix anything that looks broken, and show me screenshots of both.
```

What changed: stated the goal (visits and calls) so design choices serve it; listed the sections; fixed
the tech choice so it's easy to host; added a check (view at both widths) and asked for evidence
(screenshots); marked what only the user knows as placeholders.
