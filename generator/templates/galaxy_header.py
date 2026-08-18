"""SVG template: Galaxy Header — the signature spiral galaxy banner (850x280)."""

import math

from generator.templates.cosmic_background import render as render_cosmic_background
from generator.templates.foreground_animation import render as render_foreground_animation
from generator.utils import esc, resolve_arm_colors, spiral_points

# ── Module-level constants ──
WIDTH, HEIGHT = 850, 280
CENTER_X, CENTER_Y = 425, 155
MAX_RADIUS = 220
SPIRAL_TURNS = 0.85
NUM_POINTS = 30
X_SCALE, Y_SCALE = 1.5, 0.38
START_ANGLES = [25, 150, 265]


def _build_glow_filters(galaxy_arms, arm_colors):
    """Build the star glow filters, one per arm."""
    glow_filters = []
    for i, _arm in enumerate(galaxy_arms):
        color = arm_colors[i]
        glow_filters.append(
            f'    <filter id="star-glow-{i}" x="-100%" y="-100%" width="300%" height="300%">\n'
            f'      <feGaussianBlur stdDeviation="3" result="blur"/>\n'
            f'      <feFlood flood-color="{color}" flood-opacity="0.5" result="color"/>\n'
            f'      <feComposite in="color" in2="blur" operator="in" result="glow"/>\n'
            f"      <feMerge>\n"
            f'        <feMergeNode in="glow"/>\n'
            f'        <feMergeNode in="SourceGraphic"/>\n'
            f"      </feMerge>\n"
            f"    </filter>"
        )
    return "\n".join(glow_filters)


def _points_to_path(points):
    """Build a quadratic Bezier SVG path string from a list of (x, y) points."""
    d = f"M {points[0][0]:.1f} {points[0][1]:.1f}"
    for j in range(1, len(points)):
        px, py = points[j - 1]
        x, y = points[j]
        cpx = (px + x) / 2
        cpy = (py + y) / 2
        d += f" Q {px:.1f} {py:.1f} {cpx:.1f} {cpy:.1f}"
    d += f" L {points[-1][0]:.1f} {points[-1][1]:.1f}"
    return d


def _build_spiral_arms(galaxy_arms, arm_colors, all_arm_points):
    """Build arm paths (segmented fade) and arm particles."""
    arm_paths = []
    arm_particles = []
    segment_count = 4
    opacity_steps = [0.50, 0.40, 0.30, 0.20]
    width_steps = [2.0, 1.7, 1.4, 1.1]

    for arm_idx, _arm in enumerate(galaxy_arms):
        color = arm_colors[arm_idx]
        points = all_arm_points[arm_idx]

        if len(points) < 2:
            continue

        # Split into segments (Step 4)
        pts_per_seg = len(points) // segment_count
        for seg in range(segment_count):
            start_i = seg * pts_per_seg
            end_i = min(start_i + pts_per_seg + 1, len(points))
            seg_pts = points[start_i:end_i]

            if len(seg_pts) < 2:
                continue

            seg_d = _points_to_path(seg_pts)

            op = opacity_steps[seg]
            sw = width_steps[seg]
            arm_paths.append(
                f'    <path d="{seg_d}" fill="none" stroke="{color}" '
                f'stroke-width="{sw:.1f}" opacity="{op:.2f}" stroke-linecap="round" '
                f'class="svg-pulse-opacity" style="--motion-low:{op - 0.1:.2f}; '
                f'--motion-high:{op + 0.1:.2f}; --motion-duration:8s; --motion-delay:{arm_idx}s"/>'
            )

        # Arm particles — 2 per arm (Step 7)
    return "\n".join(arm_paths), "\n".join(arm_particles)


