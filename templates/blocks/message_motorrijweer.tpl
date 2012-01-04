{% if today.cijfer < 5 %}
<div class="alert-message error">
		<a class="close" href="#">×</a>
		<p>Het is vandaag <strong>slecht</strong> motorrijweer :(</p>
</div> 

{% elif today.cijfer > 5 and today.cijfer < 7 %}

<div class="alert-message warning">
		<a class="close" href="#">×</a>
		<p>Het is vandaag <strong>redelijk</strong> motorrijweer!</p>
</div> 

{% elif today.cijfer > 6 %}

<div class="alert-message success">
		<a class="close" href="#">×</a>
		<p>Het is vandaag <strong>goed</goed> motorrijweer!</p>
		</div> 
		{% endif %}
