"""Recruiter-facing proof of processing, scale and quality impact."""

from generator.templates.cosmic_background import render as render_cosmic_background
from generator.utils import esc

WIDTH, HEIGHT = 850, 300


def _metric(items: list, index: int, fallback: dict) -> dict:
    return items[index] if index < len(items) else fallback


def render(items: list, theme: dict) -> str:
    volume = _metric(items, 0, {"value": "~4K", "label": "RECORDS VALIDATED", "detail": "records evaluated per run"})
    processing = _metric(items, 1, {"value": "~99.997%", "label": "PROCESSING TIME REDUCTION", "detail": "~192h → ~24s · ~28,800× faster"})
    scale = _metric(items, 2, {"value": "~24s", "label": "DATA VALIDATION", "detail": "~4K records • 108 fields • ~53 business rules"})
    quality = _metric(items, 3, {"value": "+3.03%", "label": "MORE ISSUES DETECTED", "detail": "higher analysis effectiveness"})
    cyan, violet, amber = theme["synapse_cyan"], theme["dendrite_violet"], theme["axon_amber"]
    cosmic = render_cosmic_background("impact-proof", WIDTH, HEIGHT, theme, preset="card")

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">
  <defs>
{cosmic.defs}
    <radialGradient id="value-halo"><stop stop-color="{cyan}" stop-opacity=".20"/><stop offset="1" stop-color="{cyan}" stop-opacity="0"/></radialGradient>
    <linearGradient id="processing-bar" x1="0" y1="0" x2="1" y2="0"><stop stop-color="{violet}" stop-opacity=".12"/><stop offset="1" stop-color="{cyan}" stop-opacity=".035"/></linearGradient>
    <style>
      .impact-enter {{ opacity:0; animation:impact-enter .8s ease-out var(--impact-delay,0s) forwards; }}
      .impact-breathe {{ animation:impact-breathe 5s ease-in-out infinite; transform-box:fill-box; transform-origin:center; }}
      .impact-orbit {{ animation:impact-orbit 34s linear infinite; transform-origin:188px 169px; }}
      @keyframes impact-enter {{ from {{ opacity:0; transform:translateY(9px); }} to {{ opacity:1; transform:translateY(0); }} }}
      @keyframes impact-breathe {{ 0%,100% {{ opacity:.55; transform:scale(.97); }} 50% {{ opacity:1; transform:scale(1.04); }} }}
      @keyframes impact-orbit {{ to {{ transform:rotate(360deg); }} }}
    </style>
  </defs>
  <rect data-svg-layer="background" width="{WIDTH}" height="{HEIGHT}" fill="{theme['nebula']}"/>
{cosmic.elements}
  <g data-svg-layer="content">
    <line x1="425" y1="0" x2="425" y2="17" stroke="{cyan}" opacity=".42"/>
    <text x="35" y="36" fill="{theme['text_faint']}" font-size="10" font-family="monospace" letter-spacing="3">PROOF OF IMPACT</text>
    <text x="815" y="36" text-anchor="end" fill="{theme['text_faint']}" font-size="8" font-family="monospace">SOFTWARE ENGINEERING • PERFORMANCE • DATA QUALITY</text>
    <line x1="35" y1="52" x2="815" y2="52" stroke="{theme['star_dust']}" opacity=".5"/>

    <g class="impact-enter" style="--impact-delay:.08s">
      <rect x="35" y="70" width="285" height="202" rx="16" fill="{theme['void']}" stroke="{cyan}" stroke-opacity=".32"/>
      <circle cx="188" cy="169" r="91" fill="url(#value-halo)" class="impact-breathe"/>
      <circle cx="188" cy="169" r="68" fill="none" stroke="{cyan}" stroke-width=".8" stroke-dasharray="3 9" opacity=".36" class="impact-orbit"/>
      <text x="58" y="94" fill="{cyan}" font-size="8" font-weight="bold" font-family="monospace" letter-spacing="1.2">PRODUCTION DATA VALIDATION</text>
      <text x="177" y="158" text-anchor="middle" fill="{theme['text_bright']}" font-size="39" font-weight="bold" font-family="sans-serif">{esc(volume['value'])}</text>
      <text x="177" y="183" text-anchor="middle" fill="{cyan}" font-size="9" font-weight="bold" font-family="monospace">RECORDS</text>
      <text x="177" y="199" text-anchor="middle" fill="{cyan}" font-size="9" font-weight="bold" font-family="monospace">VALIDATED</text>
      <text x="177" y="235" text-anchor="middle" fill="{theme['text_dim']}" font-size="9" font-family="sans-serif">108 fields evaluated per record</text>
      <text x="177" y="252" text-anchor="middle" fill="{theme['text_faint']}" font-size="8" font-family="monospace">APPROXIMATE VOLUME</text>
    </g>

    <g class="impact-enter" style="--impact-delay:.20s">
      <rect x="340" y="70" width="475" height="91" rx="14" fill="url(#processing-bar)" stroke="{violet}" stroke-opacity=".30"/>
      <text x="365" y="92" fill="{violet}" font-size="8" font-weight="bold" font-family="monospace" letter-spacing="1">PERFORMANCE</text>
      <text x="365" y="132" fill="{theme['text_bright']}" font-size="29" font-weight="bold" font-family="sans-serif">{esc(processing['value'])}</text>
      <text x="365" y="149" fill="{violet}" font-size="8" font-weight="bold" font-family="monospace">PROCESSING TIME REDUCTION</text>
      <line x1="535" y1="86" x2="535" y2="145" stroke="{theme['star_dust']}"/>
      <text x="560" y="111" fill="{theme['text_bright']}" font-size="17" font-weight="bold" font-family="sans-serif">~192 HOURS → ~24 SECONDS</text>
      <text x="560" y="137" fill="{cyan}" font-size="11" font-weight="bold" font-family="monospace">~28,800× FASTER THAN MANUAL REFERENCE</text>
    </g>

    <g class="impact-enter" style="--impact-delay:.32s">
      <rect x="340" y="176" width="294" height="96" rx="14" fill="{theme['void']}" stroke="{amber}" stroke-opacity=".28"/>
      <text x="365" y="199" fill="{amber}" font-size="8" font-weight="bold" font-family="monospace" letter-spacing="1">SCALE + COMPLEXITY</text>
      <text x="365" y="239" fill="{theme['text_bright']}" font-size="31" font-weight="bold" font-family="sans-serif">{esc(scale['value'])}</text>
      <text x="452" y="222" fill="{amber}" font-size="9" font-weight="bold" font-family="monospace">DATA VALIDATION</text>
      <text x="452" y="240" fill="{theme['text_dim']}" font-size="10" font-family="monospace">~4K RECORDS • 108 FIELDS</text>
      <text x="452" y="257" fill="{theme['text_dim']}" font-size="10" font-family="monospace">~53 BUSINESS RULES / ANALYSIS</text>
    </g>

    <g class="impact-enter" style="--impact-delay:.44s">
      <rect x="649" y="176" width="166" height="96" rx="14" fill="{theme['void']}" stroke="{cyan}" stroke-opacity=".28"/>
      <text x="669" y="199" fill="{cyan}" font-size="8" font-weight="bold" font-family="monospace" letter-spacing="1">ANALYSIS QUALITY</text>
      <text x="669" y="236" fill="{theme['text_bright']}" font-size="27" font-weight="bold" font-family="sans-serif">{esc(quality['value'])}</text>
      <text x="669" y="254" fill="{cyan}" font-size="7" font-weight="bold" font-family="monospace">MORE INCONSISTENCIES</text>
      <text x="669" y="265" fill="{cyan}" font-size="7" font-weight="bold" font-family="monospace">DETECTED</text>
    </g>
    <line x1="425" y1="285" x2="425" y2="300" stroke="{violet}" opacity=".42"/>
  </g>
</svg>"""
