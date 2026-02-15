from datetime import date
from logging import Logger
from markdown import Markdown
from operator import itemgetter
from pathlib import Path

def parse_blogposts(path: Path, md: Markdown, logger: Logger) -> tuple[dict, ...]:
    ret = []
    for file_path in path.glob("*.md"):
        logger.info(f"Parsing {file_path}")
        with open(file_path, "r") as file:
            html = md.convert(file.read())
            ret.append({
                "title": md.Meta["title"][0],
                "date": date.strptime(md.Meta["date"][0], "%Y-%m-%d"),
                "filename": file_path.stem,
                "html": html
            })
    return tuple(sorted(ret, key=itemgetter("date"), reverse=True))

