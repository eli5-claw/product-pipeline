# SKILL.md — Visual Scraper

## Description
Captures and analyzes visual designs from websites. Extracts color palettes, typography, layouts, and effects for design system creation.

## When to Use
- Need to understand a reference design precisely
- Creating design system from visual inspiration
- Documenting competitor designs
- Reverse-engineering UI patterns

## Prerequisites
- Browser automation must be available
- Chrome extension must be attached to target page

## Input
```json
{
  "urls": ["https://example.com/design"],
  "capture": ["screenshot", "css", "colors", "typography", "layout"],
  "outputFormat": "detailed|summary|design-tokens"
}
```

## Process

### 1. Navigate to Page
```
browser open [url]
```

### 2. Capture Screenshot
```
browser screenshot --fullPage
```

### 3. Extract Visual Data
Use browser evaluate to extract:
- Color palette (computed styles)
- Typography (font families, sizes)
- Spacing (padding, margins)
- Effects (shadows, borders, blur)

### 4. Analyze Components
Identify and document:
- Button styles
- Card designs
- Input fields
- Navigation patterns
- Hero sections

### 5. Output Design Spec
```json
{
  "url": "",
  "screenshot": "path/to/screenshot.png",
  "colors": {
    "primary": "",
    "secondary": "",
    "background": "",
    "text": ""
  },
  "typography": {
    "heading": "",
    "body": "",
    "sizes": {}
  },
  "components": {
    "buttons": {},
    "cards": {},
    "inputs": {}
  }
}
```

## Output Format

```markdown
# Visual Analysis — [URL]

## Screenshot
[Attached image]

## Color Palette
| Element | Hex | RGB | Usage |

## Typography
| Element | Font | Size | Weight |

## Layout
- Container max-width: 
- Grid system: 
- Spacing scale: 

## Components
### Buttons
- Primary: ...
- Secondary: ...

### Cards
- Background: ...
- Border: ...
- Shadow: ...

## Effects
- Shadows: ...
- Blur/backdrop: ...
- Animations: ...
```

## Tools
- `browser open` — Navigate to page
- `browser screenshot` — Capture visual
- `browser snapshot` — Extract structure
- `browser act` — Interact with elements
- `write` — Save analysis

## Example Usage
```
Scrape https://axion-ai.aura.build/
Capture: full screenshot, color palette, component styles
Output detailed design spec
```

## Limitations
- Requires active browser connection
- JavaScript-heavy sites may need wait time
- Dynamic content may require interaction

## Fallback Options
If browser unavailable:
1. Request user upload screenshot
2. Use external screenshot API
3. Ask user to describe design elements
