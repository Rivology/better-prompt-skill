---
name: better-prompt
description: Turn a rough prompt into the strongest prompt for getting Claude to reach that goal, using Anthropic's current prompting best practices. Use when the user says "improve/upgrade/rewrite/optimize this prompt", "make this a better prompt", "/better-prompt", or pastes a prompt and asks how to get better results from Claude.
---

# Better Prompt

Turn the user's rough prompt (the skill arguments; if none, ask them to paste it) into the prompt most likely to
get Claude to the result they actually want. Then explain briefly what you changed, and offer to run it.
`references/prompting-guide.md` is your checklist. Read it first.

## 1. Understand the request

- **Real goal:** what the user ultimately wants, not just the literal words, and the task type (bug, feature,
  research, writing, data, learning, automation, system prompt for an AI app).
- **What Claude can't see:** the why, what done looks like, preferences, constraints, audience, deadline.
- **Software project** (an app, site, tool or sizeable feature)? Also read `references/project-building.md` and
  shape the rewrite as it describes, sized to the project: every project gets a spec, a first milestone,
  user-level testing and checks for its specific risks; large or multi-session ones add the bookkeeping
  (feature file, progress file, per-feature commits, review per milestone).
- **Visual work** (a page, screen, poster, slide, game or chart)? Also read `references/visual-design.md`: ask for a
  distinctive design that fits the context, and make the finish line rendering it and checking it at phone and desktop size.
- **Inside a project folder?** Take a quick look (a few reads or greps) so you can name real files, commands and patterns.
- **Already strong** (clear goal, specifics, constraints)? Say so, keep their wording verbatim, and append only
  what's missing, usually the "Done when:" line. Skip to step 4.

## 2. Fill the gaps

- **Decisive and unguessable** (it changes what gets built: platform, audience, minimal vs. full): ask with
  AskUserQuestion, once, at most 3 multiple-choice questions, recommended option first. Then rewrite with the answers.
- **Everything else:**
  - A default for something unstated (a priority, target, audience, threshold) goes inline as
    `(assumed: …; change if not)`, never as plain fact.
  - A fact the prompt relies on (names, hours, numbers) is either given by the user or a
    `[PLACEHOLDER: …]`, never invented.
  - For code and data, facts in the repo or files (test command, paths, patterns, column names) are not
    placeholders: tell Claude to find them and report what it found.
  - For code, a behaviour detail only the user knows (a time or size limit, a file, command or function name, how
    it's run, what happens on bad input) is a `[PLACEHOLDER: …]`, not an assumption: a wrong guess there ships as a
    bug. Include only the ones this task's behaviour depends on.
- **Route:** if it would need more than ~5 placeholders, or the user clearly hasn't decided what they want,
  write an interview prompt instead: "Interview me with multiple-choice questions until you could write the
  spec, then write it to SPEC.md."

## 3. Write the prompt

Use only the items that help *this* task:

1. **Goal and why**, in a sentence or two.
2. **Specifics Claude can't find:** files, the error or symptom, links, examples, data.
3. **Scope:** "be ambitious: …" listing the extras wanted, or "keep it minimal: …".
4. **Preferences and constraints**, stated positively, with the reason.
5. **Output:** format, length, where to save it, what to report back.
6. **Process steps** only where order matters (e.g. "reproduce with a failing test first, then fix").
7. **End with "Done when:"**, a concrete check plus the evidence to show, matched to the task: code → tests,
   build or a screenshot vs. the mockup; research → claims cited, dated, cross-checked; writing → length,
   audience and tone met, with a self-review against the goal; studying → a score on fresh problems without
   hints; data → numbers that reconcile with a known total. Tutoring and brainstorming are interactive, one
   step at a time. Keep the user's own "Done when" if they gave one.

Style: plain sentences in the user's voice, as a message they would send. No ALL CAPS, "IMPORTANT", "think
step by step" or "don't be lazy". Right-size it: a small task gets a few sentences, and only long multi-part
tasks get headings or XML tags. Long pasted material goes first, the request last. Keep the user's facts exactly.

## 4. Reply

1. **Improved prompt** in one fenced `text` block, ready to copy.
2. **What changed:** 3–6 short bullets, each naming the technique and why it helps here.
3. **Fill in / assumptions** (only if any): the placeholders and the defaults you chose.
4. One line: "Want me to run this prompt now?"
   On yes, carry out the improved prompt as the task.

## Example

Rough: `make me a website for my bakery`

```text
Build a one-page website for my bakery, [PLACEHOLDER: bakery name] in [PLACEHOLDER: city]. Its job is to get
local customers to visit or call, so the address, hours and phone number should be visible without scrolling.

Include a hero with the name and a short tagline, a menu with [PLACEHOLDER: 5-10 items with prices], hours with
a map link, and a contact section. Warm, simple design that works well on phones (assumed: most visitors are on
mobile; change if not). Use plain HTML and CSS in a single index.html, no frameworks, so I can host it anywhere.

Done when: the page opens with no console errors, the address, hours and phone are above the fold at phone and
desktop widths, the phone number and map link work, and you've shown me screenshots at both widths.
```

What changed: stated the goal (visits and calls) so design choices serve it; listed the sections; chose a
stack that's easy to host; marked the mobile assumption; made the finish line a check aimed at the goal.
