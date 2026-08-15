# /infographic-design

Design a single-page infographic — a shareable visual explainer meant to be
understood in about 5 seconds, not an interactive dashboard or a data chart.

## What It Does

1. Pins down the single takeaway the page must communicate.
2. Narrows supporting content to 3-7 facts — enough to back the takeaway,
   few enough to stay scannable.
3. Picks a layout to match the content shape: hero-stat, step flow,
   comparison panels, or timeline.
4. Locks in a strict 3-size type scale so the headline stat dominates.
5. Picks one accent color plus 1-2 neutrals — reserved for what matters most.
6. Uses one consistent icon style, sparingly.
7. Renders as a self-contained HTML/SVG artifact — static, no interactivity.
8. Checks legibility at thumbnail size, then runs a 5-second takeaway test.

## Example

```
/infographic-design
```

```
Takeaway: "73% of support tickets are resolved without a human"
Supporting facts: 4 (avg resolution time, top ticket categories, CSAT score, trend vs last quarter)
Layout: hero-stat (73% dominant, 4 facts below)
Palette: one teal accent + charcoal/gray neutrals
Icons: single outline set, used only on the 4 supporting facts

→ Rendered as a self-contained HTML artifact, 5-second test passed
  (headline stat readable at thumbnail size).
```

## Notes

- Different job from [Data Visualization](visualization.md) — that skill
  maximizes data-ink for close reading; an infographic cuts aggressively for
  an at-a-glance read.
- Pairs with the general Artifact mechanics (self-contained HTML, favicon,
  responsive layout) — this skill is the content/hierarchy layer on top.
- No server-side image export in this environment — "print to PDF" or a
  screenshot is the path to a downloadable image file.
