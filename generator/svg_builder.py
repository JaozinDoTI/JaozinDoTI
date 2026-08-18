"""SVG Builder — orchestrator connecting config, stats, and templates."""

from generator.templates import (
    case_study,
    expertise_card,
    galaxy_header,
    impact_card,
    projects_constellation,
    stats_card,
    tech_stack,
)


class SVGBuilder:
    """Builds all SVG assets from config and GitHub data.

    Expects a config dict that has already been through validate_config(),
    which resolves theme defaults and applies missing optional fields.
    """

    def __init__(self, config: dict, stats: dict, languages: dict):
        self.config = config
        self.stats = stats
        self.languages = languages
        self.theme = config["theme"]
        self.galaxy_arms = config.get("galaxy_arms", [])
        self.projects = config.get("projects", [])

    def render_galaxy_header(self) -> str:
        return galaxy_header.render(
            config=self.config,
            theme=self.theme,
            galaxy_arms=self.galaxy_arms,
            projects=self.projects,
        )

    def render_stats_card(self) -> str:
        metrics = self.config["stats"]["metrics"]
        return stats_card.render(
            stats=self.stats,
            metrics=metrics,
            theme=self.theme,
        )

    def render_impact_card(self) -> str:
        return impact_card.render(
            items=self.config.get("impact", []),
            theme=self.theme,
        )

    def render_expertise_card(self) -> str:
        return expertise_card.render(
            config=self.config.get("technology_constellation", {}),
            theme=self.theme,
        )

    def render_case_study(self) -> str:
        return case_study.render(
            config=self.config.get("case_study", {}),
            theme=self.theme,
        )

    def render_tech_stack(self) -> str:
        lang_config = self.config.get("languages", {})
        return tech_stack.render(
            languages=self.languages,
            galaxy_arms=self.galaxy_arms,
            theme=self.theme,
            exclude=lang_config.get("exclude", []),
            max_display=lang_config.get("max_display", 8),
        )

    def render_projects_constellation(self) -> str:
        return projects_constellation.render(
            projects=self.projects,
            galaxy_arms=self.galaxy_arms,
            theme=self.theme,
        )
