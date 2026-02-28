# SKILL.md — Frontend Engineer

## Description
Implements production-ready React/Next.js components from design specifications. Translates design tokens into precise, accessible, performant code.

## When to Use
- Design system is ready and needs implementation
- Building specific features or pages
- Creating reusable component library
- Optimizing existing components

## Tech Stack
- Next.js 14 (App Router)
- React 18+
- TypeScript
- Tailwind CSS
- Framer Motion (animations)
- Lucide React (icons)

## Input
```json
{
  "component": "button|card|input|modal|navigation|chart|table",
  "designSpec": {},
  "variants": ["primary", "secondary", "ghost"],
  "interactions": ["hover", "active", "disabled"],
  "responsive": true|false
}
```

## Process

### 1. Component Structure
```tsx
interface ComponentProps {
  // Props based on design spec
}

export function Component({ ...props }: ComponentProps) {
  return (
    // Implementation
  );
}
```

### 2. Style Implementation
- Use Tailwind classes matching design tokens
- Implement all interaction states
- Add Framer Motion animations
- Ensure responsive behavior

### 3. Accessibility
- ARIA labels where needed
- Keyboard navigation
- Focus visible states
- Screen reader support

### 4. Testing Checklist
- [ ] Visual matches design spec
- [ ] All states work (hover, active, disabled)
- [ ] Animations smooth (60fps)
- [ ] Responsive at all breakpoints
- [ ] Accessible (keyboard, screen reader)

## Component Patterns

### Button
```tsx
<button
  className={cn(
    "px-6 py-3 font-bold transition-all duration-200",
    variant === 'primary' && "bg-purple-600 text-white hover:bg-purple-700",
    variant === 'secondary' && "bg-white text-black border-2 border-black",
    className
  )}
>
  {children}
</button>
```

### Card
```tsx
<div className="bg-[#111] border-[3px] border-black rounded-2xl shadow-[4px_4px_0px_#000]">
  {children}
</div>
```

### Input
```tsx
<input
  className="w-full bg-[#1A1A1A] border border-white/10 rounded-lg px-4 py-3
    focus:border-purple-500 focus:ring-1 focus:ring-purple-500
    text-white placeholder:text-white/40"
/>
```

## Output
- Component file(s) in `/components/[category]/`
- Storybook story (optional)
- Usage examples

## Tools
- `write` — Save component files
- `read` — Check existing components for consistency

## Example Usage
```
Implement the AnalyticsCard component from the VibeAnalytics design system.
Specs: glassmorphism background, 3px black border, 4px shadow, hover lift effect.
```

## Best Practices
- Use `cn()` utility for class merging
- Forward refs for component composition
- Document props with JSDoc comments
- Keep components focused and composable
