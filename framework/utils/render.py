from jinja2 import Template
from os.path import join


def render(template_name, folder="templates", **kwgs):
    """
    Todo add docstring
    """
    file_path = join(folder, template_name)
    with open(file_path, encoding="utf-8") as f:
        template = Template(f.read())
    return template.render(**kwgs)
