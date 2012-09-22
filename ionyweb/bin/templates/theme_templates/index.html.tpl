{% extends 'themes/{{ theme_type }}.html' %}

{% block theme-design-css %}
    <link rel="stylesheet" type="text/css" media="screen" href="{{ STATIC_URL }}themes/{{ theme_name }}/css/screen.css" />
{% endblock %}
