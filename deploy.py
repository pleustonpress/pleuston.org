# use the template engine Jinja2 to generate HTML pages from JSON data.
import os
import json
from jinja2 import Environment, FileSystemLoader
import datetime
import requests
class DeployError(Exception):
    ...

VERSION = "Versions/0.1.0/prod"

TEMPLATE_FOLDER = "html_templates"

TARGET_FOLDER = "artifact"

RENDER_DATA_FOLDER = "data_source"

LIST_OF_PAGES = [  # order by priority
    "index",
    "about",
    "terms",
    "community",
    "projects",
    "public"
]

overall_config = {}

def update_analytics_config():
    # GOOGLE_ANALYTICS_ID = os.getenv("GOOGLE_ANALYTICS_ID")
    # BING_ANALYTICS_ID = os.getenv("BING_ANALYTICS_ID")
    BAIDU_ANALYTICS_ID = os.getenv("BAIDU_ANALYTICS_ID")
    if BAIDU_ANALYTICS_ID:
        print("BAIDU ANALYTICS ID FOUND")
        sites = [f"https://pleuston.org/{page}.html\n" for page in LIST_OF_PAGES]
        r = requests.post(url=f"http://data.zz.baidu.com/urls?site=https://pleuston.org&token={BAIDU_ANALYTICS_ID}",data="\n".join(sites))
        print(r.text)
    print("Analytics config updated")
    ...


def generate_html_pages():

    for page in reversed(LIST_OF_PAGES):  # descending order
        with open(os.path.join(RENDER_DATA_FOLDER, page + ".template.json"), "r", encoding="utf-8") as f:
            overall_config.update(json.load(f))
            overall_config.update({"DeployData":os.getenv("DeployData",{})})
            overall_config.update({
                    "WebSiteCICD":{
                    "date":datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d %H:%M:%S"),
                    "version":VERSION,
                    "commit":os.getenv('CF_PAGES_COMMIT_SHA',"0000000000000000")[0:7],
                    "branch":os.getenv('CF_PAGES_BRANCH',"master"),
                    "author":"Pleuston",
                    "repo":f"https://github.com/pleustonpress/pleuston.org/commit/{os.getenv('CF_PAGES_COMMIT_SHA')}"
                }
            })

    env = Environment(loader=FileSystemLoader(TEMPLATE_FOLDER))
    for page in LIST_OF_PAGES:
        try:
            template = env.get_template(f'{page}.template.html')
            html_output = template.render(overall_config)
            # save result
            with open(os.path.join(TARGET_FOLDER, page + ".html"), 'w', encoding='utf-8') as f:
                f.write(html_output)
        except Exception as e:
            raise DeployError(f"Error while rendering {page}.template.html: {e}")

def generate_sitemap():
    sitemap = []
    priority = 0.5
    changefreq = "monthly"
    for page in LIST_OF_PAGES:
        sitemap.append(f"https://pleuston.org/{page}.html")

    bodys = []
    for url in sitemap:
        bodys.append(f"<url><loc>{url}</loc><priority>{priority}</priority><changefreq>{changefreq}</changefreq></url>")

    sitemap_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{"".join(bodys)}
</urlset>"""
    with open(os.path.join(TARGET_FOLDER, "sitemap.xml"), 'w', encoding='utf-8') as f:
        f.write(sitemap_xml)
    return sitemap_xml

generate_html_pages()
generate_sitemap()
update_analytics_config()
exit(0)
