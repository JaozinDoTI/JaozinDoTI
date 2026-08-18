"""SVG template: measurable professional impact (850x190)."""

from generator.utils import esc

WIDTH, HEIGHT = 850, 190


def render(items: list, theme: dict) -> str:
    """Render up to three impact indicators using the profile theme."""
    visible = items[:3]
    colors = [
        theme["synapse_cyan"],
        theme["axon_amber"],
        theme["dendrite_violet"],
    ]
    cell_width = WIDTH / max(len(visible), 1)
    cells = []
    dividers = []

    for index, item in enumerate(visible):
        center_x = cell_width * index + cell_width / 2
        color = colors[index % len(colors)]
        cells.append(
            f"""  <g transform="translate({center_x}, 0)">
    <circle cx="0" cy="73" r="22" fill="{color}" opacity="0.08"/>
    <circle cx="0" cy="73" r="5" fill="{color}" opacity="0.9">
      <animate attributeName="r" values="4;6;4" dur="3s" begin="{index * 0.4}s" repeatCount="indefinite"/>
    </circle>
    <line x1="-34" y1="73" x2="-9" y2="73" stroke="{color}" stroke-width="1" opacity="0.35"/>
    <line x1="9" y1="73" x2="34" y2="73" stroke="{color}" stroke-width="1" opacity="0.35"/>
    <text x="0" y="116" text-anchor="middle" fill="{theme['text_bright']}" font-size="25" font-weight="bold" font-family="sans-serif">{esc(item['value'])}</text>
    <text x="0" y="137" text-anchor="middle" fill="{color}" font-size="10" font-weight="bold" font-family="monospace" letter-spacing="1">{esc(item['label'])}</text>
    <text x="0" y="157" text-anchor="middle" fill="{theme['text_dim']}" font-size="11" font-family="sans-serif">{esc(item['detail'])}</text>
  </g>"""
        )
        if index < len(visible) - 1:
            x = cell_width * (index + 1)
            dividers.append(
                f'  <line x1="{x}" y1="55" x2="{x}" y2="165" stroke="{theme["star_dust"]}" stroke-width="1" opacity="0.55"/>'
            )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">
  <rect x="0.5" y="0.5" width="{WIDTH - 1}" height="{HEIGHT - 1}" rx="12" ry="12"
        fill="{theme['nebula']}" stroke="{theme['star_dust']}" stroke-width="1"/>
  <line x1="30" y1="47" x2="820" y2="47" stroke="{theme['star_dust']}" stroke-width="1" opacity="0.35"/>
  <text x="30" y="31" fill="{theme['text_faint']}" font-size="11" font-family="monospace" letter-spacing="3">IMPACTO GERADO</text>
{chr(10).join(dividers)}
{chr(10).join(cells)}
</svg>"""
