"""Featured systems presented as real products, not repository badges."""

from generator.templates.cosmic_background import render as render_cosmic_background
from generator.utils import esc, resolve_arm_colors, wrap_text

WIDTH, HEIGHT = 850, 310


def _text_lines(text: str, x: int, y: int, max_chars: int, theme: dict, size: int = 10, limit: int = 2) -> str:
    return "\n".join(
        f'      <text x="{x}" y="{y + index * 15}" fill="{theme["text_dim"]}" font-size="{size}" font-family="sans-serif">{esc(line)}</text>'
        for index, line in enumerate(wrap_text(text, max_chars)[:limit])
    )


def render(projects: list, galaxy_arms: list, theme: dict) -> str:
    cosmic = render_cosmic_background("featured-systems", WIDTH, HEIGHT, theme, preset="card")
    cyan, violet, amber = theme["synapse_cyan"], theme["dendrite_violet"], theme["axon_amber"]
    colors = resolve_arm_colors(galaxy_arms, theme) if galaxy_arms else [cyan, violet, amber]
    featured = projects[0] if projects else {"repo": "Featured system"}
    secondary = projects[1] if len(projects) > 1 else None
    featured_color = colors[featured.get("arm", 0) % len(colors)]
    featured_name = featured.get("repo", "System").split("/")[-1]

    secondary_markup = ""
    if secondary:
        secondary_color = colors[secondary.get("arm", 0) % len(colors)]
        secondary_name = secondary.get("repo", "Project").split("/")[-1]
        secondary_markup = f"""    <g class="product-enter" style="--product-delay:.35s">
      <rect x="560" y="70" width="255" height="210" rx="14" fill="{theme['void']}" stroke="{secondary_color}" stroke-opacity="0.30"/>
      <circle cx="590" cy="101" r="17" fill="{secondary_color}" opacity="0.08"/>
      <circle cx="590" cy="101" r="5" fill="{secondary_color}" class="product-pulse"/>
      <text x="620" y="99" fill="{theme['text_bright']}" font-size="16" font-weight="bold" font-family="sans-serif">{esc(secondary_name)}</text>
      <text x="620" y="115" fill="{secondary_color}" font-size="8" font-family="monospace" letter-spacing="1">COLLABORATIVE WEB SYSTEM</text>
      <text x="582" y="148" fill="{theme['text_faint']}" font-size="8" font-weight="bold" font-family="monospace">CHALLENGE</text>
{_text_lines(secondary.get('problem', secondary.get('description', '')), 582, 167, 35, theme, 10, 2)}
      <text x="582" y="206" fill="{theme['text_faint']}" font-size="8" font-weight="bold" font-family="monospace">ENGINEERING</text>
{_text_lines(secondary.get('solution', ''), 582, 225, 35, theme, 10, 2)}
      <rect x="580" y="250" width="215" height="20" rx="10" fill="{secondary_color}" opacity="0.08"/>
      <text x="687" y="263" text-anchor="middle" fill="{secondary_color}" font-size="8" font-family="monospace">{esc(secondary.get('stack', ''))}</text>
    </g>"""

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">
  <defs>
{cosmic.defs}
    <linearGradient id="featured-glow" x1="0" y1="0" x2="1" y2="1"><stop stop-color="{featured_color}" stop-opacity=".11"/><stop offset=".6" stop-color="{theme['void']}" stop-opacity=".88"/></linearGradient>
    <style>
      .product-enter {{ opacity:0; animation:product-enter .8s ease-out var(--product-delay,0s) forwards; }}
      .product-pulse {{ animation:product-pulse 4s ease-in-out infinite; transform-box:fill-box; transform-origin:center; }}
      .product-orbit {{ animation:product-orbit 36s linear infinite; transform-origin:472px 117px; }}
      @keyframes product-enter {{ from {{ opacity:0; transform:translateY(10px); }} to {{ opacity:1; transform:translateY(0); }} }}
      @keyframes product-pulse {{ 0%,100% {{ opacity:.5; transform:scale(.85); }} 50% {{ opacity:1; transform:scale(1.18); }} }}
      @keyframes product-orbit {{ to {{ transform:rotate(360deg); }} }}
    </style>
  </defs>
  <rect data-svg-layer="background" width="{WIDTH}" height="{HEIGHT}" fill="{theme['nebula']}"/>
{cosmic.elements}
  <g data-svg-layer="content">
    <line x1="425" y1="0" x2="425" y2="17" stroke="{violet}" opacity="0.4"/>
    <text x="35" y="36" fill="{theme['text_faint']}" font-size="10" font-family="monospace" letter-spacing="3">FEATURED SYSTEMS</text>
    <text x="815" y="36" text-anchor="end" fill="{theme['text_faint']}" font-size="8" font-family="monospace">PROBLEM → SOFTWARE → IMPACT</text>
    <line x1="35" y1="52" x2="815" y2="52" stroke="{theme['star_dust']}" opacity="0.5"/>

    <g class="product-enter" style="--product-delay:.12s">
      <rect x="35" y="70" width="500" height="210" rx="14" fill="url(#featured-glow)" stroke="{featured_color}" stroke-opacity="0.38"/>
      <rect x="35" y="70" width="5" height="210" rx="2" fill="{featured_color}" opacity="0.55"/>
      <text x="65" y="97" fill="{featured_color}" font-size="8" font-weight="bold" font-family="monospace" letter-spacing="1.5">FLAGSHIP • PRODUCTION AUTOMATION</text>
      <text x="65" y="130" fill="{theme['text_bright']}" font-size="25" font-weight="bold" font-family="sans-serif">{esc(featured_name)}</text>
      <text x="65" y="151" fill="{theme['text_dim']}" font-size="11" font-family="sans-serif">{esc(featured.get('description', ''))}</text>

      <text x="65" y="185" fill="{theme['text_faint']}" font-size="8" font-weight="bold" font-family="monospace">PROBLEM</text>
      <text x="65" y="204" fill="{theme['text_bright']}" font-size="11" font-family="sans-serif">{esc(featured.get('problem', ''))}</text>
      <text x="65" y="230" fill="{theme['text_faint']}" font-size="8" font-weight="bold" font-family="monospace">BUILT</text>
      <text x="65" y="249" fill="{theme['text_bright']}" font-size="11" font-family="sans-serif">{esc(featured.get('solution', ''))}</text>
      <rect x="65" y="259" width="285" height="14" rx="7" fill="{featured_color}" opacity="0.07"/>
      <text x="207" y="269" text-anchor="middle" fill="{featured_color}" font-size="7" font-family="monospace">{esc(featured.get('stack', ''))}</text>

      <circle cx="464" cy="130" r="55" fill="{featured_color}" opacity="0.06"/>
      <circle cx="464" cy="130" r="40" fill="none" stroke="{featured_color}" stroke-width="0.8" stroke-dasharray="3 8" opacity="0.40" class="product-orbit"/>
      <circle cx="464" cy="130" r="25" fill="{theme['void']}" stroke="{featured_color}" stroke-opacity="0.5"/>
      <text x="464" y="126" text-anchor="middle" fill="{theme['text_bright']}" font-size="17" font-weight="bold" font-family="sans-serif">~99.99%</text>
      <text x="464" y="143" text-anchor="middle" fill="{featured_color}" font-size="7" font-weight="bold" font-family="monospace">LESS MANUAL WORK</text>
      <path d="M365 204 C420 204 431 184 464 173" fill="none" stroke="{featured_color}" stroke-width=".8" stroke-dasharray="3 6" opacity=".35"/>
    </g>
{secondary_markup}
    <line x1="425" y1="294" x2="425" y2="310" stroke="{cyan}" opacity="0.4"/>
  </g>
</svg>"""
