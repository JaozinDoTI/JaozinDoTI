"""Signature profile hero: software engineering, data and space."""

from generator.templates.cosmic_background import render as render_cosmic_background
from generator.utils import esc

WIDTH, HEIGHT = 850, 340


def _node(x: int, y: int, label: str, color: str, delay: float, anchor: str = "middle") -> str:
    text_x = x if anchor == "middle" else x + (15 if anchor == "start" else -15)
    return f"""    <g class="hero-reveal" style="--hero-delay:{delay:.1f}s">
      <circle cx="{x}" cy="{y}" r="13" fill="{color}" opacity="0.08"/>
      <circle cx="{x}" cy="{y}" r="4" fill="{color}" opacity="0.92" class="hero-node-pulse" style="--hero-delay:{delay:.1f}s"/>
      <circle cx="{x}" cy="{y}" r="8" fill="none" stroke="{color}" stroke-width="0.6" opacity="0.35"/>
      <text x="{text_x}" y="{y + 25}" text-anchor="{anchor}" fill="{color}" font-size="9" font-weight="bold" font-family="monospace">{esc(label)}</text>
    </g>"""


def render(config: dict, theme: dict, galaxy_arms: list, projects: list) -> str:
    profile = config.get("profile", {})
    name = profile.get("name", config.get("username", "Developer"))
    tagline = profile.get("tagline", "Backend Developer | Data & Automation")
    cosmic = render_cosmic_background(config.get("username", "profile"), WIDTH, HEIGHT, theme, preset="hero")
    cyan = theme["synapse_cyan"]
    violet = theme["dendrite_violet"]
    amber = theme["axon_amber"]
    stack = config.get("technology_constellation", {})
    core = stack.get("core", ["TypeScript", "Node.js", "Fastify", "REST APIs"])
    data = stack.get("data", ["SQL", "PostgreSQL", "MySQL"])
    labels = (core + data)[:7]
    positions = [(555, 92), (680, 78), (758, 145), (733, 246), (604, 272), (522, 215), (648, 168)]
    colors = [cyan, violet, cyan, amber, violet, amber, cyan]
    nodes = [_node(x, y, labels[i], colors[i], 0.6 + i * 0.12) for i, (x, y) in enumerate(positions) if i < len(labels)]
    connections = "\n".join(
        f'    <line x1="648" y1="168" x2="{x}" y2="{y}" stroke="{colors[i]}" stroke-width="0.8" opacity="0.24" stroke-dasharray="3 6"/>'
        for i, (x, y) in enumerate(positions[:-1])
        if i < len(labels) - 1
    )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">
  <defs>
{cosmic.defs}
    <linearGradient id="hero-shade" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{theme['void']}" stop-opacity="0.97"/>
      <stop offset="58%" stop-color="{theme['void']}" stop-opacity="0.72"/>
      <stop offset="100%" stop-color="{theme['void']}" stop-opacity="0.08"/>
    </linearGradient>
    <radialGradient id="planet-surface" cx="35%" cy="30%" r="72%">
      <stop offset="0%" stop-color="{cyan}" stop-opacity="0.24"/>
      <stop offset="45%" stop-color="{violet}" stop-opacity="0.11"/>
      <stop offset="100%" stop-color="{theme['void']}" stop-opacity="0.94"/>
    </radialGradient>
    <linearGradient id="horizon-line" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{cyan}" stop-opacity="0"/>
      <stop offset="50%" stop-color="{cyan}" stop-opacity="0.8"/>
      <stop offset="100%" stop-color="{violet}" stop-opacity="0"/>
    </linearGradient>
    <filter id="hero-glow" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="9"/></filter>
    <style>
      .hero-reveal {{ opacity:0; animation:hero-reveal .9s ease-out var(--hero-delay,0s) forwards; }}
      .hero-node-pulse {{ animation:hero-node 4s ease-in-out var(--hero-delay,0s) infinite; transform-box:fill-box; transform-origin:center; }}
      .hero-orbit {{ animation:hero-orbit 34s linear infinite; transform-origin:648px 168px; }}
      .hero-orbit-reverse {{ animation:hero-orbit 48s linear infinite reverse; transform-origin:648px 168px; }}
      .hero-core {{ animation:hero-core 5s ease-in-out infinite; transform-box:fill-box; transform-origin:center; }}
      @keyframes hero-reveal {{ from {{ opacity:0; transform:translateY(8px); }} to {{ opacity:1; transform:translateY(0); }} }}
      @keyframes hero-node {{ 0%,100% {{ opacity:.55; transform:scale(.88); }} 50% {{ opacity:1; transform:scale(1.15); }} }}
      @keyframes hero-orbit {{ to {{ transform:rotate(360deg); }} }}
      @keyframes hero-core {{ 0%,100% {{ opacity:.72; transform:scale(.96); }} 50% {{ opacity:1; transform:scale(1.05); }} }}
    </style>
  </defs>
  <rect data-svg-layer="background" width="{WIDTH}" height="{HEIGHT}" rx="16" fill="{theme['void']}"/>
{cosmic.elements}
  <g data-svg-layer="content">
    <rect width="{WIDTH}" height="{HEIGHT}" rx="16" fill="url(#hero-shade)"/>
    <path d="M430 323 Q645 270 850 302" fill="none" stroke="url(#horizon-line)" stroke-width="13" opacity="0.08" filter="url(#hero-glow)"/>
    <path d="M430 323 Q645 270 850 302" fill="none" stroke="url(#horizon-line)" stroke-width="1.2" opacity="0.75"/>

    <g opacity="0.72">
      <circle cx="648" cy="168" r="100" fill="{cyan}" opacity="0.05" filter="url(#hero-glow)"/>
      <circle cx="648" cy="168" r="76" fill="url(#planet-surface)" stroke="{cyan}" stroke-width="0.8" stroke-opacity="0.35"/>
      <ellipse cx="648" cy="168" rx="126" ry="46" fill="none" stroke="{cyan}" stroke-width="0.8" stroke-dasharray="4 8" opacity="0.30" class="hero-orbit"/>
      <ellipse cx="648" cy="168" rx="102" ry="112" fill="none" stroke="{violet}" stroke-width="0.6" stroke-dasharray="3 11" opacity="0.24" class="hero-orbit-reverse"/>
      <path d="M575 168 Q648 132 721 168 Q648 204 575 168Z" fill="none" stroke="{cyan}" stroke-width="0.5" opacity="0.18"/>
      <path d="M648 92 Q615 168 648 244 Q681 168 648 92Z" fill="none" stroke="{violet}" stroke-width="0.5" opacity="0.18"/>
    </g>
{connections}
{chr(10).join(nodes)}
    <g class="hero-core">
      <circle cx="648" cy="168" r="31" fill="{cyan}" opacity="0.10" filter="url(#hero-glow)"/>
      <circle cx="648" cy="168" r="22" fill="{theme['nebula']}" stroke="{cyan}" stroke-width="1.2"/>
      <text x="648" y="165" text-anchor="middle" fill="{cyan}" font-size="11" font-weight="bold" font-family="monospace">BACKEND</text>
      <text x="648" y="180" text-anchor="middle" fill="{theme['text_dim']}" font-size="9" font-family="monospace">DATA CORE</text>
    </g>

    <g class="hero-reveal" style="--hero-delay:.08s">
      <text x="48" y="50" fill="{cyan}" font-size="10" font-weight="bold" font-family="monospace" letter-spacing="2.4">BACKEND DEVELOPER • SOFTWARE ENGINEER</text>
      <circle cx="34" cy="46" r="3" fill="{cyan}"/>
    </g>
    <g class="hero-reveal" style="--hero-delay:.18s">
      <text x="48" y="93" fill="{theme['text_bright']}" font-size="32" font-weight="bold" font-family="sans-serif">{esc(name)}</text>
      <rect x="48" y="106" width="92" height="2" rx="1" fill="{cyan}"/>
      <rect x="145" y="106" width="44" height="2" rx="1" fill="{violet}" opacity="0.75"/>
    </g>
    <g class="hero-reveal" style="--hero-delay:.3s">
      <text x="48" y="139" fill="{theme['text_dim']}" font-size="14" font-family="sans-serif">Building production systems with backend, data and automation.</text>
      <text x="48" y="160" fill="{theme['text_faint']}" font-size="11" font-family="monospace">TypeScript • Node.js • Fastify • SQL • PostgreSQL • REST APIs</text>
    </g>
    <g class="hero-reveal" style="--hero-delay:.42s">
      <rect x="48" y="190" width="146" height="29" rx="14" fill="{cyan}" opacity="0.09" stroke="{cyan}" stroke-opacity="0.32"/>
      <text x="121" y="208" text-anchor="middle" fill="{cyan}" font-size="9" font-weight="bold" font-family="monospace">PRODUCTION SYSTEMS</text>
      <rect x="204" y="190" width="138" height="29" rx="14" fill="{violet}" opacity="0.08" stroke="{violet}" stroke-opacity="0.28"/>
      <text x="273" y="208" text-anchor="middle" fill="{violet}" font-size="9" font-weight="bold" font-family="monospace">DATA-INTENSIVE</text>
      <rect x="352" y="190" width="112" height="29" rx="14" fill="{amber}" opacity="0.08" stroke="{amber}" stroke-opacity="0.28"/>
      <text x="408" y="208" text-anchor="middle" fill="{amber}" font-size="9" font-weight="bold" font-family="monospace">AUTOMATION</text>
    </g>
    <g class="hero-reveal" style="--hero-delay:.55s">
      <text x="48" y="264" fill="{theme['text_bright']}" font-size="21" font-weight="bold" font-family="sans-serif">~192h → ~24s</text>
      <text x="48" y="282" fill="{cyan}" font-size="9" font-family="monospace" letter-spacing="1.1">AUTOMATED PROCESSING</text>
      <line x1="205" y1="250" x2="205" y2="286" stroke="{theme['star_dust']}"/>
      <text x="230" y="264" fill="{theme['text_bright']}" font-size="21" font-weight="bold" font-family="sans-serif">R$ 3M+</text>
      <text x="230" y="282" fill="{violet}" font-size="8" font-family="monospace" letter-spacing="1">PROJECTED ANNUAL VALUE</text>
    </g>
    <text x="48" y="320" fill="{theme['text_faint']}" font-size="8" font-family="monospace" letter-spacing="1.5">FLORIANÓPOLIS, BRAZIL  //  SYSTEMS • DATA • AUTOMATION</text>
    <line x1="425" y1="326" x2="425" y2="340" stroke="{cyan}" opacity="0.45"/>
    <circle cx="425" cy="326" r="2" fill="{cyan}" opacity="0.8"/>
  </g>
</svg>"""
