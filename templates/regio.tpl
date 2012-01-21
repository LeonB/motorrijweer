{% extends "layout.tpl" %}
{% block title %}Index{% endblock %}
{% block body %}

{% set weer = weer.overdag %}

{{ weer.forecasts|count }}
{{ weer.cijfer }}

{% endblock %}
