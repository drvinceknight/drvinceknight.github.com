from jinja2.loaders import FileSystemLoader
import jinja2
from latex.jinja2 import make_env
from latex import build_pdf
import yaml
import os
import glob

def read_dir(directory):
    """
    Read all yaml files in a directory
    """
    dictionaries = []
    for f in glob.glob("{}/*yml".format(directory)):
        with open(f, "r") as f:
            dictionaries.append(yaml.load(f))
    return dictionaries

def read_data(data_dir):
    kwargs = {}
    for var, directory in (("appointments", "Appointment"),
                           ("qualifications", "Qualification"),
                           ("publications", "Publication"),
                           ("student_projects", "StudentProject"),
                           ("courses", "Course"),
                           ("funds", "Funding"),
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
            d = yaml.load(f)
            pk = yaml_file[len(data_dir + "Collaborator/"):-len(".yml")]
            d["pk"] = pk
            collaborators[pk] = d


    for publication in kwargs["publications"]:
        for pos, author in enumerate(publication["authors"]):
            publication["authors"][pos] = {"pk": author, "name":
                                           collaborators[author]["name"]}
            try:
                collaborators[author]["publications"].append(publication)
            except KeyError:
                collaborators[author]["publications"] = [publication]

    kwargs["student_projects"].sort(key=lambda d: str(d["start_date"]),
                                    reverse=True)
    for project in kwargs["student_projects"]:
        project["student"] = {"pk": project["student"],
                              "name": collaborators[project["student"]]["name"]}
        try:
            collaborators[project["student"]["pk"]]["student_projects"].append(project)
        except KeyError:
            collaborators[project["student"]["pk"]]["student_projects"] = [project]

    kwargs["software_projects"].sort(key=lambda x: x["name"])
    kwargs["software_communities"].sort(key=lambda x: x["name"])
    kwargs["publications"].sort(key=lambda x: x["date"], reverse=True)
    kwargs["media"].sort(key=lambda x: x["date"], reverse=True)
    kwargs["collaborators"] = sorted(collaborators.values(),
                                     key=lambda d: d["name"])
    kwargs["awards"].sort(key=lambda x: x["date"], reverse=True)
    kwargs["roles"].sort(key=lambda x: x["start_date"], reverse=True)
    return kwargs



def build_cv(data, templates_dir, assets_dir):
    current_dir = os.path.abspath(os.path.dirname(__file__))

    env = make_env(loader=FileSystemLoader('.'))
    tpl = env.get_template("{}cv.latex".format(templates_dir))

    # Only pass str names for latex
    for publication in data["publications"]:
        publication["authors"] = [author["name"]
                                  for author in publication["authors"]]
    for project in data["student_projects"]:
        project["name"] = project["student"]["name"]

    tex = tpl.render(**data)
    # Write tex
    with open("{}vince-knight.tex".format(assets_dir), 'w') as f:
       f.write(tex)

    # Write pdf
    pdf = build_pdf(tex, texinputs=[current_dir, ''])
    pdf.save_to("{}vince-knight.pdf".format(assets_dir))


def render_template(templates_dir, template_file, template_vars):
    """
    Render a jinja2 template
    """
    templateLoader = jinja2.FileSystemLoader(searchpath=templates_dir)
    template_env = jinja2.Environment(loader=templateLoader)
    template = template_env.get_template(template_file)
    return template.render(template_vars)

def build_index(data, templates_dir):
    data["root"] = "."
    html = render_template(templates_dir=templates_dir,
                           template_file="home.html",
                           template_vars=data)
    with open("../index.html", "w") as f:
        f.write(html)

def build_collaborators(data, templates_dir):
    data["root"] = ".."
    html = render_template(templates_dir=templates_dir,
                           template_file="collaborators.html",
                           template_vars=data)
    with open("../collaborators/index.html", "w") as f:
        f.write(html)

    for collaborator in data["collaborators"]:
        html = render_template(templates_dir=templates_dir,
                               template_file="collaborator.html",
                               template_vars={"collaborator": collaborator,
                                              "root": "../.."})
        collaborator_dir = "../collaborators/{}".format(collaborator["pk"])
        try:
            os.makedirs(collaborator_dir)
        except OSError:
            pass
        with open("{}/index.html".format(collaborator_dir), "w") as f:
            f.write(html)

def build_about(data, templates_dir):
    data["root"] = ".."
    html = render_template(templates_dir=templates_dir,
                           template_file="about.html",
                           template_vars=data)
    with open("../about/index.html", "w") as f:
        f.write(html)


if __name__ == "__main__":
    data_dir = "./data/"
    assets_dir = "../assets/"
    data = read_data(data_dir=data_dir)

    build_index(data=data, templates_dir="./templates/html/")
    build_collaborators(data=data, templates_dir="./templates/html/")
    build_about(data=data, templates_dir="./templates/html/")

    build_cv(data=data, assets_dir=assets_dir,
             templates_dir="./templates/latex/")
