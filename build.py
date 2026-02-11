from markdown import Markdown
from modules import project_entries_parser
from pathlib import Path
from shutil import rmtree
from staticjinja import Site

STATIC_PATH = Path("./static")
OUTPUT_PATH = Path("./_site")
PROJECT_ENTRIES_PATH = Path("./project_entries")


md = Markdown(
    output_format="html",
    extensions = (
        "meta",
        "toc"
    )
)

if __name__ == "__main__":
    project_entries = project_entries_parser.parse_project_entries(PROJECT_ENTRIES_PATH, md)
    if OUTPUT_PATH.exists():
        rmtree(OUTPUT_PATH)
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
        }
    )
    site.render()

# def md_context(template):
#     markdown_content = Path(template.filename).read_text()


