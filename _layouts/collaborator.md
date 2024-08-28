---
layout: default
---

<h2> {{ page.name }}</h2>

{{ page.content }}

{% assign publications = site.books | concat: site.articles | where_exp:"publication", "publication.authors contains page.name" %}
{% assign number_of_publications = publications | size %}

{% if number_of_publications != 0 %}

<h3>📢 {{number_of_publications}} Publication{% if number_of_publications>1 %}s{% endif %} </h3>

<ol reversed>
{% for publication in publications %}

<li> <a href="{{publication.url}}">{{publication.title}}</a></li>

{% endfor %}

</ol>
{% endif %}

{% if page.category == "student" %}
🧑‍🎓 I worked with {{page.name}} as a {{ page.tags | array_to_sentence_string }} student.
{% endif %}
