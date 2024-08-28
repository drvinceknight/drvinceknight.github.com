---
layout: default
---

## [Latest post]({{site.baseurl}}/posts/):

{% assign latest_post = site.posts.first %}

{{latest_post.date | date: "%b %d, %Y" }} - [{{latest_post.title}}]({{latest_post.url}}) ({{ latest_post.content | number_of_words}} words): {{latest_post.excerpt | strip_html }}

---

## 🛹 [Teaching](teaching/)

{% for class in site.courses %}

{% if class.current %}
{% if class.direct_url %}

- [{{ class.title }}]({{ class.direct_url }})
  {% else %}
- [{{ class.title }}]({{ class.url }})
  {% endif %}
  {% endif %}

{% endfor %}

---

## 🍦 Software

{% for tool in site.software %}

- [{{ tool.title }}]({{ tool.direct_url }}): {{ tool.description }}

{% endfor %}

---

## 📢 Publications

### 📚 Books

{% for book in site.books %}

- {{ book.published_date }}: [{{ book.title }}]({{ book.url }}). {{ book.details }}.
  {% for author in book.authors %} [{{author}}](collaborators/{{author | slugify}}.html){% if author != book.authors.last %},{% else %}.{% endif %}{% endfor %}
  {% endfor %}

### 📝 {{ site.articles | size }} Articles

{% assign articles = site.articles | sort: "published_date" | reverse %}
{% for article in articles %}

- {{ article.published_date }}: [{{ article.title }}]({{ article.url }}). {% if article.direct_url %}[{{ article.details }}]({{article.direct_url}}){% else %}{{article.details}}{% endif%}.
  {% for author in article.authors %} [{{author}}](collaborators/{{author | slugify}}.html){% if author != article.authors.last %},{% else %}.{% endif %}{% endfor %}
  {% if article.preprint_direct_url %}**[Preprint]({{article.preprint_direct_url}}).**{% endif %}
  {% endfor %}
