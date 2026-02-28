# SKILL.md — Frontend Implementation Agent

## Purpose
Specialized agent for implementing UI components with precision and performance.

## Capabilities
- Convert design specs to React/Next.js components
- Implement animations with Framer Motion
- Ensure responsive design
- Optimize for Core Web Vitals
- Write clean, maintainable TypeScript

## Tech Stack
- Next.js 14 (App Router)
- React 18+
- TypeScript
- Tailwind CSS
- Framer Motion
- Lucide React (icons)

## Component Patterns

### Glassmorphism Card
```tsx
<div className="relative overflow-hidden rounded-2xl bg-white/10 backdrop-blur-xl border border-white/20 shadow-[0_8px_32px_rgba(0,0,0,0.1)]">
  <div className="absolute inset-0 bg-gradient-to-br from-white/10 to-transparent" />
  <div className="relative p-6">{children}</div>
</div>
```

### Brutalist Button
```tsx
<button className="px-6 py-3 bg-yellow-400 border-4 border-black text-black font-bold uppercase tracking-wider shadow-[4px_4px_0px_#000] hover:translate-x-[2px] hover:translate-y-[2px] hover:shadow-[2px_2px_0px_#000] transition-all">
  {label}
</button>
```

### Dark Premium Input
```tsx
<input className="w-full px-4 py-3 bg-[#1A1A1A] border border-white/10 rounded-lg text-white placeholder:text-white/40 focus:outline-none focus:border-blue-500/50 focus:ring-1 focus:ring-blue-500/50 transition-all" />
```

## Animation Standards

| Animation | Duration | Easing |
|-----------|----------|--------|
| Hover | 200ms | ease-out |
| Modal open | 300ms | cubic-bezier(0.16, 1, 0.3, 1) |
| Page transition | 500ms | cubic-bezier(0.16, 1, 0.3, 1) |
| Stagger children | 50ms delay | ease-out |

## File Structure
```
components/
  ui/           # Reusable UI primitives
  layout/       # Layout components
  features/     # Feature-specific components
  animations/   # Animation wrappers
```
