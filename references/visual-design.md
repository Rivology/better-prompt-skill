# Prompting for visual work (refreshed 2026-10-28)

Use this when the result is something people look at: a web page, app screen, poster, slide, game screen or chart.

Source: Anthropic, "Prompting best practices", Frontend design section
(platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices).

## Ask for a distinctive design that fits the context

Without guidance, Claude tends toward generic, "on distribution" designs. A visual prompt should name the
context's character (audience, mood, where it's seen) and ask for a design made for it:
- **Typography:** distinctive fonts that suit the context, not defaults like Arial, Inter, Roboto or system fonts.
- **Color and theme:** one committed aesthetic, kept consistent with CSS variables; a dominant color with sharp
  accents beats a timid, evenly spread palette.
- **Backgrounds:** atmosphere and depth (layered gradients, patterns, context-fitting effects), not flat defaults.
- **Motion** (only where it fits): one well-orchestrated moment, such as a staggered reveal on load, beats scattered
  micro-animations. CSS-only for plain HTML.
- **Avoid:** clichés like purple gradients on white, and cookie-cutter layouts with no context-specific character.

Keep the user's stated style if they gave one; these defaults are for when they didn't.

## The finish line: look at it

The "Done when" for visual work asks Claude to render the result and look at it at phone (~390px) and desktop
(~1440px) widths, fix what's wrong, and show both screenshots. It counts as done only when:
- the layout **reflows** for the phone (it doesn't just shrink), and all text is legible at that size;
- the key information or action is visible without scrolling;
- nothing overflows, overlaps or gets cut off;
- for anything meant to print, it also fits its page size;
- it looks finished: no "draft" or "edit me" badges and no `[placeholder]` text on the visible page. Where a detail
  is missing, Claude writes a sensible version into the page, keeps notes for the user in code comments, and lists
  what to confirm or replace in its report.
