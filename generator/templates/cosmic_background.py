"""Reusable, deterministic cosmic backdrop for profile SVGs."""

from dataclasses import dataclass
import math
from numbers import Real

from generator.utils import deterministic_random


@dataclass(frozen=True)
class CosmicBackground:
    """SVG fragments that belong in ``defs`` and behind foreground content."""

    defs: str
    elements: str


_PRESETS = {
    "hero": {"counts": (34, 20, 10), "dust": 12, "glows": 3, "flashes": 2},
    "card": {"counts": (10, 6, 3), "dust": 5, "glows": 2, "flashes": 1},
}

_LAYERS = (
    ("far", 0.28, 0.70, 0.08, 0.28, 9.0, 16.0),
    ("mid", 0.48, 1.05, 0.14, 0.45, 6.5, 12.0),
    ("near", 0.78, 1.55, 0.28, 0.72, 4.5, 9.0),
)


def _safe_prefix(seed: str, preset: str) -> str:
    cleaned = "".join(char if char.isalnum() else "-" for char in seed.lower()).strip("-")
    return f"cosmic-{preset}-{cleaned or 'profile'}"


def render(seed: str, width: int, height: int, theme: dict, preset: str = "card") -> CosmicBackground:
    """Return a bounded cosmic background with deterministic coordinates.

    ``hero`` is intentionally denser than ``card``. Animation is CSS-only and
    every animated background element becomes static when reduced motion is set.
    """
    if preset not in _PRESETS:
        raise ValueError(f"Unknown cosmic background preset: {preset}")
    if (
        isinstance(width, bool)
        or isinstance(height, bool)
        or not isinstance(width, Real)
        or not isinstance(height, Real)
        or not math.isfinite(width)
        or not math.isfinite(height)
        or width < 40
        or height < 40
    ):
        raise ValueError("Cosmic background width and height must each be at least 40")

    settings = _PRESETS[preset]
    prefix = _safe_prefix(seed, preset)
    cyan = theme.get("synapse_cyan", "#00d4ff")
    violet = theme.get("dendrite_violet", "#a78bfa")
    amber = theme.get("axon_amber", "#ffb020")
    accents = (cyan, violet, amber)

    defs = f"""    <style>
      .cosmic-star {{
        animation: cosmic-twinkle ease-in-out infinite;
        transform-box: fill-box;
        transform-origin: center;
      }}
      .cosmic-drift-far {{ animation: cosmic-drift-far 34s ease-in-out infinite alternate; }}
      .cosmic-drift-mid {{ animation: cosmic-drift-mid 27s ease-in-out infinite alternate; }}
      .cosmic-drift-near {{ animation: cosmic-drift-near 21s ease-in-out infinite alternate; }}
      .cosmic-flash {{ animation: cosmic-flash 13s ease-in-out infinite; }}
      @keyframes cosmic-twinkle {{
        0%, 100% {{ opacity: var(--star-low); transform: scale(0.92); }}
        48% {{ opacity: var(--star-high); transform: scale(1.05); }}
      }}
      @keyframes cosmic-drift-far {{ from {{ transform: translate(-2px, 1px); }} to {{ transform: translate(3px, -1px); }} }}
      @keyframes cosmic-drift-mid {{ from {{ transform: translate(2px, -1px); }} to {{ transform: translate(-3px, 2px); }} }}
      @keyframes cosmic-drift-near {{ from {{ transform: translate(-1px, -2px); }} to {{ transform: translate(2px, 2px); }} }}
      @keyframes cosmic-flash {{ 0%, 88%, 100% {{ opacity: 0.08; }} 91% {{ opacity: 0.75; }} 94% {{ opacity: 0.14; }} }}
      @media (prefers-reduced-motion: reduce) {{
        svg * {{ animation: none !important; }}
      }}
    </style>
    <filter id="{prefix}-nebula-blur" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="28"/>
    </filter>
    <filter id="{prefix}-bright-glow" x="-150%" y="-150%" width="400%" height="400%">
      <feGaussianBlur stdDeviation="2.2" result="halo"/>
      <feMerge><feMergeNode in="halo"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <clipPath id="{prefix}-clip">
      <rect x="0" y="0" width="{width}" height="{height}" rx="12" ry="12"/>
    </clipPath>"""

    pieces = [
        f'  <g data-cosmic-background="{preset}" aria-hidden="true" '
        f'clip-path="url(#{prefix}-clip)">'
    ]

    glow_x = deterministic_random(f"{seed}-{preset}-glow-x", settings["glows"], 0.12 * width, 0.88 * width)
    glow_y = deterministic_random(f"{seed}-{preset}-glow-y", settings["glows"], 0.15 * height, 0.85 * height)
    glow_r = deterministic_random(
        f"{seed}-{preset}-glow-r", settings["glows"], 0.16 * min(width, height), 0.34 * min(width, height)
    )
    pieces.append('    <g class="cosmic-nebulae">')
    for index in range(settings["glows"]):
        pieces.append(
            f'      <circle cx="{glow_x[index]:.1f}" cy="{glow_y[index]:.1f}" r="{glow_r[index]:.1f}" '
            f'fill="{accents[index % len(accents)]}" opacity="{0.025 + index * 0.006:.3f}" '
            f'filter="url(#{prefix}-nebula-blur)"/>'
        )
    pieces.append("    </g>")

    dust_x = deterministic_random(f"{seed}-{preset}-dust-x", settings["dust"], 4, width - 4)
    dust_y = deterministic_random(f"{seed}-{preset}-dust-y", settings["dust"], 4, height - 4)
    dust_r = deterministic_random(f"{seed}-{preset}-dust-r", settings["dust"], 0.18, 0.42)
    pieces.append('    <g class="cosmic-dust" fill="#ffffff" opacity="0.12">')
    for index in range(settings["dust"]):
        pieces.append(
            f'      <circle cx="{dust_x[index]:.1f}" cy="{dust_y[index]:.1f}" r="{dust_r[index]:.2f}"/>'
        )
    pieces.append("    </g>")

    for layer_index, layer in enumerate(_LAYERS):
        name, r_min, r_max, o_min, o_max, dur_min, dur_max = layer
        count = settings["counts"][layer_index]
        values = {
            "x": deterministic_random(f"{seed}-{preset}-{name}-x", count, 5, width - 5),
            "y": deterministic_random(f"{seed}-{preset}-{name}-y", count, 5, height - 5),
            "r": deterministic_random(f"{seed}-{preset}-{name}-r", count, r_min, r_max),
            "o": deterministic_random(f"{seed}-{preset}-{name}-o", count, o_min, o_max),
            "d": deterministic_random(f"{seed}-{preset}-{name}-d", count, dur_min, dur_max),
            "delay": deterministic_random(f"{seed}-{preset}-{name}-delay", count, -dur_max, 0),
        }
        pieces.append(f'    <g data-cosmic-layer="{name}" class="cosmic-drift-{name}">')
        for index in range(count):
            base_opacity = values["o"][index]
            fill = accents[(index + layer_index) % 3] if index % 11 == 0 else "#ffffff"
            bright = name == "near" and index in (0, 7)
            filter_attr = f' filter="url(#{prefix}-bright-glow)"' if bright else ""
            pieces.append(
                f'      <circle class="cosmic-star cosmic-star-{name}" cx="{values["x"][index]:.1f}" '
                f'cy="{values["y"][index]:.1f}" r="{values["r"][index]:.2f}" fill="{fill}" '
                f'opacity="{base_opacity:.2f}"{filter_attr} style="--star-low:{base_opacity * 0.65:.2f}; '
                f'--star-high:{min(base_opacity * 1.35, 0.92):.2f}; animation-duration:{values["d"][index]:.1f}s; '
                f'animation-delay:{values["delay"][index]:.1f}s"/>'
            )
        pieces.append("    </g>")

    flash_x = deterministic_random(f"{seed}-{preset}-flash-x", settings["flashes"], 20, width - 20)
    flash_y = deterministic_random(f"{seed}-{preset}-flash-y", settings["flashes"], 16, height - 16)
    for index in range(settings["flashes"]):
        pieces.append(
            f'    <circle class="cosmic-flash" cx="{flash_x[index]:.1f}" cy="{flash_y[index]:.1f}" r="1.8" '
            f'fill="{accents[index % 3]}" opacity="0.08" filter="url(#{prefix}-bright-glow)" '
            f'style="animation-delay:{-(index * 4.7):.1f}s"/>'
        )
    pieces.append("  </g>")
    return CosmicBackground(defs=defs, elements="\n".join(pieces))
