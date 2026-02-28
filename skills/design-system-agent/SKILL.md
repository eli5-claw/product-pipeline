# SKILL.md — Design System Agent

## Purpose
Specialized agent for creating and maintaining design systems based on specific aesthetic references.

## Capabilities
- Analyze design references (Aura.build, Dribbble, Behance, etc.)
- Extract color palettes, typography, spacing, shadows, animations
- Create Tailwind config extensions
- Document component specifications
- Generate Figma-ready design tokens

## Input Format
```
Reference: [URL or description]
Vibe: [glassmorphism | brutalism | minimal | dark-premium | etc.]
Output: [tailwind-config | design-tokens | component-specs]
```

## Output Format
```json
{
  "colors": {
    "primary": "#...",
    "secondary": "#...",
    "accent": "#...",
    "background": "#...",
    "surface": "#..."
  },
  "typography": {
    "heading": "...",
    "body": "..."
  },
  "effects": {
    "shadows": [...],
    "blur": "...",
    "borders": "..."
  },
  "spacing": {...},
  "animations": {...}
}
```

## Aura.build Reference Style Guide

### Glassmorphism
- Backdrop blur: 8px-24px
- Background: rgba(255,255,255,0.1) to rgba(255,255,255,0.3)
- Border: 1px solid rgba(255,255,255,0.2)
- Shadow: 0 8px 32px rgba(0,0,0,0.1)
- Gradient overlays for depth

### Brutalism
- Thick borders: 3px-4px solid black
- Hard shadows: 4px 4px 0px #000
- Bold typography, uppercase headings
- Vibrant accent colors (neon pink, electric blue, acid green)
- Asymmetric layouts
- Visible grid lines

### Neo-Brutalism
- Combination of brutalism + modern polish
- Rounded corners (8px-16px) with thick borders
- Pastel backgrounds with bold accents
- Playful illustrations
- Hover effects: lift + shadow shift

### Dark Premium (Linear-style)
- Background: #0A0A0A to #111111
- Surface: #1A1A1A to #222222
- Border: rgba(255,255,255,0.1)
- Accent: Electric blue (#3B82F6) or Purple (#8B5CF6)
- Subtle glows on interactive elements
