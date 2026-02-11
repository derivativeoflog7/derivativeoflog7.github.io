from logging import Logger
from markdown import Markdown
from pathlib import Path

_COMPATIBILITY_BADGES = {
    "ds": {
        "name": "Nintendo DS (Lite)",
        "image_src": "/img/compatibility_badges/ds_lite.svg"
    },
    "dsi": {
        "name": "Nintendo DSi (XL)",
        "image_src": "/img/compatibility_badges/dsi.svg"
    },
    "aroma": {
        "name": "Aroma",
        "image_src": "/img/compatibility_badges/aroma.png"
    },
    "cemu": {
        "name": "Cemu",
        "image_src": "https://raw.githubusercontent.com/cemu-project/Cemu/refs/heads/main/src/resource/logo_icon.png"
    },
}

def parse_project_entries(path: Path, md: Markdown, logger: Logger) -> tuple[dict, ...]:
    ret = []
    for file_path in path.glob("*.md"):
        logger.info(f"Parsing {file_path}")
        with open(file_path, "r") as file:
            html = md.convert(file.read())
            compatibility_badge_ids = md.Meta.get("compatibility_badges", [])
            ret.append({
                "title": md.Meta["title"][0],
                "github_link": md.Meta.get("github_link", [None])[0], # Is there a better way to do this?
                "compatibility_badges": tuple(_COMPATIBILITY_BADGES[badge_id.strip()] for badge_id in compatibility_badge_ids),
                "html": html
            })
    return tuple(ret)

