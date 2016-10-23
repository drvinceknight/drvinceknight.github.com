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

# Read grants
with open("../_data/grants.yml", "r") as f:
    grants = yaml.load(f)

# Read media
with open("../_data/media.yml", "r") as f:
    media = yaml.load(f)

# Read outreach
with open("../_data/outreach_activities.yml", "r") as f:
    outreach_activities = yaml.load(f)

# Read software projects
with open("../_data/software_projects.yml", "r") as f:
    software_projects = yaml.load(f)

# Read software communities
with open("../_data/software_communities.yml", "r") as f:
    software_communities = yaml.load(f)

# Read roles
with open("../_data/roles.yml", "r") as f:
    roles = yaml.load(f)

# Read research interests
with open("../_data/research_topics.yml", "r") as f:
    interests = yaml.load(f)

# Read awards
with open("../_data/awards.yml", "r") as f:
    awards = yaml.load(f)


current_dir = os.path.abspath(os.path.dirname(__file__))

env = make_env(loader=FileSystemLoader('.'))
tpl = env.get_template('cv.latex')

tex = tpl.render(appointments=appointments,
                 qualifications=qualifications,
                 publications=publications,
                 students=students,
                 courses=courses,
                 grants=grants,
                 media=media,
                 outreach_activities=outreach_activities,
                 software_projects=software_projects,
                 software_communities=software_communities,
                 roles=roles,
                 interests=interests,
                 awards=awards,
                 )

# Write tex
with open("vince-knight.tex", 'w') as f:
    f.write(tex)

# Write pdf
pdf = build_pdf(tex, texinputs=[current_dir, ''])
pdf.save_to("vince-knight.pdf")
