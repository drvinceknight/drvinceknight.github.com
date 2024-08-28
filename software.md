---
layout: default
title: Software
permalink: /software/
---

## 🍦 Software

{% for tool in site.software %}

- [{{ tool.title }}]({{ tool.direct_url }}): {{ tool.description }}

{% endfor %}
