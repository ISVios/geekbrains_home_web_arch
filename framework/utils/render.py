from jinja2 import FileSystemLoader, Environment


def render(template_name, folder="templates", **kwgs):
    env = Environment()
    env.loader = FileSystemLoader(folder)
    template = env.get_template(template_name)
    return template.render(**kwgs)
