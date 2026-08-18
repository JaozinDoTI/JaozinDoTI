"""Entry point for the Galaxy Profile README generator."""

import argparse
import copy
import json
import logging
import os
import sys

import requests
import yaml

from generator.config import ConfigError, validate_config
from generator.github_api import GitHubAPI
from generator.svg_builder import SVGBuilder
from generator.social_preview import render_social_preview
from generator.utils import DEFAULT_LIGHT_THEME

logger = logging.getLogger(__name__)

STATS_START = "<!-- stats:start -->"
STATS_END = "<!-- stats:end -->"

DEMO_STATS = {"commits": 1847, "stars": 342, "prs": 156, "issues": 89, "repos": 42}
DEMO_LANGUAGES = {
    "Python": 450000,
    "TypeScript": 380000,
    "JavaScript": 120000,
    "Go": 95000,
    "Rust": 45000,
    "Shell": 30000,
    "Dockerfile": 15000,
    "CSS": 10000,
}


def update_readme_stats(readme_path: str, stats: dict[str, int]) -> None:
    """Update the accessible Markdown summary between the managed stats markers."""
    try:
        with open(readme_path, encoding="utf-8") as file:
            content = file.read()
    except FileNotFoundError:
        return

    if STATS_START not in content or STATS_END not in content:
        return

    labels = {
        "commits": "Commits",
        "stars": "Stars recebidas",
        "prs": "Pull requests",
        "issues": "Issues",
        "repos": "Repositórios públicos",
    }
    cells = " | ".join(f"**{stats.get(key, 0)}** {label}" for key, label in labels.items())
    replacement = f"{STATS_START}\n{cells}\n{STATS_END}"
    before, remainder = content.split(STATS_START, 1)
    _, after = remainder.split(STATS_END, 1)
    with open(readme_path, "w", encoding="utf-8") as file:
        file.write(before + replacement + after)


def generate(args):
    """Generate SVGs from config (existing behavior extracted into a function)."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    demo = getattr(args, "demo", False)

    # Load config
    if demo:
        config_path = os.path.join(os.path.dirname(__file__), "..", "config.example.yml")
    else:
        config_path = os.path.join(os.path.dirname(__file__), "..", "config.yml")

    try:
        with open(config_path, encoding="utf-8") as f:
            config = yaml.safe_load(f)
    except FileNotFoundError:
        if demo:
            logger.error("config.example.yml not found.")
        else:
            logger.error("config.yml not found. Copy config.example.yml to config.yml and edit it.")
        sys.exit(1)

    try:
        config = validate_config(config)
    except ConfigError as e:
        logger.error("Invalid config: %s", e)
        sys.exit(1)

    username = config["username"]
    output_dir = os.path.join(os.path.dirname(__file__), "..", "assets", "generated")
    os.makedirs(output_dir, exist_ok=True)
    cache_path = os.path.join(output_dir, "profile-data.json")
    try:
        with open(cache_path, encoding="utf-8") as file:
            cached_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        cached_data = {}

    logger.info("Generating profile SVGs for @%s...", username)

    if demo:
        logger.info("Demo mode: using hardcoded stats and languages.")
        stats = DEMO_STATS
        languages = DEMO_LANGUAGES
    else:
        # Fetch GitHub data
        api = GitHubAPI(username)

        logger.info("Fetching stats...")
        try:
            stats = api.fetch_stats()
        except (requests.exceptions.RequestException, ValueError, KeyError) as e:
            logger.warning("Could not fetch stats (%s). Using cached data when available.", e)
            stats = cached_data.get(
                "stats", {"commits": 0, "stars": 0, "prs": 0, "issues": 0, "repos": 0}
            )

        logger.info("Fetching languages...")
        try:
            languages = api.fetch_languages()
        except (requests.exceptions.RequestException, ValueError, KeyError) as e:
            logger.warning("Could not fetch languages (%s). Using cached data when available.", e)
            languages = cached_data.get("languages", {})

    logger.info("Stats: %s", stats)
    logger.info("Languages: %d found", len(languages))

    with open(cache_path, "w", encoding="utf-8") as file:
        json.dump({"stats": stats, "languages": languages}, file, ensure_ascii=False, indent=2)

    # Build SVGs
    builder = SVGBuilder(config, stats, languages)
    light_config = copy.deepcopy(config)
    light_config["theme"] = DEFAULT_LIGHT_THEME.copy()
    light_builder = SVGBuilder(light_config, stats, languages)
    svgs = {
        "galaxy-header.svg": builder.render_galaxy_header(),
        "stats-card.svg": builder.render_stats_card(),
        "tech-stack.svg": builder.render_tech_stack(),
        "projects-constellation.svg": builder.render_projects_constellation(),
        "galaxy-header-light.svg": light_builder.render_galaxy_header(),
        "stats-card-light.svg": light_builder.render_stats_card(),
        "tech-stack-light.svg": light_builder.render_tech_stack(),
        "projects-constellation-light.svg": light_builder.render_projects_constellation(),
    }

    for filename, content in svgs.items():
        path = os.path.join(output_dir, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        logger.info("Wrote %s", path)

    social_preview_path = os.path.join(output_dir, "social-preview.png")
    render_social_preview(config, social_preview_path)
    logger.info("Wrote %s", social_preview_path)
    readme_path = os.path.join(os.path.dirname(__file__), "..", "README.md")
    update_readme_stats(readme_path, stats)
    logger.info("Updated accessible stats in %s", readme_path)
    logger.info("Done! 8 SVGs and 1 social preview generated.")


def main():
    parser = argparse.ArgumentParser(description="Generate Galaxy Profile SVGs")
    subparsers = parser.add_subparsers(dest="command")

    # Subcommand: init
    subparsers.add_parser("init", help="Interactive setup wizard to create config.yml")

    # Subcommand: generate
    gen_parser = subparsers.add_parser("generate", help="Generate SVGs from config")
    gen_parser.add_argument(
        "--demo",
        action="store_true",
        help="Generate SVGs with demo data (no API calls, uses config.example.yml)",
    )

    # Top-level --demo for backward compatibility (python -m generator.main --demo)
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Generate SVGs with demo data (no API calls, uses config.example.yml)",
    )

    args = parser.parse_args()

    if args.command == "init":
        from generator.cli_init import run_init

        run_init()
    else:
        # Default behavior: generate (supports both `generate --demo` and `--demo`)
        generate(args)


if __name__ == "__main__":
    main()
