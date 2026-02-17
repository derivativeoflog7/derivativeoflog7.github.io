import logging
import PyRSS2Gen
import sys
from datetime import date, datetime
from markdown import Markdown
from modules import blogposts_parser, project_entries_parser
from pathlib import Path
from shutil import rmtree
from staticjinja import Site

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(sys.stderr))

BASE_URL = "https://derivativeoflog7.github.io/"
STATIC_PATH = Path("./static")
OUTPUT_PATH = Path("./_site")
BLOGPOSTS_OUTPUT_PATH = OUTPUT_PATH / "blog"
BLOGPOSTS_PATH = Path("./templates/blog")
PROJECT_ENTRIES_PATH = Path("./project_entries")

md = Markdown(
    output_format="html",
    extensions = (
        "meta",
        "toc"
    )
)

def blogpost_md_context(template):
    markdown_content = Path(template.filename).read_text()
    return {
        "html": md.convert(markdown_content),
        "title": md.Meta["title"][0],
        "date": date.strptime(md.Meta["date"][0], "%Y-%m-%d"),
    }

def render_blogpost_md(site, template, **kwargs):
    out = BLOGPOSTS_OUTPUT_PATH / Path(template.name).stem / "index.html"

    # Compile and stream the result
    out.parent.mkdir(exist_ok=True, parents=True)
    site.get_template("_partials/blogpost.html").stream(**kwargs).dump(str(out), encoding="utf-8")

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
        outpath=OUTPUT_PATH,
        contexts=[(r"blog/.*\.md", blogpost_md_context)],
        rules=[(r"blog/.*\.md", render_blogpost_md)],
        env_globals={
            "project_entries": project_entries,
            "blogposts": blogposts,
        }
    )
    site.render()
    logger.info(f"Creating blog RSS feed")
    blog_rss = PyRSS2Gen.RSS2(
        title = "derivativeoflog7 - New blogposts",
        link = BASE_URL + "blog/",
        lastBuildDate = datetime.now(),
        description = "derivativeoflog7 - New blogposts",

        items = (
            PyRSS2Gen.RSSItem(
                title = post["title"],
                link = BASE_URL + blogposts_parser.blogpost_path(post),
                guid = PyRSS2Gen.Guid(BASE_URL + blogposts_parser.blogpost_path(post)),
                pubDate = datetime.combine(post["date"], datetime.min.time()).isoformat(),
            ) for post in blogposts
        )
    ).write_xml(open(OUTPUT_PATH / "blog/rss.xml", "w"))
    logger.info("Creating projects RSS feed")
    projects_rss = PyRSS2Gen.RSS2(
        title="derivativeoflog7 - New projects",
        link=BASE_URL + "projects/",
        lastBuildDate=datetime.now(),
        description="derivativeoflog7 - Nwe projects",

        items = (
            PyRSS2Gen.RSSItem(
                title = entry["title"],
                link = BASE_URL + "projects/",
                guid = entry["title"]
            ) for entry in project_entries
        )
    ).write_xml(open(OUTPUT_PATH / "projects/rss.xml", "w"))

# def md_context(template):
#     markdown_content = Path(template.filename).read_text()


