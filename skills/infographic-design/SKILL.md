---
name: infographic-design
description: Design a single-page infographic — one clear takeaway, strict visual hierarchy from headline stat to supporting detail, restrained color and icon use, rendered as a self-contained HTML/SVG artifact. Use when the user wants an infographic, a one-pager, a poster-style summary, or a shareable visual explainer — not an interactive dashboard or a data-chart-library plot.
---

# Design an Infographic

Build a single-page infographic that communicates one idea at a glance —
different from a chart or dashboard, which is read closely and often explored.

## Steps

1. Identify the single takeaway the infographic must communicate, in one
   sentence. If the request bundles several unrelated messages, split into
   multiple infographics or ask the user which is primary — an infographic
   that tries to say five things ends up saying none of them clearly.
2. Gather the 3-7 supporting data points or facts that back the takeaway.
   Beyond roughly 7 discrete stats on one page, the "understand it in 5
   seconds" read that defines the format breaks down — group related points
   or cut the weakest ones.
3. Choose a layout that matches the content's shape:
   - One dominant stat + a short supporting list → hero-stat layout (huge
     number at the top, 3-4 smaller supporting facts below).
   - Sequential/process content → a numbered step flow (top-to-bottom or
     left-to-right).
   - Comparison → side-by-side panels or a simple icon/bar comparison, not a
     dense multi-series chart.
   - Timeline → a horizontal or vertical line with milestone markers.
4. Establish a strict type scale before writing any content: one size for the
   headline stat (largest — roughly 4-8x body size), one for section labels,
   one for body/supporting text. Three sizes is usually enough; more
   fragments the hierarchy the reader is supposed to follow.
5. Pick a restrained palette: one accent color for emphasis (the headline
   stat, key icons) plus one or two neutrals for everything else. Reserve the
   accent exclusively for what matters most — if everything is colored,
   nothing stands out. If the infographic embeds an actual chart (not just
   icons/stats), follow the `dataviz` skill's palette method for that component.
6. Use icons sparingly and consistently: one icon set/style throughout (all
   outline or all filled, never mixed), sized to a shared grid, and only where
   they add scannable meaning — not as decoration next to every line of text.
7. Build it as a self-contained artifact (see the `artifact-design` skill for
   the general Artifact mechanics): inline SVG for icons/illustrations so
   nothing depends on external assets, CSS flexbox/grid for layout, and no
   interactivity — infographics are static, read top-to-bottom or in one
   glance, not explored with hover/click.
8. Check the render at both a small size (as it'll appear as a shared
   thumbnail or preview image) and full size — the headline stat and takeaway
   must stay legible scaled down; if they don't, the hierarchy is wrong.
9. Run the 5-second test: could someone who only looks for 5 seconds state the
   one takeaway? If not, the headline element isn't dominant enough — go back
   to step 4 and widen the gap between it and everything else.

## Examples

### BAD: everything competes for attention

A page with 14 stats in same-sized boxes, 4 different accent colors, and 3
different icon styles. Nothing draws the eye first; the reader has to read
everything to find anything.

### GOOD: one dominant number, everything else supports it

A single "73%" in huge type at the top, one muted accent color used only on
that number and its icon, 4 supporting facts below in a smaller uniform size,
one consistent outline icon style. The takeaway is legible from across the room.

### BAD: chart-density thinking applied to an infographic

```
<!-- Cramming a 12-category stacked bar chart with a legend into
     a "quick facts" infographic -->
```
This is dashboard density, not infographic density — the reader has to study
it, which defeats the format.

### GOOD: the same comparison, infographic-appropriate

```
<!-- Top 3 categories only, as three icon+number pairs side by side,
     with "+9 more" as a small footnote if completeness matters -->
```

## Notes

- **Vs. `dataviz`/`visualization`**: those skills produce charts and
  chart-heavy dashboards meant for close reading and often interactive
  exploration — maximize data-ink from the full dataset. An infographic
  inverts that: it's a single static page meant to be understood in seconds,
  so cut aggressively instead of maximizing density.
- **Vs. `artifact-design`**: that skill covers general Artifact production
  mechanics (self-contained HTML, responsive layout, favicon, etc.). This
  skill is the content/information-design layer specific to infographics —
  use both together when producing an HTML infographic artifact.
- If the user wants a downloadable image rather than an on-screen artifact,
  note that browser "print to PDF" or a manual screenshot is the only export
  path available here — there's no server-side rasterization tool.
