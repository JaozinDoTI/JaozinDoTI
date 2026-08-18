"""Tests for SVG generation (SVGBuilder + templates)."""

import re
import xml.etree.ElementTree as ET

import pytest

from generator.config import validate_config
from generator.svg_builder import SVGBuilder
from generator.templates.cosmic_background import render as render_cosmic_background


class TestCosmicBackground:
    def test_output_is_deterministic_for_the_same_seed(self, sample_config):
        theme = sample_config["theme"]
        first = render_cosmic_background("profile", 850, 280, theme, preset="hero")
        second = render_cosmic_background("profile", 850, 280, theme, preset="hero")
        assert first == second

    def test_different_seeds_produce_different_backgrounds(self, sample_config):
        theme = sample_config["theme"]
        first = render_cosmic_background("profile-a", 850, 280, theme, preset="hero")
        second = render_cosmic_background("profile-b", 850, 280, theme, preset="hero")
        assert first.elements != second.elements

    @pytest.mark.parametrize(
        "width,height",
        [(0, 280), (850, 0), (-1, 280), (39, 280), (850, 39), ("850", 280), (850, float("inf"))],
    )
    def test_rejects_dimensions_below_the_safe_minimum(self, sample_config, width, height):
        with pytest.raises(ValueError, match="at least 40"):
            render_cosmic_background("profile", width, height, sample_config["theme"])

    def test_minimum_dimensions_are_supported(self, sample_config):
        background = render_cosmic_background("small", 40, 40, sample_config["theme"])
        ET.fromstring(f'<svg xmlns="http://www.w3.org/2000/svg"><defs>{background.defs}</defs>{background.elements}</svg>')

    def test_contains_three_depth_layers_and_reduced_motion(self, sample_config):
        background = render_cosmic_background(
            "profile", 850, 280, sample_config["theme"], preset="hero"
        )
        assert 'data-cosmic-layer="far"' in background.elements
        assert 'data-cosmic-layer="mid"' in background.elements
        assert 'data-cosmic-layer="near"' in background.elements
        assert "@media (prefers-reduced-motion: reduce)" in background.defs
        assert "animation: none" in background.defs
        assert "animate, animateMotion, animateTransform" not in background.defs
        assert 'class="cosmic-flash"' in background.elements
        assert 'opacity="0.08"' in background.elements
        assert ".project-card" not in background.defs

    def test_layers_are_clipped_to_a_rounded_rectangle(self, sample_config):
        background = render_cosmic_background("profile", 850, 280, sample_config["theme"])
        assert "<clipPath" in background.defs
        assert 'rx="12"' in background.defs
        match = re.search(r'clip-path="url\(#([^)]+)\)"', background.elements)
        assert match
        assert f'id="{match.group(1)}"' in background.defs

    def test_hero_is_denser_than_bounded_card_preset(self, sample_config):
        theme = sample_config["theme"]
        hero = render_cosmic_background("profile", 850, 280, theme, preset="hero")
        card = render_cosmic_background("card", 850, 220, theme, preset="card")
        hero_count = hero.elements.count('class="cosmic-star ')
        card_count = card.elements.count('class="cosmic-star ')
        assert hero_count > card_count
        assert hero_count <= 80
        assert 12 <= card_count <= 30


