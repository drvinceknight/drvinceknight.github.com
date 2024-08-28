---
layout: default
---

<h2> {{ page.title }}</h2>

{{ page.content }}

<hr>

{% if page.comments == true %}

<div>
<script src="https://giscus.app/client.js"
        data-repo="drvinceknight/drvinceknight.github.com"
        data-repo-id="MDEwOlJlcG9zaXRvcnk2ODI1NDI2"
        data-category="General"
        data-category-id="DIC_kwDOAGgl0s4CiAHw"
        data-mapping="pathname"
        data-strict="0"
        data-reactions-enabled="1"
        data-emit-metadata="0"
        data-input-position="bottom"
        data-theme="preferred_color_scheme"
        data-lang="en"
        crossorigin="anonymous"
        async>
</script>
</div>
{% endif %}
