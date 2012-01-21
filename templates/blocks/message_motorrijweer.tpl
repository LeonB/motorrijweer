{% if weer.cijfer < 5 %}
<div class="alert-message error">
		<a class="close" href="#">×</a>
		<p>Het is {{ datum_str }} <strong>slecht</strong> motorrijweer :(</p>
</div> 

{% elif weer.cijfer > 5 and weer.cijfer < 7 %}

<div class="alert-message warning">
		<a class="close" href="#">×</a>
		<p>Het is {{ datum_str }} <strong>redelijk</strong> motorrijweer!</p>
</div> 

{% elif weer.cijfer > 6 %}

<div class="alert-message success">
		<a class="close" href="#">×</a>
		<p>Het is {{ datum_str }} <strong>goed</goed> motorrijweer!</p>
		</div> 
		{% endif %}
