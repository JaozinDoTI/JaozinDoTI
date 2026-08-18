# Premium Cosmic Background Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Transform the GitHub profile SVG background into a richer, premium cosmic environment while preserving readability, deterministic output, performance, and reduced-motion accessibility.

**Architecture:** Add one reusable SVG background component under `generator/templates/` and consume it from all seven existing templates. The component owns deterministic star generation, three depth layers, subtle nebulae, rare highlights, CSS-only drift/twinkle, and reduced-motion behavior; each card selects a density profile instead of duplicating effects.

**Tech Stack:** Python 3, generated SVG, CSS keyframes embedded in SVG, pytest.

---

### Task 1: Reusable cosmic background component

**Files:**
- Create: `generator/templates/cosmic_background.py`
- Modify: `tests/test_svg_generation.py`

- [ ] Add tests asserting deterministic output, three depth layers, varied stars, rare highlights, nebulae, and a `prefers-reduced-motion` rule.
- [ ] Implement density presets for hero and cards with bounded element counts.
- [ ] Use only opacity and transform animations; avoid per-star blur filters and scripting.
- [ ] Ensure all generated IDs/classes are safe inside independent SVG images.

### Task 2: Integrate the richer hero background

**Files:**
- Modify: `generator/templates/galaxy_header.py`
- Modify: `tests/test_svg_generation.py`

- [ ] Replace the existing simple starfield/nebula layer with the shared hero preset.
- [ ] Preserve the galaxy arms, technology labels, core, project stars, typography, and current palette.
- [ ] Remove distracting shooting stars that repeatedly cross the composition.
- [ ] Keep content visually above all background layers.

### Task 3: Create continuity across all cards

**Files:**
- Modify: `generator/templates/impact_card.py`
- Modify: `generator/templates/expertise_card.py`
- Modify: `generator/templates/case_study.py`
- Modify: `generator/templates/projects_constellation.py`
- Modify: `generator/templates/tech_stack.py`
- Modify: `generator/templates/stats_card.py`
- Modify: `tests/test_svg_generation.py`

- [ ] Add the shared low-density background to every card.
- [ ] Keep stars and nebulae dimmer than text, charts, metrics, and project content.
- [ ] Preserve responsive SVG `viewBox` behavior and existing dimensions.
- [ ] Ensure animations stop under `prefers-reduced-motion`.

### Task 4: Regenerate and verify assets

**Files:**
- Modify: `assets/generated/*.svg`

- [ ] Generate all seven production assets from `config.yml` using the current cached GitHub statistics.
- [ ] Parse every output as XML and verify expected viewBox/dimensions.
- [ ] Run the test suite and inspect output sizes to avoid excessive SVG growth.
- [ ] Confirm the README still references only existing generated assets.
