{% if links['link_back'] %}
	<div class="back">&lt;&lt;
	{% if links['link_back'] is instance('date') %}
		<a href="{{ links['link_back']|dateformat('dMMyyyy') }}" alt="{{ links['link_back'] }}">{{ links['link_back'] }}</a>
	{% else %}
		<a href="{{ links['link_back'] }}" alt="{{ links['link_back'] }}">{{ links['link_back'] }}</a>
	{% endif %}
	</div>
{% endif %}

{% if links['link_forward'] %}
	<div class="forward">
	{% if links['link_forward'] is instance('date') %}
		<a href="{{ links['link_forward']|dateformat('dMMyyyy') }}" alt="{{ links['link_forward'] }}">{{ links['link_forward'] }}</a>
	{% else %}
		<a href="{{ links['link_forward'] }}" alt="{{ links['link_forward'] }}">{{ links['link_forward'] }}</a>
	{% endif %}
	&gt;&gt;
	</div>
{% endif %}
