"""SVG template: operational context behind the PRISMA case."""

from generator.utils import esc

WIDTH, HEIGHT = 850, 165


def render(items: list, theme: dict) -> str:
    """Render up to three historical process indicators."""
    visible = items[:3]
    colors = [theme["synapse_cyan"], theme["dendrite_violet"], theme["axon_amber"]]
    cell_width = WIDTH / max(len(visible), 1)
    cells = []

    for index, item in enumerate(visible):
        center_x = cell_width * index + cell_width / 2
        color = colors[index % len(colors)]
        cells.append(
            f"""  <g transform="translate({center_x}, 0)">
    <circle cx="0" cy="76" r="3" fill="{color}" opacity="0.75"/>
    <line x1="-48" y1="76" x2="-9" y2="76" stroke="{color}" opacity="0.22"/>
    <line x1="9" y1="76" x2="48" y2="76" stroke="{color}" opacity="0.22"/>
    <text x="0" y="105" text-anchor="middle" fill="{theme['text_bright']}" font-size="21" font-weight="bold" font-family="sans-serif">{esc(item['value'])}</text>
    <text x="0" y="124" text-anchor="middle" fill="{color}" font-size="9" font-weight="bold" font-family="monospace" letter-spacing="1">{esc(item['label'])}</text>
    <text x="0" y="142" text-anchor="middle" fill="{theme['text_dim']}" font-size="10" font-family="sans-serif">{esc(item['detail'])}</text>
  </g>"""
        )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">
  <rect x="0.5" y="0.5" width="{WIDTH - 1}" height="{HEIGHT - 1}" rx="12" ry="12"
        fill="{theme['void']}" stroke="{theme['star_dust']}" stroke-width="1"/>
  <text x="30" y="31" fill="{theme['text_faint']}" font-size="11" font-family="monospace" letter-spacing="3">CONTEXTO OPERACIONAL</text>
  <text x="820" y="31" text-anchor="end" fill="{theme['text_faint']}" font-size="9" font-family="monospace">PROCESSO ANALISADO • NÃO REPRESENTA GANHO DIRETO</text>
  <line x1="30" y1="47" x2="820" y2="47" stroke="{theme['star_dust']}" opacity="0.3"/>
{chr(10).join(cells)}
</svg>"""
