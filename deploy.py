# use the template engine Jinja2 to generate HTML pages from JSON data.
# the script has 3 functions:
# 1. generate_sitemap
# 2. render html files
# 3. generate index for analytics

import os
import json
from jinja2 import Environment, FileSystemLoader
import datetime
import requests
class DeployError(Exception):
    ...

class SitemapError(Exception):
    ...

class AnalyticsError(Exception):
    ...

class GenerateError(Exception):
    ...

VERSION = "0.1.0prod"

BASEURL = "https://pleuston.org"

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

__builtins__.printf = print  # override built-in print function to add prefix

def print(*args, **kwargs):
    prompt = "[Deploy] "
    printf(prompt, *args, **kwargs)

def update_analytics_config():
    # ===== Google Analytics =====
    # GOOGLE_ANALYTICS_ID = os.getenv("GOOGLE_ANALYTICS_ID")
    ...

    # ===== Bing Analytics =====
    # BING_ANALYTICS_ID = os.getenv("BING_ANALYTICS_ID")
    ...

    # ===== Baidu Analytics =====
    BAIDU_ANALYTICS_ID = os.getenv("BAIDU_ANALYTICS_ID")
    if BAIDU_ANALYTICS_ID:
        sites = [f"https://{BASEURL}/{page}.html\n" for page in LIST_OF_PAGES]
        r = requests.post(url=f"http://data.zz.baidu.com/urls?site={BASEURL}&token={BAIDU_ANALYTICS_ID}",data="\n".join(sites))
        if r.status_code == 200:
            print("Baidu Analytics config updated")
        elif r.status_code == 400:
            data = r.json()
            if data.get("message") == "empty content":
                raise DeployError("Baidu Analytics config update failed: empty content")
            else:
                print("Error Message: " + data.get("message")) 
        else:
            ...
    print("Analytics config updated")

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
        print(f"Adding {page}.html to sitemap")
        sitemap.append(f"{BASEURL}/{page}.html")

    bodys = []
    for url in sitemap:
        bodys.append(f"<url><loc>{url}</loc><priority>{priority}</priority><changefreq>{changefreq}</changefreq></url>")

    sitemap_xml = f"""<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{"".join(bodys)}</urlset>"""
    with open(os.path.join(TARGET_FOLDER, "sitemap.xml"), 'w', encoding='utf-8') as f:
        f.write(sitemap_xml)
    return sitemap_xml

generate_html_pages()
generate_sitemap()
update_analytics_config()
exit(0)
