"""SVG template: externally understandable production case study."""

from generator.utils import esc
from generator.templates.cosmic_background import render as render_cosmic_background

WIDTH, HEIGHT = 850, 245


def render(config: dict, theme: dict) -> str:
    """Render problem, technical ownership, solution, and stack."""
    cyan = theme["synapse_cyan"]
    violet = theme["dendrite_violet"]
    amber = theme["axon_amber"]
    columns = [
        (45, cyan, config.get("problem_title", "PROBLEMA"), config.get("problem", "")),
        (315, violet, config.get("role_title", "ATUAÇÃO"), config.get("role", "")),
        (585, amber, config.get("outcome_title", "RESULTADO"), config.get("outcome", "")),
    ]
    blocks = []
    cosmic = render_cosmic_background("case-study", WIDTH, HEIGHT, theme, preset="card")

    for x, color, title, description in columns:
        blocks.append(
            f"""  <rect x="{x}" y="76" width="220" height="90" rx="9" fill="{color}" opacity="0.07" stroke="{color}" stroke-opacity="0.38"/>
  <circle cx="{x + 22}" cy="99" r="4" fill="{color}"/>
  <text x="{x + 36}" y="103" fill="{color}" font-size="9" font-weight="bold" font-family="monospace" letter-spacing="0.8">{esc(title)}</text>
  <text x="{x + 20}" y="130" fill="{theme['text_bright']}" font-size="12" font-weight="bold" font-family="sans-serif">{esc(description)}</text>
  <text x="{x + 20}" y="150" fill="{theme['text_dim']}" font-size="10" font-family="sans-serif">{_supporting_line(title)}</text>"""
        )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">
  <defs>
{cosmic.defs}
  </defs>
  <rect data-svg-layer="background" x="0.5" y="0.5" width="{WIDTH - 1}" height="{HEIGHT - 1}" rx="12" fill="{theme['nebula']}" stroke="{theme['star_dust']}"/>
{cosmic.elements}
  <g data-svg-layer="content">
  <text x="30" y="31" fill="{theme['text_faint']}" font-size="11" font-family="monospace" letter-spacing="3">{esc(config.get('title', 'CASE DE ENGENHARIA'))}</text>
  <rect x="681" y="18" width="139" height="20" rx="10" fill="{cyan}" opacity="0.10"/>
  <text x="750" y="31" text-anchor="middle" fill="{cyan}" font-size="8" font-weight="bold" font-family="monospace">{esc(config.get('status', 'PRODUÇÃO'))}</text>
  <line x1="30" y1="49" x2="820" y2="49" stroke="{theme['star_dust']}" opacity="0.35"/>
{chr(10).join(blocks)}
  <line x1="265" y1="121" x2="307" y2="121" stroke="{violet}" stroke-dasharray="4 4" opacity="0.5"/>
  <path d="M307 121 L300 117 L300 125 Z" fill="{violet}" opacity="0.7"/>
  <line x1="535" y1="121" x2="577" y2="121" stroke="{amber}" stroke-dasharray="4 4" opacity="0.5"/>
  <path d="M577 121 L570 117 L570 125 Z" fill="{amber}" opacity="0.7"/>
  <rect x="45" y="187" width="760" height="33" rx="7" fill="{theme['void']}" stroke="{theme['star_dust']}"/>
  <text x="425" y="208" text-anchor="middle" fill="{theme['text_dim']}" font-size="10" font-family="monospace" letter-spacing="0.5">{esc(config.get('stack', ''))}</text>
  </g>
</svg>"""


def _supporting_line(title: str) -> str:
    normalized = title.upper()
    if "MANUAL" in normalized or "PROBLEMA" in normalized:
        return "Regras complexas e validação manual"
    if "RESPONSABILIDADE" in normalized or "ATUAÇÃO" in normalized:
        return "Arquitetura, processamento e integrações"
    return "Menos esforço humano e mais confiabilidade"
