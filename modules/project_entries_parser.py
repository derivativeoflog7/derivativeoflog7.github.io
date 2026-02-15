from json import JSONDecoder
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
        "name": "Aroma (Wii U)",
        "image_src": "/img/compatibility_badges/aroma.png",
        "link": "https://aroma.foryour.cafe/"
    },
    "cemu": {
        "name": "Cemu",
        "image_src": "https://raw.githubusercontent.com/cemu-project/Cemu/refs/heads/main/src/resource/logo_icon.png",
        "link": "https://cemu.info/"
    },
}

def parse_project_entries(path: Path, md: Markdown, logger: Logger) -> tuple[dict, ...]:
    ret = []
    jd = JSONDecoder()
    for file_path in path.glob("*.md"):
        logger.info(f"Parsing {file_path}")
        with open(file_path, "r") as file:
            html = md.convert(file.read())
            ret.append({
                "title": md.Meta["title"][0],
                "links": [{k:v for k,v in jd.decode(link).items()} for link in md.Meta.get("links", [])],
                "compatibility_badges": tuple(_COMPATIBILITY_BADGES[badge_id.strip()] for badge_id in md.Meta.get("compatibility_badges", [])),
                "html": html,
                "filename": file_path.name,
            })
    return tuple(ret)

