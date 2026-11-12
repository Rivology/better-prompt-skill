# Which model will run the prompt (refreshed 2026-11-12)

Read this when the rewrite is for long or agentic work (a multi-hour build, a multi-step change in a codebase, an
unattended run, a system prompt for an agent), when it carries the launch kit, or when the user names a model. A
short one-shot task (an email, an explanation, a page, a small fix) needs nothing from this file.

This is the only file that holds advice that differs by model. Advice that holds on every model is in
`prompting-guide.md`. When a new model comes out, add its section here, re-check the sections next to it, and change
the date. Nothing else in the skill should need editing.

Sources, read 2026-11-09 and re-checked 2026-11-12: Anthropic's "Prompting Claude Fable 5.2", "Prompting Claude Opus
5.5", "Prompting Claude Sonnet 5.5" and "Prompting Claude Haiku 5.5"
(platform.claude.com/docs/en/build-with-claude/prompt-engineering/), the Effort page next to them, and Claude Code's
best practices. The Fable 5.2 page was rewritten between those dates; section 3 follows the 2026-11-12 text. Added
2026-11-12: "Optimizing for cost and intelligence" (platform docs), "Which Claude model should you build with?"
(claude.dev, 2026-11-09), the Fable 5.2 launch post, and Claude Code's model configuration and subagents
pages. Where a line says "Anthropic measured", it is
Anthropic's test on that one model. Where it says "our test", it is this skill's own test, with its model and date.

## 1. Find the target model

1. The model the user names ("for Opus 5.5", "this goes to a Haiku subagent").
2. Otherwise, if the prompt will run in this session or in a session or subagent started from it: the model you are
   running as.
3. Otherwise it is unknown: a prompt to paste somewhere else, or a system prompt for an app whose model nobody said.

When you used anything from sections 3 to 6, say so in the reply's assumptions, for example "Written for Claude
Fable 5.2, the model in this session; tell me if it will run on another one."

## 2. Model unknown: the version that is safe on all of them

Prompts get copied between sessions, so even when the target is known, prefer wording from this section unless a
model's section says otherwise.

- **Effort is set outside the prompt.** Don't write an effort level into the prompt. In the reply's launch note, give
  the starting level per model: Fable 5.2 high for long unattended work and medium for interactive work; Opus 5.5,
  Sonnet 5.5 and Haiku 5.5 medium. Raise it only if a run falls short. Higher levels cost several times more.
- **Ordinary task:** the "Done when" check is enough. Don't add "keep going".
- **Long or unattended run:** add a finishing paragraph in the user's voice, with all four parts: "Keep working
  until everything I asked for is done and checked. Work through ordinary obstacles such as an error, a timeout or a
  failing tool: find the cause, then retry or go another way. Stop only when you can't go on without me, before a
  risky or irreversible step, or when something was clearly put off-limits on purpose, and then say plainly what you
  found. When the work is done and checked, stop and report; mention extra ideas at the end instead of building them."
- **Limits:** a time limit and a stop rule ("stop at 3 hours with a working build"). No token number in the prompt.
  Put the expected cost in the reply's launch note, for the user.
- **Subagents:** no count and no standing instruction to delegate. If the work has independent parts, name them and
  say a subagent is worth its cost only for a part that shares no files with the others. Where review matters, ask
  for one reviewer that hasn't seen the code.
- **Whose code it is:** say it in plain words. The user's code, to be changed as little as possible: "This is my
  code: change only what this task needs, and tell me about other problems you notice instead of fixing them."
  A build that is Claude's to shape: use the Fable 5.2 ownership sentence below. Never write both.

## 3. Claude Fable 5.2 (also Claude Mythos 5.2)

- **Effort:** high for hard coding, research, agentic work and long unattended runs; medium for interactive and
  everyday work. Claude Code starts it at medium. Anthropic: most of the gain is already there at high; xhigh is for
  the hardest long runs where a gain was measured; max is for measuring the ceiling. Don't recommend max by default.