class TestSVGBuilder:
    def test_init(self, svg_builder):
        assert svg_builder.config["username"] == "galaxy-dev"

    def test_render_galaxy_header_valid_svg(self, svg_builder):
        svg = svg_builder.render_galaxy_header()
        assert svg.strip().startswith("<svg")
        assert svg.strip().endswith("</svg>")

    def test_galaxy_header_contains_name(self, svg_builder):
        svg = svg_builder.render_galaxy_header()
        assert "Nyx Orion" in svg

    def test_galaxy_header_contains_animations(self, svg_builder):
        svg = svg_builder.render_galaxy_header()
        assert "@keyframes" in svg
        assert "animation:" in svg

    def test_render_stats_card_valid_svg(self, svg_builder):
        svg = svg_builder.render_stats_card()
        assert svg.strip().startswith("<svg")
        assert svg.strip().endswith("</svg>")

    def test_stats_card_contains_formatted_values(self, svg_builder):
        svg = svg_builder.render_stats_card()
        assert "1.8k" in svg  # commits=1847
        assert "342" in svg  # stars
        assert "156" in svg  # prs

    def test_render_tech_stack_valid_svg(self, svg_builder):
        svg = svg_builder.render_tech_stack()
        assert svg.strip().startswith("<svg")
        assert svg.strip().endswith("</svg>")

    def test_tech_stack_contains_language_names(self, svg_builder):
        svg = svg_builder.render_tech_stack()
        assert "Python" in svg
        assert "TypeScript" in svg

    def test_render_projects_constellation_valid_svg(self, svg_builder):
        svg = svg_builder.render_projects_constellation()
        assert svg.strip().startswith("<svg")
        assert svg.strip().endswith("</svg>")

    def test_projects_constellation_contains_repo_names(self, svg_builder):
        svg = svg_builder.render_projects_constellation()
        assert "nebula-ui" in svg
        assert "stargate-api" in svg

    def test_every_profile_svg_contains_the_shared_cosmic_background(self, svg_builder):
        for _name, svg, _dimensions in _all_profile_svgs(svg_builder):
            root = ET.fromstring(svg)
            assert 'data-cosmic-background="card"' in svg or 'data-cosmic-background="hero"' in svg
            smil_tags = {"animate", "animateMotion", "animateTransform"}
            assert not [node for node in root.iter() if _local_name(node.tag) in smil_tags]

    def test_dimensions_and_viewboxes_are_preserved(self, svg_builder):
        for _name, svg, (width, height) in _all_profile_svgs(svg_builder):
            root = ET.fromstring(svg)
            assert root.attrib["width"] == str(width)
            assert root.attrib["height"] == str(height)
            assert root.attrib["viewBox"] == f"0 0 {width} {height}"

    def test_background_layers_precede_content(self, svg_builder):
        for name, svg, _dimensions in _all_profile_svgs(svg_builder):
            background_index = svg.index('data-svg-layer="background"')
            cosmic_index = svg.index("data-cosmic-background=")
            content_index = svg.index('data-svg-layer="content"')
            assert background_index < cosmic_index < content_index, name

    def test_ids_are_unique_and_url_references_resolve(self, svg_builder):
        for name, svg, _dimensions in _all_profile_svgs(svg_builder):
            root = ET.fromstring(svg)
            ids = [node.attrib["id"] for node in root.iter() if "id" in node.attrib]
            assert len(ids) == len(set(ids)), name
            references = set(re.findall(r"url\(#([^)]+)\)", svg))
            assert references <= set(ids), (name, references - set(ids))

    def test_keyframes_only_animate_opacity_or_transform(self, svg_builder):
        allowed = {"opacity", "transform"}
        for name, svg, _dimensions in _all_profile_svgs(svg_builder):
            keyframes = re.findall(r"@keyframes\s+[\w-]+\s*\{((?:[^{}]|\{[^{}]*\})*)\}", svg)
            assert keyframes, name
            for body in keyframes:
                properties = set(re.findall(r"([\w-]+)\s*:", body))
                assert properties <= allowed, (name, properties - allowed)

    def test_reduced_motion_keeps_flashes_and_project_cards_visible(self, svg_builder):
        projects_svg = svg_builder.render_projects_constellation()
        root = ET.fromstring(projects_svg)
        flashes = [node for node in root.iter() if "cosmic-flash" in node.attrib.get("class", "")]
        project_cards = [node for node in root.iter() if "project-card" in node.attrib.get("class", "")]
        assert flashes and all(node.attrib.get("opacity") == "0.08" for node in flashes)
        assert project_cards and all(node.attrib.get("opacity") == "0" for node in project_cards)
        assert ".project-card { opacity: 1 !important; transform: none !important; }" in projects_svg


def _local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def _all_profile_svgs(svg_builder):
    return [
        ("galaxy", svg_builder.render_galaxy_header(), (850, 280)),
        ("impact", svg_builder.render_impact_card(), (850, 205)),
        ("expertise", svg_builder.render_expertise_card(), (850, 180)),
        ("case-study", svg_builder.render_case_study(), (850, 245)),
        ("projects", svg_builder.render_projects_constellation(), (850, 220)),
        ("tech-stack", svg_builder.render_tech_stack(), (850, 240)),
        ("stats", svg_builder.render_stats_card(), (850, 180)),
    ]


class TestEdgeCases:
    def test_empty_projects(self, cfg, sample_stats, sample_languages):
        cfg["projects"] = []
        config = validate_config(cfg)
        builder = SVGBuilder(config, sample_stats, sample_languages)
        svg = builder.render_projects_constellation()
        assert svg.strip().startswith("<svg")
        assert svg.strip().endswith("</svg>")

    def test_empty_languages(self, cfg, sample_stats):
        config = validate_config(cfg)
        builder = SVGBuilder(config, sample_stats, {})
        svg = builder.render_tech_stack()
        assert svg.strip().startswith("<svg")
        assert svg.strip().endswith("</svg>")

    def test_zero_stats(self, cfg, sample_languages):
        config = validate_config(cfg)
        zero_stats = {"commits": 0, "stars": 0, "prs": 0, "issues": 0, "repos": 0}
        builder = SVGBuilder(config, zero_stats, sample_languages)
        svg = builder.render_stats_card()
        assert svg.strip().startswith("<svg")
        assert svg.strip().endswith("</svg>")
