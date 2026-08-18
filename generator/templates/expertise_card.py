"""Technology constellation showing how the core stack connects."""

from generator.templates.cosmic_background import render as render_cosmic_background
from generator.utils import esc

WIDTH, HEIGHT = 850, 285


def _tech_node(x: int, y: int, name: str, color: str, primary: bool = False) -> str:
    radius = 25 if primary else 15
    font_size = 11 if primary else 9
    return f"""    <g class="stack-node">
      <circle cx="{x}" cy="{y}" r="{radius + 8}" fill="{color}" opacity="0.035"/>
      <circle cx="{x}" cy="{y}" r="{radius}" fill="{theme_placeholder('nebula')}" stroke="{color}" stroke-width="{1.2 if primary else .7}" stroke-opacity="{.68 if primary else .42}"/>
      <circle cx="{x}" cy="{y}" r="3" fill="{color}" class="stack-pulse"/>
      <text x="{x}" y="{y + radius + 18}" text-anchor="middle" fill="{color}" font-size="{font_size}" font-weight="bold" font-family="monospace">{esc(name)}</text>
    </g>"""


def theme_placeholder(key: str) -> str:
    return "__NEBULA__" if key == "nebula" else ""


def render(config: dict, theme: dict) -> str:
    core = config.get("core", ["TypeScript", "Node.js", "Fastify", "REST APIs"])
    data = config.get("data", ["SQL", "PostgreSQL", "MySQL"])
    satellites = config.get("satellites", ["React 19", "Vite", "Python", "PHP / Laravel", "Zod", "Docker"])
    cyan, violet, amber = theme["synapse_cyan"], theme["dendrite_violet"], theme["axon_amber"]
    cosmic = render_cosmic_background("technology-constellation", WIDTH, HEIGHT, theme, preset="card")
    core_positions = [(105, 128), (295, 128), (490, 128), (700, 128)]
    core_nodes = []
    for index, name in enumerate(core[:4]):
        color = [violet, cyan, cyan, amber][index]
        core_nodes.append(_tech_node(*core_positions[index], name, color, primary=True).replace("__NEBULA__", theme["nebula"]))
    data_positions = [(245, 228), (390, 228), (535, 228)]
    data_nodes = []
    for index, name in enumerate(data[:3]):
        data_nodes.append(_tech_node(*data_positions[index], name, violet, primary=False).replace("__NEBULA__", theme["nebula"]))
    satellite_positions = [(79, 69), (163, 62), (604, 66), (704, 63), (773, 80), (639, 228)]
    satellite_nodes = []
    for index, name in enumerate(satellites[:6]):
        color = amber if index in (0, 1, 3) else violet
        satellite_nodes.append(_tech_node(*satellite_positions[index], name, color, primary=False).replace("__NEBULA__", theme["nebula"]))

    links = [
        (105, 128, 295, 128, violet), (295, 128, 490, 128, cyan), (490, 128, 700, 128, amber),
        (295, 128, 245, 228, violet), (295, 128, 390, 228, violet), (490, 128, 535, 228, violet),
        (105, 128, 79, 69, amber), (105, 128, 163, 62, amber), (490, 128, 604, 66, violet),
        (700, 128, 704, 63, amber), (700, 128, 773, 80, amber), (490, 128, 639, 228, violet),
    ]
    lines = "\n".join(
        f'    <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="0.8" opacity="0.26" stroke-dasharray="3 6"/>'
        for x1, y1, x2, y2, color in links
    )
    flow_dots = "\n".join(
        f'    <circle cx="{x}" cy="128" r="2" fill="{cyan}" opacity="0.8" class="stack-flow" style="--stack-delay:{i * .7}s"/>'
        for i, x in enumerate((185, 375, 590))
    )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">
  <defs>
{cosmic.defs}
    <style>
      .stack-node {{ animation:stack-enter .7s ease-out both; transform-box:fill-box; transform-origin:center; }}
      .stack-node:nth-of-type(2n) {{ animation-delay:.15s; }}
      .stack-pulse {{ animation:stack-pulse 4s ease-in-out infinite; transform-box:fill-box; transform-origin:center; }}
      .stack-flow {{ animation:stack-flow 3.8s ease-in-out var(--stack-delay,0s) infinite; }}
      @keyframes stack-enter {{ from {{ opacity:0; transform:scale(.85); }} to {{ opacity:1; transform:scale(1); }} }}
      @keyframes stack-pulse {{ 0%,100% {{ opacity:.45; transform:scale(.8); }} 50% {{ opacity:1; transform:scale(1.3); }} }}
      @keyframes stack-flow {{ 0%,100% {{ opacity:.18; transform:translateX(-14px); }} 50% {{ opacity:.9; transform:translateX(14px); }} }}
    </style>
  </defs>
  <rect data-svg-layer="background" width="{WIDTH}" height="{HEIGHT}" fill="{theme['void']}"/>
{cosmic.elements}
  <g data-svg-layer="content">
    <line x1="425" y1="0" x2="425" y2="18" stroke="{violet}" opacity="0.4"/>
    <text x="35" y="36" fill="{theme['text_faint']}" font-size="10" font-family="monospace" letter-spacing="3">CORE TECHNOLOGY CONSTELLATION</text>
    <text x="815" y="36" text-anchor="end" fill="{theme['text_faint']}" font-size="8" font-family="monospace">TYPED BACKEND • DATA • APIS</text>
    <line x1="35" y1="51" x2="815" y2="51" stroke="{theme['star_dust']}" opacity="0.5"/>
{lines}
{flow_dots}
{chr(10).join(core_nodes)}
{chr(10).join(data_nodes)}
{chr(10).join(satellite_nodes)}
    <text x="35" y="267" fill="{theme['text_faint']}" font-size="8" font-family="monospace" letter-spacing="1">CORE PATH</text>
    <line x1="96" y1="264" x2="205" y2="264" stroke="{cyan}" opacity="0.35"/>
    <text x="815" y="267" text-anchor="end" fill="{theme['text_faint']}" font-size="8" font-family="monospace">REACT • VITE • ZOD • PYTHON • PHP/LARAVEL • DOCKER</text>
    <line x1="425" y1="270" x2="425" y2="285" stroke="{cyan}" opacity="0.4"/>
  </g>
</svg>"""
