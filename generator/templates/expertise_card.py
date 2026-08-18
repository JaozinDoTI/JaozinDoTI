"""SVG template: recruiter-oriented technical positioning."""

from generator.utils import esc
from generator.templates.cosmic_background import render as render_cosmic_background

WIDTH, HEIGHT = 850, 180


def render(items: list, theme: dict) -> str:
    """Render the three technical pillars a recruiter should identify quickly."""
    visible = items[:3]
    colors = [theme["synapse_cyan"], theme["dendrite_violet"], theme["axon_amber"]]
    cell_width = WIDTH / max(len(visible), 1)
    cells = []
    dividers = []
    cosmic = render_cosmic_background("expertise-card", WIDTH, HEIGHT, theme, preset="card")

    for index, item in enumerate(visible):
        center_x = cell_width * index + cell_width / 2
        color = colors[index % len(colors)]
        cells.append(
            f"""  <g transform="translate({center_x}, 0)">
    <circle cx="0" cy="72" r="18" fill="{color}" opacity="0.07"/>
    <circle cx="0" cy="72" r="4" fill="{color}" opacity="0.9"/>
    <line x1="-38" y1="72" x2="-8" y2="72" stroke="{color}" opacity="0.3"/>
    <line x1="8" y1="72" x2="38" y2="72" stroke="{color}" opacity="0.3"/>
    <text x="0" y="108" text-anchor="middle" fill="{theme['text_bright']}" font-size="19" font-weight="bold" font-family="sans-serif">{esc(item['value'])}</text>
    <text x="0" y="130" text-anchor="middle" fill="{color}" font-size="9" font-weight="bold" font-family="monospace" letter-spacing="0.7">{esc(item['label'])}</text>
    <text x="0" y="150" text-anchor="middle" fill="{theme['text_dim']}" font-size="10" font-family="sans-serif">{esc(item['detail'])}</text>
  </g>"""
        )
        if index < len(visible) - 1:
            x = cell_width * (index + 1)
            dividers.append(
                f'  <line x1="{x}" y1="58" x2="{x}" y2="154" stroke="{theme["star_dust"]}" opacity="0.5"/>'
            )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">
  <defs>
{cosmic.defs}
  </defs>
  <rect data-svg-layer="background" x="0.5" y="0.5" width="{WIDTH - 1}" height="{HEIGHT - 1}" rx="12" fill="{theme['void']}" stroke="{theme['star_dust']}"/>
{cosmic.elements}
  <g data-svg-layer="content">
  <text x="30" y="31" fill="{theme['text_faint']}" font-size="11" font-family="monospace" letter-spacing="3">ATUAÇÃO TÉCNICA</text>
  <text x="820" y="31" text-anchor="end" fill="{theme['text_faint']}" font-size="9" font-family="monospace">BACKEND DEVELOPER • SOFTWARE ENGINEER</text>
  <line x1="30" y1="47" x2="820" y2="47" stroke="{theme['star_dust']}" opacity="0.35"/>
{chr(10).join(dividers)}
{chr(10).join(cells)}
  </g>
</svg>"""
