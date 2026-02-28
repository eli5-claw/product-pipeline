"""
Eli5AI Visual Renderer
Generates infographics from thread specs.
"""

import json
from typing import Dict
from pathlib import Path


class InfographicRenderer:
    """Renders infographics as PNG images."""
    
    # Style constants
    BG_COLOR = "#0a0a0a"
    TEXT_COLOR = "#ffffff"
    SECONDARY_TEXT = "#a1a1aa"
    DEFAULT_ACCENT = "#3b82f6"
    
    def __init__(self, output_dir: str = "assets/infographics"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def render(self, spec: Dict, filename: str = None) -> str:
        """
        Render an infographic from spec.
        
        Returns:
            Path to generated PNG file
        """
        template = spec.get('template', 'definition_card')
        
        if template == 'definition_card':
            html = self._render_definition_card(spec)
        elif template == 'step_flow':
            html = self._render_step_flow(spec)
        elif template == 'ecosystem_map':
            html = self._render_ecosystem_map(spec)
        else:
            html = self._render_definition_card(spec)
        
        # Save HTML for debugging
        html_path = self.output_dir / f"{filename or 'latest'}.html"
        with open(html_path, 'w') as f:
            f.write(html)
        
        # TODO: Use Playwright or similar to convert HTML to PNG
        # For now, return HTML path
        return str(html_path)
    
    def _render_definition_card(self, spec: Dict) -> str:
        """Render a definition card template."""
        accent = spec.get('accent_color', self.DEFAULT_ACCENT)
        
        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            width: 1200px;
            height: 675px;
            background: {self.BG_COLOR};
            font-family: 'Inter', sans-serif;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 60px;
        }}
        .card {{
            width: 100%;
            text-align: center;
        }}
        .label {{
            color: {accent};
            font-size: 18px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-bottom: 20px;
        }}
        .title {{
            color: {self.TEXT_COLOR};
            font-size: 64px;
            font-weight: 700;
            margin-bottom: 24px;
            line-height: 1.1;
        }}
        .subtitle {{
            color: {self.SECONDARY_TEXT};
            font-size: 28px;
            line-height: 1.4;
            max-width: 900px;
            margin: 0 auto 40px;
        }}
        .features {{
            display: flex;
            justify-content: center;
            gap: 40px;
            margin-top: 40px;
        }}
        .feature {{
            text-align: center;
        }}
        .feature-icon {{
            width: 48px;
            height: 48px;
            background: {accent}20;
            border-radius: 12px;
            margin: 0 auto 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
        }}
        .feature-text {{
            color: {self.TEXT_COLOR};
            font-size: 16px;
            font-weight: 500;
        }}
        .footer {{
            position: absolute;
            bottom: 30px;
            left: 60px;
            color: {self.SECONDARY_TEXT};
            font-size: 14px;
        }}
    </style>
</head>
<body>
    <div class="card">
        <div class="label">What is</div>
        <h1 class="title">{spec.get('title', 'Topic')}</h1>
        <p class="subtitle">{spec.get('subtitle', '')}</p>
        <div class="features">
            <div class="feature">
                <div class="feature-icon">⚡</div>
                <div class="feature-text">Fast</div>
            </div>
            <div class="feature">
                <div class="feature-icon">🔒</div>
                <div class="feature-text">Secure</div>
            </div>
            <div class="feature">
                <div class="feature-icon">🌐</div>
                <div class="feature-text">Decentralized</div>
            </div>
        </div>
    </div>
    <div class="footer">@Eli5AI · eli5ai.xyz</div>
</body>
</html>"""
        return html
    
    def _render_step_flow(self, spec: Dict) -> str:
        """Render a step-by-step flow template."""
        accent = spec.get('accent_color', self.DEFAULT_ACCENT)
        steps = spec.get('steps', [])
        
        step_html = ""
        for i, step in enumerate(steps[:5]):
            num = i + 1
            # Clean up step text
            step_text = step.replace(f"❶", "").replace(f"❷", "").replace(f"❸", "").replace(f"❹", "").replace(f"❺", "").strip()
            step_html += f"""
            <div class="step">
                <div class="step-number">{num}</div>
                <div class="step-text">{step_text}</div>
            </div>
            """
        
        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            width: 1200px;
            height: 675px;
            background: {self.BG_COLOR};
            font-family: 'Inter', sans-serif;
            padding: 60px;
            display: flex;
            flex-direction: column;
        }}
        .header {{
            margin-bottom: 40px;
        }}
        .label {{
            color: {accent};
            font-size: 16px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-bottom: 12px;
        }}
        .title {{
            color: {self.TEXT_COLOR};
            font-size: 48px;
            font-weight: 700;
        }}
        .steps {{
            display: flex;
            gap: 20px;
            flex: 1;
            align-items: center;
        }}
        .step {{
            flex: 1;
            text-align: center;
            padding: 30px 20px;
            background: #18181b;
            border-radius: 16px;
            border: 1px solid #27272a;
        }}
        .step-number {{
            width: 48px;
            height: 48px;
            background: {accent};
            color: {self.BG_COLOR};
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
            font-weight: 700;
            margin: 0 auto 20px;
        }}
        .step-text {{
            color: {self.TEXT_COLOR};
            font-size: 16px;
            line-height: 1.5;
        }}
        .footer {{
            margin-top: 30px;
            color: {self.SECONDARY_TEXT};
            font-size: 14px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <div class="label">How it Works</div>
        <h1 class="title">{spec.get('title', 'Topic')}</h1>
    </div>
    <div class="steps">
        {step_html}
    </div>
    <div class="footer">@Eli5AI · eli5ai.xyz</div>
</body>
</html>"""
        return html
    
    def _render_ecosystem_map(self, spec: Dict) -> str:
        """Render an ecosystem map template."""
        # Simplified version
        return self._render_definition_card(spec)
