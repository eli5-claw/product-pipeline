# SKILL.md — Design System Architect

## Description
Creates comprehensive, reference-based design systems for web applications. Specializes in translating visual inspiration into concrete design tokens, component specs, and Tailwind configurations.

## When to Use
- Starting a new product and need a visual identity
- Have design references (Dribbble, Behance, Aura.build) to translate into code
- Need to document existing design patterns
- Creating reusable component libraries

## Input
```json
{
  "references": ["https://example.com/design"],
  "vibe": "glassmorphism|brutalism|minimal|dark-premium|neo-brutalism|custom",
  "productType": "dashboard|landing|saas|ecommerce|mobile",
  "outputFormat": "tailwind-config|css-variables|component-specs|all"
}
```

## Process

### 1. Analyze References
- Extract color palettes (primary, secondary, accents, neutrals)
- Identify typography (fonts, weights, sizes, line heights)
- Document spacing patterns
- Note effects (shadows, blur, gradients, animations)
- Capture layout principles

### 2. Define Design Tokens
```json
{
  "colors": {
    "primary": "",
    "secondary": "",
    "accent": "",
    "background": "",
    "surface": "",
    "text": ""
  },
  "typography": {
    "fontFamily": "",
    "headingSizes": {},
    "bodySizes": {},
    "lineHeights": {}
  },
  "spacing": {},
  "effects": {
    "shadows": [],
    "blur": "",
    "borders": ""
  }
}
```

### 3. Component Specifications
For each component:
- Visual appearance (colors, borders, shadows)
- Interaction states (default, hover, active, disabled)
- Animation specifications
- Responsive behavior

### 4. Output Deliverables
- Complete design system document
- Tailwind config extension
- CSS variables file
- Component specification sheet

## Output Format

```markdown
# Design System — [Product Name]

## Color Palette
| Token | Hex | Usage |

## Typography
| Level | Size | Weight | Usage |

## Spacing
| Token | Value | Usage |

## Effects
| Effect | Value | Usage |

## Components
### [Component Name]
- **Appearance:** ...
- **States:** ...
- **Animation:** ...
```

## Tools
- `web_fetch` — For analyzing reference URLs
- `browser` — For screenshot capture (if available)
- `write` — To save design system file

## Example Usage
```
Create a design system for VibeAnalytics with Neo-Brutalist aesthetic.
References: Aura.build style, thick borders, hard shadows, vibrant accents on dark background.
```

## Notes
- Always name specific references in output
- Include exact hex codes, not approximations
- Document animation timing functions precisely
- Consider dark mode as default for modern SaaS
