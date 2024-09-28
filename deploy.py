# use the template engine Jinja2 to generate HTML pages from JSON data.
import os
import json
from jinja2 import Environment, FileSystemLoader

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

for page in reversed(LIST_OF_PAGES):  # descending order
    with open(os.path.join(RENDER_DATA_FOLDER, page + ".template.json"), "r", encoding="utf-8") as f:
        overall_config.update(json.load(f))

env = Environment(loader=FileSystemLoader(TEMPLATE_FOLDER))
for page in LIST_OF_PAGES:
    template = env.get_template(f'{page}.template.html')
    html_output = template.render(overall_config)
    # save result
    with open(os.path.join(TARGET_FOLDER, page + ".html"), 'w', encoding='utf-8') as f:
        f.write(html_output)

exit(0)
