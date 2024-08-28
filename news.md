---
layout: page
title: Posts
permalink: /posts/
---

{% for post in site.posts %}

- {{ post.date | date: "%b %d, %Y" }} - [{{ post.title}}]({{ post.url}}) ({{ post.content | number_of_words}} words): {{ post.excerpt | strip_html }}

{% endfor %}