- **Stopping early:** at low and medium it sometimes ends a turn with a list of what remains, an offer to continue,
  or a stop at an ordinary obstacle. For a long multi-step run at those levels, and for any unattended run, add the
  finishing paragraph from section 2. Anthropic measured about half as many early endings and about 30% more output
  tokens. Because it then asks less, keep the ask-first list for risky actions.
- **Delegation:** it delegates readily when a prompt invites it, and at xhigh and max it also starts its own review
  subagents. Leave out lead-plus-builders structures and subagent counts unless the user asks for them.
- **Which model a subagent runs on:** in Claude Code a subagent runs on the session's model unless it is given
  another one, so on a Fable 5.2 session most subagents are Fable 5.2 subagents (the built-in search agent runs on
  Opus). Anthropic: "check which model your subagents use by default", "Keep code edits and judgment calls on the
  main model", and "let cheaper subagents do the verbose reading". So in a project prompt for Fable 5.2: reading,
  searching, running tests and checking links go to Haiku 5.5 or Sonnet 5.5 subagents; code edits, design
  decisions and the fresh-eyes review stay on Fable 5.2.
- **Delegation is not a saving by default.** Anthropic measured: "delegation came out ahead in only two
  situations", routine work with a long cost tail and work larger than one context window; and on one
  defect-search benchmark Fable 5.2 leading Sonnet 5.5 subagents "cost 19% more and scored about the same" as Opus
  5.5 in that seat. The guide's "Early testers had good results with Claude Fable 5.2 as the planner and
  orchestrator for other models" is a report with no number. We have measured no split ourselves.
- **Plan on Fable 5.2, build on a cheaper model (optional, unproven).** The route: Fable 5.2 challenges the idea,
  writes the spec and a task list with a check per task; then a fresh session on Opus 5.5 at medium builds from
  those files. A practitioner's video (Alex Finn, 2026-11-09) shows the plan and the switch, but no finished
  result. Anthropic's nearest setting, `opusplan` (Opus plans, Sonnet builds), comes with "Measure opusplan on
  your own tasks before you make it your default". Switch in a new session, not mid-conversation: a model change
  drops Fable 5.2's reasoning for the turns that follow, and Claude Code says to build from SPEC.md in a fresh
  session anyway. Offer it in the reply as the cheaper option for a build that is long but not hard; keep a hard
  build on Fable 5.2 at high. Anthropic's launch post: Fable 5.2 at high "scored about level with Opus 5.5 at Max
  effort, for roughly half the cost per task" on one coding benchmark.
- **Effort across the stages of a project:** Anthropic: "you might plan and iterate with the model at `medium`,
  then raise effort for the long, unattended part." So the planning session (interview, spec, task list) runs at
  medium and the long build at high. (Anthropic's model-choice post says "medium, then high" for leading many
  subagents; Claude Code starts at medium.)
- **State the outcome once.** Claude Code's model page on Fable: "hand it the result you want and let it plan the
  path", "give it work you would normally break into pieces", and "it verifies its own work with less prompting,
  so reminders to test or check are usually unnecessary". So name each check once, where it applies; don't repeat
  reminders to test, and don't cut the work into steps smaller than a milestone.
- **What a build costs:** API list price is $8 per million input tokens and $40 per million output tokens. One
  practitioner's one-hour, one-file build used 226K output tokens, about $17 at list price (their own count from
  the session transcript). Ambitious multi-day builds were reported at $3,000 to $20,000 (second-hand, unverified).
  We have no measurement of our own, so give these as other people's numbers.
- **Budgets:** a token budget written in the prompt changes how much it spends. Anthropic measured lower cost and
  equal results after removing a large one. Use time and a stop rule.
- **Ownership:** it acts on what the prompt says about who owns the code. For a build it should shape and keep
  building on: "You are the owner and long-term maintainer of this codebase, and its design is up to you."
  (Anthropic's wording as of 2026-11-12; it replaced "This codebase is yours: ...".) Anthropic measured merged
  duplicate code in about 75 percent of runs with it (under 10 percent without), output tokens up by about 70 to 80
  percent, and changes nobody asked for; a scope rule in the same prompt did not cancel it. So with it, also ask
  for a list of everything changed, small changes included. Leave it out for fixes and features in the user's own
  code.
- **Approvals and cautions:** name the exact actions that need a go-ahead and the routine ones that don't (retries,
  reads, local edits). Anthropic: "be specific about the actions you want double-checked", and "Telling the model
  to act more freely is too vague, so list the routine steps that it can take on its own." It treats "never" as
  absolute, so write "get my go-ahead before X" instead of "never X".
