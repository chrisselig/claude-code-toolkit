# /ui-components

Build React UI components that are typed, accessible, and consistent with the
rest of the app — matching its existing styling approach instead of
introducing a new one.

## What It Does

1. Detects the project's styling approach (Tailwind, CSS Modules, CSS-in-JS)
   and matches it.
2. Types every component's props explicitly — no `any`, no `React.FC`.
3. Keeps components focused; splits large or multi-concern components into
   smaller composed pieces.
4. Lifts state no higher than the nearest common consumer needs.
5. Covers accessibility basics: semantic elements, `alt` text, labeled inputs,
   keyboard operability.
6. Uses the project's design tokens instead of hardcoded colors/spacing.
7. Prefers an existing component library's primitives (Radix, Headless UI,
   shadcn/ui, MUI) over hand-rolling accessibility-sensitive widgets.

## Example

```
/ui-components
```

```
Detected: Tailwind (tailwind.config.ts present)
Detected: shadcn/ui components in src/components/ui/

Building Badge component:
- interface BadgeProps with explicit variant union
- Uses theme tokens (text-primary, bg-muted) instead of hex values
- Reuses existing Tooltip primitive from src/components/ui/tooltip.tsx
  instead of adding a new dependency
```

## Notes

- For chart/graph visual design, use the `dataviz` skill instead — this skill
  is for general UI components, not data visualization.
- In Next.js, only mark a component `"use client"` when it actually needs
  state, effects, or a browser API.
- Match an existing design system even where you'd choose differently on a
  greenfield project.
