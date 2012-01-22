{% if datum is in_past %}
	{% set werkwoord = 'was' %}
{% elif datum is in_future %}
	{% set werkwoord = 'is' %}
{% else %}
	{% if now.hour > 20 %}
		{% set werkwoord = 'was' %}
	{% else %}
		{% set werkwoord = 'is' %}
	{% endif %}
{% endif %}

{% if datum|datestr %}
	{% set datum_str = datum|datestr %}	
{% else %}
	{% set datum_str = datum|dateformat('EEEE d MMMM yyyy') %}
{% endif %}

{% if weer.cijfer < 5 %}
<div class="alert-message error">
		<a class="close" href="#">×</a>
		<p>Het {{ werkwoord }} {{ datum_str }} <strong>slecht</strong> motorrijweer :(</p>
</div> 

{% elif weer.cijfer > 5 and weer.cijfer < 7 %}

<div class="alert-message warning">
		<a class="close" href="#">×</a>
		<p>Het {{ werkwoord }} {{ datum_str }} <strong>redelijk</strong> motorrijweer!</p>
</div> 

{% elif weer.cijfer > 6 %}

<div class="alert-message success">
		<a class="close" href="#">×</a>
		<p>Het {{ werkwoord }} {{ datum_str }} <strong>goed</goed> motorrijweer!</p>
		</div> 
{% endif %}
