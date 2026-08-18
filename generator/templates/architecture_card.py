"""SVG template: planned PRISMA Web architecture."""

from generator.utils import esc

WIDTH, HEIGHT = 850, 250


def _chip(x: int, y: int, text: str, color: str, theme: dict) -> str:
    return f"""  <rect x="{x}" y="{y}" width="170" height="28" rx="6" fill="{color}" opacity="0.08" stroke="{color}" stroke-opacity="0.32"/>
  <circle cx="{x + 14}" cy="{y + 14}" r="3" fill="{color}"/>
  <text x="{x + 26}" y="{y + 18}" fill="{theme['text_dim']}" font-size="10" font-family="monospace">{esc(text)}</text>"""


def render(config: dict, theme: dict) -> str:
    """Render target architecture while clearly marking SIGRH as discovery."""
    cyan = theme["synapse_cyan"]
    violet = theme["dendrite_violet"]
    amber = theme["axon_amber"]
    chips = [
        _chip(35, 75, config.get("frontend", "React + TypeScript"), cyan, theme),
        _chip(35, 113, config.get("backend", "Node.js + Fastify"), cyan, theme),
        _chip(35, 151, config.get("database", "PostgreSQL"), cyan, theme),
        _chip(645, 75, config.get("testing", "Vitest + Playwright"), violet, theme),
        _chip(645, 113, config.get("deployment", "Docker Compose"), violet, theme),
        _chip(645, 151, config.get("strategy", "Monólito modular"), violet, theme),
    ]

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">
  <rect x="0.5" y="0.5" width="{WIDTH - 1}" height="{HEIGHT - 1}" rx="12" fill="{theme['nebula']}" stroke="{theme['star_dust']}"/>
  <text x="30" y="31" fill="{theme['text_faint']}" font-size="11" font-family="monospace" letter-spacing="3">ARQUITETURA PRISMA WEB</text>
  <text x="820" y="31" text-anchor="end" fill="{amber}" font-size="9" font-family="monospace" letter-spacing="1">PLANEJADA • MIGRAÇÃO INCREMENTAL</text>
  <line x1="30" y1="47" x2="820" y2="47" stroke="{theme['star_dust']}" opacity="0.35"/>
{chr(10).join(chips)}
  <rect x="300" y="67" width="250" height="42" rx="8" fill="{cyan}" opacity="0.10" stroke="{cyan}" stroke-opacity="0.55"/>
  <text x="425" y="93" text-anchor="middle" fill="{theme['text_bright']}" font-size="13" font-weight="bold" font-family="monospace">PRISMA CORE</text>
  <line x1="425" y1="109" x2="425" y2="126" stroke="{cyan}" opacity="0.55"/>
  <circle cx="425" cy="127" r="3" fill="{cyan}"/>
  <rect x="330" y="128" width="190" height="32" rx="6" fill="{violet}" opacity="0.08" stroke="{violet}" stroke-opacity="0.5"/>
  <text x="425" y="149" text-anchor="middle" fill="{theme['text_dim']}" font-size="11" font-family="monospace">INTEGRATION PORT</text>
  <line x1="425" y1="160" x2="425" y2="177" stroke="{violet}" opacity="0.55"/>
  <rect x="330" y="178" width="190" height="32" rx="6" fill="{amber}" opacity="0.08" stroke="{amber}" stroke-opacity="0.5"/>
  <text x="425" y="199" text-anchor="middle" fill="{theme['text_dim']}" font-size="11" font-family="monospace">SIGRH ADAPTER</text>
  <line x1="520" y1="194" x2="568" y2="194" stroke="{amber}" stroke-width="1.5" stroke-dasharray="5 5" opacity="0.65"/>
  <path d="M568 194 L561 190 L561 198 Z" fill="{amber}" opacity="0.8"/>
  <rect x="574" y="178" width="62" height="32" rx="6" fill="none" stroke="{amber}" stroke-dasharray="4 3" stroke-opacity="0.7"/>
  <text x="605" y="198" text-anchor="middle" fill="{amber}" font-size="10" font-weight="bold" font-family="monospace">SIGRH</text>
  <rect x="563" y="217" width="84" height="18" rx="9" fill="{amber}" opacity="0.12"/>
  <text x="605" y="229" text-anchor="middle" fill="{amber}" font-size="8" font-family="monospace">{esc(config.get('status', 'DISCOVERY'))}</text>
</svg>"""
