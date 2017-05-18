from jinja2.loaders import FileSystemLoader
from latex.jinja2 import make_env
from latex import build_pdf
import yaml
import os
import glob

data_dir = "../../data/"

def read_dir(directory):
    """
    Read all yaml files in a directory
    """
    dictionaries = []
    for f in glob.glob("{}/*yml".format(directory)):
        with open(f, "r") as f:
            dictionaries.append(yaml.load(f))
    return dictionaries

kwargs = {}
for var, directory in (("appointments", "Appointment"),
                       ("qualifications", "Qualification"),
                       ("publications", "Publication"),
                       ("students", "StudentProject"),
                       ("courses", "Course"),
                       ("grants", "Funding"),
                       ("outreach_activities", "Outreach"),
                       ("software_projects", "SoftwareProject"),
                       ("software_communities", "SoftwareCommunity"),
                       ("roles", "Role"),
                       ("media", "Media"),
                       ("interests", "ResearchTopic"),
                       ("awards", "Award")):
    kwargs[var] = read_dir("{}{}".format(data_dir, directory))

collaborators = {}
for yaml_file in glob.glob("{}Collaborator/*yml".format(data_dir)):
    with open(yaml_file, "r") as f:
        name = yaml.load(f)["name"]
        collaborators[yaml_file[len(data_dir + "Collaborator/"):-len(".yml")]] = name


for publication in kwargs["publications"]:
    for pos, author in enumerate(publication["authors"]):
        publication["authors"][pos] = collaborators[author]

for student in kwargs["students"]:
    student["name"] = collaborators[student["student"]]

kwargs["publications"].sort(key=lambda x: x["date"])

current_dir = os.path.abspath(os.path.dirname(__file__))

env = make_env(loader=FileSystemLoader('.'))
tpl = env.get_template('cv.latex')

tex = tpl.render(**kwargs)
# Write tex
with open("vince-knight.tex", 'w') as f:
   f.write(tex)

# Write pdf
pdf = build_pdf(tex, texinputs=[current_dir, ''])
pdf.save_to("vince-knight.pdf")
