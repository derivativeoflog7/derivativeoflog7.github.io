import logging
import sys
from markdown import Markdown
from modules import blogposts_parser, project_entries_parser
from pathlib import Path
from shutil import rmtree
from staticjinja import Site

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(sys.stderr))

STATIC_PATH = Path("./static")
OUTPUT_PATH = Path("./_site")
BLOGPOSTS_PATH = Path("./blogposts")
PROJECT_ENTRIES_PATH = Path("./project_entries")

md = Markdown(
    output_format="html",
    extensions = (
        "meta",
        "toc"
    )
)

if __name__ == "__main__":
    project_entries = project_entries_parser.parse_project_entries(PROJECT_ENTRIES_PATH, md, logger)
    blogposts = blogposts_parser.parse_blogposts(BLOGPOSTS_PATH, md, logger)
    if OUTPUT_PATH.exists():
        logger.info(f"Deleting existing {OUTPUT_PATH}")
        rmtree(OUTPUT_PATH)
    logger.info(f"Copying {STATIC_PATH} to {OUTPUT_PATH}")
    STATIC_PATH.mkdir(exist_ok=True)
    STATIC_PATH.copy(OUTPUT_PATH)
    site = Site.make_site(
        outpath="./_site",
        env_globals={
            # "nav_items": (
            #     {"text": "Projects", "dir": "projects"},
            #     {"text": "Blog", "dir": "blog"},
            #     {"text": "About", "dir": "about"},
            # ),
            "project_entries": project_entries,
            "blogposts": blogposts,
        }
    )
    site.render()

# def md_context(template):
#     markdown_content = Path(template.filename).read_text()


