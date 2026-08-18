"""Production case: from manual operations to automated software."""

from generator.templates.cosmic_background import render as render_cosmic_background
from generator.utils import esc

WIDTH, HEIGHT = 850, 270


def render(config: dict, theme: dict) -> str:
    cyan, violet, amber = theme["synapse_cyan"], theme["dendrite_violet"], theme["axon_amber"]
    cosmic = render_cosmic_background("production-case", WIDTH, HEIGHT, theme, preset="card")
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">
  <defs>
{cosmic.defs}
    <radialGradient id="engine-halo"><stop stop-color="{cyan}" stop-opacity=".20"/><stop offset="1" stop-color="{cyan}" stop-opacity="0"/></radialGradient>
    <style>
      .case-core {{ animation:case-core 5s ease-in-out infinite; transform-box:fill-box; transform-origin:center; }}
      .case-ring {{ animation:case-ring 32s linear infinite; transform-origin:425px 146px; }}
      .case-data {{ animation:case-data 3.4s ease-in-out var(--case-delay,0s) infinite; }}
      @keyframes case-core {{ 0%,100% {{ opacity:.65; transform:scale(.96); }} 50% {{ opacity:1; transform:scale(1.04); }} }}
      @keyframes case-ring {{ to {{ transform:rotate(360deg); }} }}
      @keyframes case-data {{ 0%,100% {{ opacity:.18; transform:translateX(-7px); }} 50% {{ opacity:1; transform:translateX(7px); }} }}
    </style>
  </defs>
  <rect data-svg-layer="background" width="{WIDTH}" height="{HEIGHT}" fill="{theme['nebula']}"/>
{cosmic.elements}
  <g data-svg-layer="content">
    <line x1="425" y1="0" x2="425" y2="17" stroke="{cyan}" opacity="0.4"/>
    <text x="35" y="36" fill="{theme['text_faint']}" font-size="10" font-family="monospace" letter-spacing="3">{esc(config.get('title', 'PRODUCTION CASE'))}</text>
    <rect x="670" y="20" width="145" height="21" rx="10" fill="{cyan}" opacity="0.09" stroke="{cyan}" stroke-opacity="0.28"/>
    <circle cx="686" cy="30.5" r="3" fill="{cyan}" class="case-core"/>
    <text x="744" y="34" text-anchor="middle" fill="{cyan}" font-size="8" font-weight="bold" font-family="monospace">{esc(config.get('status', 'PRODUCTION'))}</text>
    <line x1="35" y1="54" x2="815" y2="54" stroke="{theme['star_dust']}" opacity="0.5"/>

    <g>
      <text x="70" y="91" fill="{amber}" font-size="9" font-weight="bold" font-family="monospace" letter-spacing="1">{esc(config.get('problem_title', 'PROBLEM'))}</text>
      <text x="70" y="119" fill="{theme['text_bright']}" font-size="15" font-weight="bold" font-family="sans-serif">Manual analysis</text>
      <text x="70" y="140" fill="{theme['text_dim']}" font-size="11" font-family="sans-serif">High data volume</text>
      <text x="70" y="158" fill="{theme['text_dim']}" font-size="11" font-family="sans-serif">Complex business rules</text>
      <text x="70" y="176" fill="{theme['text_dim']}" font-size="11" font-family="sans-serif">Repetitive validation</text>
      <rect x="57" y="76" width="210" height="118" rx="12" fill="{amber}" opacity="0.035" stroke="{amber}" stroke-opacity="0.24"/>
    </g>

    <path d="M267 135 C310 135 325 146 353 146" fill="none" stroke="{cyan}" stroke-width="1" stroke-dasharray="4 6" opacity="0.5"/>
    <circle cx="292" cy="139" r="2.4" fill="{cyan}" class="case-data" style="--case-delay:.3s"/>
    <circle cx="323" cy="144" r="2" fill="{violet}" class="case-data" style="--case-delay:1.1s"/>

    <g class="case-core">
      <circle cx="425" cy="146" r="72" fill="url(#engine-halo)"/>
      <circle cx="425" cy="146" r="56" fill="none" stroke="{cyan}" stroke-width="0.8" stroke-dasharray="3 8" opacity="0.44" class="case-ring"/>
      <circle cx="425" cy="146" r="42" fill="{theme['void']}" stroke="{violet}" stroke-width="1" stroke-opacity="0.55"/>
      <text x="425" y="135" text-anchor="middle" fill="{cyan}" font-size="10" font-weight="bold" font-family="monospace">RULES + DATA</text>
      <text x="425" y="154" text-anchor="middle" fill="{theme['text_bright']}" font-size="13" font-weight="bold" font-family="sans-serif">PROCESSING ENGINE</text>
      <text x="425" y="173" text-anchor="middle" fill="{theme['text_faint']}" font-size="8" font-family="monospace">VALIDATE • PROCESS • TRACE</text>
    </g>

    <path d="M497 146 C530 146 548 135 583 135" fill="none" stroke="{violet}" stroke-width="1" stroke-dasharray="4 6" opacity="0.5"/>
    <circle cx="526" cy="142" r="2" fill="{violet}" class="case-data" style="--case-delay:.8s"/>
    <circle cx="557" cy="137" r="2.4" fill="{cyan}" class="case-data" style="--case-delay:1.5s"/>

    <g>
      <rect x="583" y="76" width="210" height="118" rx="12" fill="{cyan}" opacity="0.035" stroke="{cyan}" stroke-opacity="0.24"/>
      <text x="603" y="91" fill="{cyan}" font-size="9" font-weight="bold" font-family="monospace" letter-spacing="1">{esc(config.get('outcome_title', 'OUTCOME'))}</text>
      <text x="603" y="119" fill="{theme['text_bright']}" font-size="15" font-weight="bold" font-family="sans-serif">Production software</text>
      <text x="603" y="140" fill="{theme['text_dim']}" font-size="11" font-family="sans-serif">Automated workflow</text>
      <text x="603" y="158" fill="{theme['text_dim']}" font-size="11" font-family="sans-serif">Traceable execution</text>
      <text x="603" y="176" fill="{theme['text_dim']}" font-size="11" font-family="sans-serif">Consistent results</text>
    </g>

    <rect x="57" y="211" width="736" height="34" rx="17" fill="{theme['void']}" stroke="{theme['star_dust']}"/>
    <text x="77" y="232" fill="{violet}" font-size="8" font-weight="bold" font-family="monospace">TECHNICAL OWNERSHIP</text>
    <text x="220" y="232" fill="{theme['text_dim']}" font-size="9" font-family="monospace">ARCHITECTURE • BACKEND • DATA • INTEGRATIONS • AUTOMATION</text>
    <line x1="425" y1="253" x2="425" y2="270" stroke="{violet}" opacity="0.4"/>
  </g>
</svg>"""
