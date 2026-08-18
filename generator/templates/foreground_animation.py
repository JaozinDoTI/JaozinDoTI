"""Shared CSS-only motion helpers for foreground SVG content."""


def render(reduced_motion_overrides: str = "") -> str:
    """Return foreground animation helpers with optional static-state overrides."""
    return f"""    <style>
      .svg-pulse-opacity {{ animation: svg-pulse-opacity var(--motion-duration, 4s) ease-in-out var(--motion-delay, 0s) infinite; }}
      .svg-pulse-scale {{ animation: svg-pulse-scale var(--motion-duration, 3s) ease-in-out var(--motion-delay, 0s) infinite; transform-box: fill-box; transform-origin: center; }}
      .svg-pulse-core {{ animation: svg-pulse-core var(--motion-duration, 3s) ease-in-out var(--motion-delay, 0s) infinite; transform-box: fill-box; transform-origin: center; }}
      .svg-rotate {{ animation: svg-rotate var(--motion-duration, 12s) linear var(--motion-delay, 0s) infinite; transform-box: fill-box; transform-origin: center; }}
      .svg-counter-rotate {{ animation: svg-counter-rotate var(--motion-duration, 20s) linear var(--motion-delay, 0s) infinite; transform-box: fill-box; transform-origin: center; }}
      .svg-scan-y {{ animation: svg-scan-y var(--motion-duration, 6s) linear var(--motion-delay, 0s) infinite; }}
      .svg-grow-x {{ animation: svg-grow-x var(--motion-duration, .8s) ease-out var(--motion-delay, 0s) both; transform-box: fill-box; transform-origin: left center; }}
      .svg-scan-hit {{ animation: svg-scan-hit var(--motion-duration, 8s) linear var(--motion-delay, 0s) infinite; }}
      @keyframes svg-pulse-opacity {{ 0%, 100% {{ opacity: var(--motion-low, .45); }} 50% {{ opacity: var(--motion-high, 1); }} }}
      @keyframes svg-pulse-scale {{ 0%, 100% {{ transform: scale(var(--motion-scale-low, .82)); }} 50% {{ transform: scale(var(--motion-scale-high, 1.18)); }} }}
      @keyframes svg-pulse-core {{ 0%, 100% {{ opacity: var(--motion-low, .5); transform: scale(.9); }} 50% {{ opacity: var(--motion-high, .9); transform: scale(1.1); }} }}
      @keyframes svg-rotate {{ to {{ transform: rotate(360deg); }} }}
      @keyframes svg-counter-rotate {{ from {{ transform: rotate(360deg); }} to {{ transform: rotate(0deg); }} }}
      @keyframes svg-scan-y {{ from {{ transform: translateY(0); }} to {{ transform: translateY(var(--motion-distance, 140px)); }} }}
      @keyframes svg-grow-x {{ from {{ transform: scaleX(0); }} to {{ transform: scaleX(1); }} }}
      @keyframes svg-scan-hit {{ 0%, 4%, 10%, 100% {{ opacity: .35; }} 6% {{ opacity: 1; }} }}
      @media (prefers-reduced-motion: reduce) {{
        {reduced_motion_overrides}
      }}
    </style>"""
