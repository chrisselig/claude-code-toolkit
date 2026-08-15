---
name: ui-components
description: Build consistent, accessible React UI components — matching the project's styling approach, typing props explicitly, and covering accessibility basics. Use when creating or reviewing UI components for a web app.
---

# Build UI Components

Write React components that are typed, accessible, and consistent with the
rest of the app — not a one-off snowflake.

## Steps

1. Determine the project's existing styling approach before writing anything —
   don't introduce a second styling system into a project that already picked
   one:
   - `tailwind.config.*` present → Tailwind utility classes.
   - `*.module.css` files → CSS Modules.
   - `styled-components` or `@emotion/*` in `package.json` → CSS-in-JS.
   - Nothing yet (new project) → ask the user, or default to Tailwind for a
     new `new-web-app` scaffold.
2. Type every component's props with an explicit `interface Props { ... }` (or
   `type Props = {...}`). Never use `any`. Avoid `React.FC` — it implicitly
   adds a `children` prop even for components that don't accept one.
3. Default to function components with hooks. Keep components focused: if a
   component's JSX exceeds roughly 150 lines or mixes unrelated concerns
   (data fetching + layout + business logic), split it into smaller pieces
   composed together rather than one large component branching on every variant.
4. Lift state only as high as the nearest common consumer actually needs it.
   Don't reach for a global store (Context, Redux, Zustand) for state only one
   or two components use — that's what `useState`/`useReducer` in the parent is for.
5. Cover accessibility basics on every interactive element:
   - Buttons use `<button>`, not `<div onClick>`.
   - Images have meaningful `alt` text (or `alt=""` if purely decorative).
   - Form inputs have an associated `<label>` (via `htmlFor`/`id` or wrapping).
   - Interactive elements are keyboard-operable — verify with Tab/Enter, not
     just a mouse click.
6. Pull colors, spacing, and typography from the project's design tokens
   (Tailwind theme config, CSS variables, or a theme object) instead of
   hardcoding hex values or magic pixel numbers — those drift from the rest of
   the app the first time the palette changes.
7. Before adding a new dependency for something common (modal, tooltip,
   accordion, dropdown), check whether the project already has a component
   library installed (Radix, Headless UI, shadcn/ui, MUI). Use its primitive
   rather than hand-rolling focus-trap/keyboard/ARIA behavior that's easy to
   get subtly wrong.

## Examples

### Interactive elements

**BAD** — not focusable, not announced to screen readers, no keyboard support:
```tsx
<div onClick={handleSubmit}>Submit</div>
```

**GOOD** — native semantics, keyboard support for free:
```tsx
<button type="button" onClick={handleSubmit}>Submit</button>
```

### Styling tokens

**BAD** — a color no one else in the app is using, invisible to a future
palette change:
```tsx
<div style={{ color: "#3b82f6", padding: "13px" }}>...</div>
```

**GOOD** — uses the project's Tailwind theme tokens:
```tsx
<div className="text-primary p-3">...</div>
```

### Props typing

**BAD**:
```tsx
function Badge(props: any) {
  return <span>{props.label}</span>;
}
```

**GOOD**:
```tsx
interface BadgeProps {
  label: string;
  variant?: "default" | "success" | "warning";
}

function Badge({ label, variant = "default" }: BadgeProps) {
  return <span className={variantClasses[variant]}>{label}</span>;
}
```

## Notes

- For chart/graph-specific visual design (color scales, chart types, legends),
  use the `dataviz` skill instead — this skill covers general UI components,
  not data visualization.
- In Next.js, components are server components by default. Only add
  `"use client"` at the top of a file when it actually needs state, effects,
  or a browser-only API — marking everything client-side loses the framework's
  server-rendering benefits.
- If the project has an existing component library or design system, match it
  rather than introducing a competing pattern, even if you'd choose differently
  on a greenfield project.
