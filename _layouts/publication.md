---
layout: default
---

<h2> {{ page.title }}</h2>

<ul>
<li>Authors: {% for author in page.authors %} <a href="{{site.baseurl}}/collaborators/{{author | slugify}}.html">{{author}}</a>{% if author != page.authors.last %},{% else %}.{% endif %}{% endfor %}</li>
<li>Date: {{ page.published_date }}</li>
    {% if page.details %}
<li>Details: {% if page.direct_url %}<a href={{page.direct_url}}>{{ page.details }}</a>{% else %}{{page.details}}{% endif%}
        {% endif %}
  {% if page.preprint_direct_url %}
<li><a href={{page.preprint_direct_url}})>Preprint.</a></li>
{% endif %}
</ul>

{{ page.content }}
