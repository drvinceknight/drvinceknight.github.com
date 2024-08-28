---
layout: default
title: Students
permalink: /students/
---

{% assign students = site.collaborators  | where: "category", "student"  | sort:"year" | reverse %}

## 🧑‍🎓 {{ students | size }} Students

{% for student in students %}

- [{{ student.name }}]({{ student.url }})

{% endfor %}