def _build_tech_labels(galaxy_arms, arm_colors, all_arm_points, cx, cy):
    """Build tech dots, leader lines, and labels with radial placement."""
    arm_dots = []
    outer_start = 8  # Only use outer 65% of spiral (indices 8-27 of 30)

    for arm_idx, arm in enumerate(galaxy_arms):
        color = arm_colors[arm_idx]
        points = all_arm_points[arm_idx]
        items = arm.get("items", [])

        if not items:
            continue

        # Distribute items across outer portion of spiral
        available = len(points) - outer_start - 2  # leave last 2 points free
        spacing = max(1, available // max(len(items), 1))

        for i, item in enumerate(items):
            pt_idx = min(outer_start + i * spacing, len(points) - 1)
            px, py = points[pt_idx]

            # Radial direction from core (Step 3)
            dx = px - cx
            dy = py - cy
            dist = math.sqrt(dx * dx + dy * dy) or 1
            nx = dx / dist
            ny = dy / dist

            # Label position: 18px outward from dot
            label_x = px + nx * 18
            label_y = py + ny * 18

            # Dynamic text-anchor based on position
            if dx > 20:
                anchor = "start"
            elif dx < -20:
                anchor = "end"
            else:
                anchor = "middle"

            # Dot with opacity pulse animation (Step 7)
            arm_dots.append(
                f'    <circle cx="{px:.1f}" cy="{py:.1f}" r="2.5" fill="{color}" opacity="0.85" '
                f'class="svg-pulse-opacity" style="--motion-low:.85; --motion-high:1; '
                f'--motion-duration:5s; --motion-delay:{i * 0.7}s"/>'
            )

            # Leader line — dashed, subtle (Step 3)
            arm_dots.append(
                f'    <line x1="{px:.1f}" y1="{py:.1f}" x2="{label_x:.1f}" y2="{label_y:.1f}" '
                f'stroke="{color}" stroke-width="0.5" opacity="0.25" stroke-dasharray="2 2"/>'
            )

            # Label glow (blurred duplicate behind — Step 9)
            arm_dots.append(
                f'    <text x="{label_x:.1f}" y="{label_y + 3:.1f}" text-anchor="{anchor}" '
                f'fill="{color}" font-size="9" font-family="monospace" opacity="0.2" '
                f'filter="url(#label-glow)">{esc(item)}</text>'
            )

            # Main label (Step 9)
            arm_dots.append(
                f'    <text x="{label_x:.1f}" y="{label_y + 3:.1f}" text-anchor="{anchor}" '
                f'fill="{color}" font-size="9" font-family="monospace" opacity="0.85">{esc(item)}</text>'
            )

    return "\n".join(arm_dots)


def _build_project_stars(projects, galaxy_arms, arm_colors, all_arm_points):
    """Build project star circles."""
    project_stars = []
    for proj in projects[:3]:
        arm_idx = proj.get("arm", 0) % len(galaxy_arms)
        color = arm_colors[arm_idx]
        points = all_arm_points[arm_idx]

        pt_idx = min(len(points) - 3, 24)
        px, py = points[pt_idx]
        delay = f"{arm_idx * 0.8}s"

        project_stars.append(
            f'    <circle cx="{px:.1f}" cy="{py:.1f}" r="4" fill="{color}" opacity="0.6" '
            f'filter="url(#star-glow-{arm_idx})" class="svg-pulse-opacity" '
            f'style="--motion-low:.6; --motion-high:1; --motion-duration:4s; --motion-delay:{delay}"/>'
        )

    return "\n".join(project_stars)


def _build_orbital_rings(cx, cy, theme):
    """Build the orbital ring ellipses."""
    return (
        f'    <ellipse cx="{cx}" cy="{cy}" rx="55" ry="18" fill="none" '
        f'stroke="{theme["synapse_cyan"]}" stroke-width="0.6" opacity="0.15" '
        f'stroke-dasharray="4 6" class="svg-rotate" style="--motion-duration:20s"/>\n'
        f'    <ellipse cx="{cx}" cy="{cy}" rx="75" ry="24" fill="none" '
        f'stroke="{theme["dendrite_violet"]}" stroke-width="0.5" opacity="0.1" '
        f'stroke-dasharray="3 8" class="svg-counter-rotate" style="--motion-duration:30s"/>'
    )


def _build_galaxy_core(cx, cy, theme, initial):
    """Build the core layers (haze, glow, rings, solid core, initial)."""
    return (
        f"    <!-- Outer haze -->\n"
        f'    <circle cx="{cx}" cy="{cy}" r="40" fill="url(#core-haze-gradient)" opacity="0.4"/>\n'
        f"    <!-- Inner glow -->\n"
        f'    <circle cx="{cx}" cy="{cy}" r="24" fill="url(#core-inner-gradient)" opacity="0.6"/>\n'
        f"    <!-- Outer ring -->\n"
        f'    <ellipse cx="{cx}" cy="{cy}" rx="20" ry="18" fill="none" '
        f'stroke="{theme["synapse_cyan"]}" stroke-width="1.2" opacity="0.55" '
        f'stroke-dasharray="5 3" class="core-ring"/>\n'
        f"    <!-- Inner ring -->\n"
        f'    <circle cx="{cx}" cy="{cy}" r="14" fill="none" '
        f'stroke="{theme["dendrite_violet"]}" stroke-width="0.8" opacity="0.4" class="core-ring-inner"/>\n'
        f"    <!-- Solid core -->\n"
        f'    <circle cx="{cx}" cy="{cy}" r="11" fill="{theme["nebula"]}" '
        f'stroke="{theme["star_dust"]}" stroke-width="0.5"/>\n'
        f"    <!-- Bright center dot -->\n"
        f'    <circle cx="{cx}" cy="{cy}" r="3" fill="{theme["synapse_cyan"]}" '
        f'filter="url(#core-bright-glow)" opacity="0.9"/>\n'
        f"    <!-- Initial -->\n"
        f'    <text x="{cx}" y="{cy + 5}" text-anchor="middle" fill="{theme["synapse_cyan"]}" '
        f'font-size="14" font-weight="bold" font-family="monospace">{initial}</text>'
    )


def render(
    config: dict,
    theme: dict,
    galaxy_arms: list,
    projects: list,
) -> str:
    """Render the galaxy header SVG.

    Args:
        config: full profile config dict
        theme: color palette dict
        galaxy_arms: list of arm configs
        projects: list of project dicts
    """
    username = config.get("username", "user")
    profile = config.get("profile", {})
    name = profile.get("name", username)
    tagline = profile.get("tagline", "")
    philosophy = profile.get("philosophy", "")
    initial = name[0].upper() if name else "?"

    arm_colors = resolve_arm_colors(galaxy_arms, theme)

    # ── Spiral geometry (Step 2) ──
    # Generate arm points for all arms
    all_arm_points = [
        spiral_points(
            CENTER_X,
            CENTER_Y,
            START_ANGLES[arm_idx % len(START_ANGLES)],
            NUM_POINTS,
            MAX_RADIUS,
            SPIRAL_TURNS,
            X_SCALE,
            Y_SCALE,
        )
        for arm_idx in range(len(galaxy_arms))
    ]

    # ── Defs: filters, gradients, animations ──

    # Glow filters for project stars
    glow_filters_str = _build_glow_filters(galaxy_arms, arm_colors)

    # Label glow filter (Step 9)
    label_glow_filter = (
        '    <filter id="label-glow" x="-20%" y="-20%" width="140%" height="140%">\n'
        '      <feGaussianBlur stdDeviation="2" result="blur"/>\n'
        "    </filter>"
    )

    # Core glow filter
    core_glow_filter = (
        '    <filter id="core-bright-glow" x="-100%" y="-100%" width="300%" height="300%">\n'
        '      <feGaussianBlur stdDeviation="4"/>\n'
        "    </filter>"
    )

    # ── Build all layers via helper functions ──
    cosmic = render_cosmic_background(username, WIDTH, HEIGHT, theme, preset="hero")
    foreground_animation = render_foreground_animation()
    arm_paths_str, arm_particles_str = _build_spiral_arms(galaxy_arms, arm_colors, all_arm_points)
    arm_dots_str = _build_tech_labels(galaxy_arms, arm_colors, all_arm_points, CENTER_X, CENTER_Y)
    project_stars_str = _build_project_stars(projects, galaxy_arms, arm_colors, all_arm_points)
    orbital_rings = _build_orbital_rings(CENTER_X, CENTER_Y, theme)
    core = _build_galaxy_core(CENTER_X, CENTER_Y, theme, initial)

    # ── Assemble SVG ──
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">
  <defs>
{cosmic.defs}
{foreground_animation}
    <style>
      .core-ring {{
        animation: pulse-core 3s ease-in-out infinite;
        transform-origin: {CENTER_X}px {CENTER_Y}px;
      }}
      .core-ring-inner {{
        animation: pulse-core 3s ease-in-out infinite 1.5s;
        transform-origin: {CENTER_X}px {CENTER_Y}px;
      }}
      @keyframes pulse-core {{
        0%, 100% {{ opacity: 0.3; transform: scale(1); }}
        50% {{ opacity: 0.8; transform: scale(1.06); }}
      }}
    </style>

{label_glow_filter}
{core_glow_filter}

    <radialGradient id="core-haze-gradient" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="{theme['synapse_cyan']}" stop-opacity="0.5"/>
      <stop offset="50%" stop-color="{theme['dendrite_violet']}" stop-opacity="0.2"/>
      <stop offset="100%" stop-color="{theme['synapse_cyan']}" stop-opacity="0"/>
    </radialGradient>

    <radialGradient id="core-inner-gradient" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.6"/>
      <stop offset="40%" stop-color="{theme['synapse_cyan']}" stop-opacity="0.3"/>
      <stop offset="100%" stop-color="{theme['synapse_cyan']}" stop-opacity="0"/>
    </radialGradient>

{glow_filters_str}
  </defs>

  <!-- 1. Background -->
  <rect data-svg-layer="background" x="0" y="0" width="{WIDTH}" height="{HEIGHT}" rx="12" ry="12" fill="{theme['void']}"/>

  <!-- 2. Shared cosmic background -->
{cosmic.elements}
  <g data-svg-layer="content">

  <!-- 6. Spiral arm paths (segmented fade) -->
{arm_paths_str}

  <!-- 7. Arm particles -->
{arm_particles_str}

  <!-- 8. Tech dots + leader lines + labels -->
{arm_dots_str}

  <!-- 9. Project stars -->
{project_stars_str}

  <!-- 10. Orbital rings -->
{orbital_rings}

  <!-- 11. Galaxy core -->
{core}

  <!-- 12. Profile text -->
  <text x="{CENTER_X}" y="30" text-anchor="middle" fill="{theme['text_bright']}" font-size="24" font-weight="bold" font-family="sans-serif">{esc(name)}</text>
  <text x="{CENTER_X}" y="50" text-anchor="middle" fill="{theme['text_dim']}" font-size="13" font-family="sans-serif">{esc(tagline)}</text>
  <text x="{CENTER_X}" y="{HEIGHT - 12}" text-anchor="middle" fill="{theme['text_faint']}" font-size="11" font-family="monospace" font-style="italic">{esc(philosophy)}</text>
  </g>
</svg>"""
