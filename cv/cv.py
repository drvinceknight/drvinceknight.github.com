from jinja2.loaders import FileSystemLoader
from latex.jinja2 import make_env
from latex import build_pdf
import yaml
import os

# Read appointments
with open("../_data/appointments.yml", "r") as f:
    appointments = yaml.load(f)

# Read qualifications
with open("../_data/qualifications.yml", "r") as f:
    qualifications = yaml.load(f)

# Read publications
with open("../_data/publications.yml", "r") as f:
    publications = yaml.load(f)

# Read students
with open("../_data/students.yml", "r") as f:
    students = yaml.load(f)

# Read courses
with open("../_data/courses.yml", "r") as f:
    courses = yaml.load(f)

current_dir = os.path.abspath(os.path.dirname(__file__))

env = make_env(loader=FileSystemLoader('.'))
tpl = env.get_template('cv.latex')

pdf = build_pdf(tpl.render(appointments=appointments,
                           qualifications=qualifications,
                           publications=publications,
                           students=students,
                           courses=courses,
                          ),
                texinputs=[current_dir, ''])
pdf.save_to("cv.pdf")