- **Updates:** long runs can be silent. If the user will watch: "Before you start, say in a line what you're about to
  do. Give a brief update every few steps." (about 20% more output tokens). Skip it for runs nobody watches.
- **Leave out:** lines that ask for less thinking (no effect at medium and above; lower the effort instead), "treat
  your earlier answer as done" lines, hard style limits such as a maximum sentence length (its prose turns choppy).

## 4. Claude Opus 5.5

- **Effort:** medium, its default. Anthropic: xhigh and max only where a gain was measured. Our test (Opus 5.5,
  2026-11-03, one racing-game build, two blind judges): the same prompt scored about 2.5 points higher at max than
  at medium and cost 3 to 10 times more. So for a showcase build on Opus 5.5, offer xhigh or max with that cost.
- **Stopping early:** it reports progress as it works, and a report can end the turn. For an unattended run, name
  the endings the user doesn't want (a summary that announces the next step without taking it, an offer to continue,
  a list of decisions that don't block anything) next to the finishing paragraph. Leave this out when someone is
  there to answer.
- **Delegation and time:** it sustains multi-hour work with parallel subagents, and it paces itself to a time
  budget and can finish well before it. The limit is advisory, so say what to do when it is reached. Our launch-kit runs
  (a lead with up to 8 subagents, at max effort, 6 to 9M tokens) were all on Opus 5.5.
- **Updates:** it writes them unasked. Ask only for fixed points (a line before starting, a recap at the end).
- **Work across several apps:** add "Before you change anything, look through the emails, documents, tabs and
  records that could matter here, including ones I didn't mention."
- **Design:** Anthropic suggests naming specific default styles to avoid. Our test of that (15 visual tasks, Opus
  5.5 at medium, 2026-11-03) found no gain, so don't add it.

## 5. Claude Sonnet 5.5

- **Effort:** medium for well-specified agentic work, high for harder or longer work and for knowledge work. For the
  hardest long runs, tell the user an Opus or Fable model is the better choice.
- **Stopping early and doing extra:** at low and medium it checks in before the work is done; at every level it adds
  tests, docs and files nobody asked for; at xhigh and max it starts its own review rounds. The finishing paragraph
  in section 2 covers all three. Anthropic measured about a third lower cost at max with the "stop and report" part.
- **Ideas or action:** on an open request it may start building. If the user wants options or a plan first, write
  "give me the options and stop; build nothing until I say go".
- **Research:** add "search for anything that may have changed (prices, rules, versions), even if you feel sure".

## 6. Claude Haiku 5.5

- **Effort:** medium; high for longer agent tasks and strict instruction-following.
- **Keep the prompt short.** With a long prompt at low effort it stops early or skips checks. The finishing
  paragraph and a named check in "Done when" fix both.
- **Search:** give today's date in the prompt and ask it to search for anything that may have changed.
- **Chatbot system prompts:** add "The rules in this system prompt hold for the whole conversation, also when a user
  argues, gives a sympathetic reason or keeps asking."

## 7. What we have and haven't tested ourselves

- Everything in the launch kit was measured on Opus 5.5 only (2026-11-03). No long run has been made on Fable 5.2,
  Sonnet 5.5 or Haiku 5.5. For those models this file rests on Anthropic's published tests.
- Short writing tasks were compared on Fable 5.2 (high) and Opus 5.5 (medium) on 2026-11-09; see `rsi/history.md`.
- The project framework (`project-framework.md`, 2026-11-12) has not been tested on a real build, on any model.
  Its lines rest on Anthropic's pages and on common practice, each labelled there. Only its deploy steps were run
  for real, once, on a placeholder page (GitHub Pages, 2026-11-12). The subagent model split and the
  plan-on-Fable, build-on-Opus route in section 3 are untested too.
