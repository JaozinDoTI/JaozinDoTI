"""Impact proof visual: one dominant result and three supporting metrics."""

from generator.templates.cosmic_background import render as render_cosmic_background
from generator.utils import esc

WIDTH, HEIGHT = 850, 270


def render(items: list, theme: dict) -> str:
    visible = items[:4]
    if not visible:
        visible = [{"value": "—", "label": "IMPACT", "detail": "No metrics configured"}]
    primary = visible[0]
    secondary = visible[1:4]
    cyan, violet, amber = theme["synapse_cyan"], theme["dendrite_violet"], theme["axon_amber"]
    colors = [violet, cyan, amber]
    cosmic = render_cosmic_background("impact-proof", WIDTH, HEIGHT, theme, preset="card")
    metric_x = [470, 620, 760]
    metrics = []
    for index, item in enumerate(secondary):
        x = metric_x[index]
        color = colors[index]
        metrics.append(f"""    <g class="impact-reveal" style="--impact-delay:{0.35 + index * 0.14:.2f}s">
      <circle cx="{x}" cy="125" r="43" fill="none" stroke="{color}" stroke-width="0.7" stroke-dasharray="2 7" opacity="0.34" class="impact-orbit" style="transform-origin:{x}px 125px"/>
      <circle cx="{x}" cy="125" r="34" fill="{color}" opacity="0.05"/>
      <text x="{x}" y="122" text-anchor="middle" fill="{theme['text_bright']}" font-size="25" font-weight="bold" font-family="sans-serif">{esc(item['value'])}</text>
      <text x="{x}" y="143" text-anchor="middle" fill="{color}" font-size="8" font-weight="bold" font-family="monospace" letter-spacing="0.8">{esc(item['label'])}</text>
      <text x="{x}" y="183" text-anchor="middle" fill="{theme['text_faint']}" font-size="9" font-family="sans-serif">{esc(item['detail'])}</text>
    </g>""")

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">
  <defs>
{cosmic.defs}
    <radialGradient id="impact-halo"><stop offset="0%" stop-color="{cyan}" stop-opacity="0.20"/><stop offset="100%" stop-color="{cyan}" stop-opacity="0"/></radialGradient>
    <linearGradient id="impact-link" x1="0" y1="0" x2="1" y2="0"><stop stop-color="{cyan}" stop-opacity="0.65"/><stop offset="1" stop-color="{violet}" stop-opacity="0.08"/></linearGradient>
    <style>
      .impact-reveal {{ opacity:0; animation:impact-reveal .8s ease-out var(--impact-delay,0s) forwards; }}
      .impact-orbit {{ animation:impact-orbit 28s linear infinite; }}
      .impact-breathe {{ animation:impact-breathe 4.5s ease-in-out infinite; transform-box:fill-box; transform-origin:center; }}
      @keyframes impact-reveal {{ from {{ opacity:0; transform:translateY(10px); }} to {{ opacity:1; transform:translateY(0); }} }}
      @keyframes impact-orbit {{ to {{ transform:rotate(360deg); }} }}
      @keyframes impact-breathe {{ 0%,100% {{ opacity:.55; transform:scale(.96); }} 50% {{ opacity:1; transform:scale(1.04); }} }}
    </style>
  </defs>
  <rect data-svg-layer="background" width="{WIDTH}" height="{HEIGHT}" fill="{theme['nebula']}"/>
{cosmic.elements}
  <g data-svg-layer="content">
    <line x1="425" y1="0" x2="425" y2="18" stroke="{cyan}" opacity="0.45"/><circle cx="425" cy="18" r="2" fill="{cyan}"/>
    <text x="35" y="37" fill="{theme['text_faint']}" font-size="10" font-family="monospace" letter-spacing="3">PROOF OF IMPACT</text>
    <text x="815" y="37" text-anchor="end" fill="{theme['text_faint']}" font-size="8" font-family="monospace" letter-spacing="1">MEASURED RESULTS • PRODUCTION WORKFLOWS</text>
    <line x1="35" y1="52" x2="815" y2="52" stroke="{theme['star_dust']}" opacity="0.5"/>

    <g class="impact-reveal" style="--impact-delay:.12s">
      <circle cx="210" cy="139" r="104" fill="url(#impact-halo)" opacity="0.55" class="impact-breathe"/>
      <circle cx="210" cy="139" r="81" fill="none" stroke="{cyan}" stroke-width="0.8" stroke-dasharray="3 9" opacity="0.42" class="impact-orbit" style="transform-origin:210px 139px"/>
      <circle cx="210" cy="139" r="64" fill="{theme['void']}" stroke="{cyan}" stroke-width="1.2" stroke-opacity="0.30"/>
      <text x="210" y="135" text-anchor="middle" fill="{theme['text_bright']}" font-size="43" font-weight="bold" font-family="sans-serif">{esc(primary['value'])}</text>
      <text x="210" y="159" text-anchor="middle" fill="{cyan}" font-size="10" font-weight="bold" font-family="monospace" letter-spacing="1.2">{esc(primary['label'])}</text>
      <text x="210" y="180" text-anchor="middle" fill="{theme['text_dim']}" font-size="10" font-family="sans-serif">{esc(primary['detail'])}</text>
    </g>
    <path d="M295 139 C345 139 365 125 420 125" fill="none" stroke="url(#impact-link)" stroke-width="1.2" stroke-dasharray="5 7" opacity="0.65"/>
    <circle cx="330" cy="136" r="2" fill="{cyan}" opacity="0.75" class="impact-breathe"/>
{chr(10).join(metrics)}
    <rect x="414" y="210" width="401" height="30" rx="15" fill="{theme['void']}" stroke="{theme['star_dust']}"/>
    <circle cx="435" cy="225" r="3" fill="{cyan}"/>
    <text x="450" y="229" fill="{theme['text_dim']}" font-size="10" font-family="monospace">~18s AUTOMATED EXECUTION • 4,000 ROWS × 108 COLUMNS</text>
    <line x1="425" y1="252" x2="425" y2="270" stroke="{violet}" opacity="0.40"/>
  </g>
</svg>"""
