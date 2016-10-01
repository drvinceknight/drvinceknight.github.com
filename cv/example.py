from jinja2.loaders import FileSystemLoader
from latex.jinja2 import make_env
from latex import build_pdf
import yaml

with open("positions.yml", "r") as f:
    positions = yaml.load(f)

env = make_env(loader=FileSystemLoader('.'))
tpl = env.get_template('doc.latex')

pdf = build_pdf(tpl.render(positions=positions))
pdf.save_to("example.pdf")
