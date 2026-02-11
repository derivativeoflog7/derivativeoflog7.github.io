from logging import Logger
from markdown import Markdown
from pathlib import Path

def parse_blogposts(path: Path, md: Markdown, logger: Logger) -> tuple[dict, ...]:
    ret = []
    for file_path in path.glob("*.md"):
        logger.info(f"Parsing {file_path}")
        with open(file_path, "r") as file:
            html = md.convert(file.read())
            ret.append({
                "title": md.Meta["title"][0],
                "date": None,
                "filename": file_path.name,
                "html": html
            })
    return tuple(ret)

