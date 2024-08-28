---
layout: default
title: Collaborators
permalink: /collaborators/
---

{% assign students = site.collaborators | where: "category", "student" %}

## 🤝 {{ site.collaborators | size }} Collaborators ({{ students | size }} students)

{% for collaborator in site.collaborators %}

- [{{ collaborator.name }}]({{ collaborator.url }}) {% if collaborator.category == "student" %} 🧑‍🎓{% endif %}

{% endfor %}
