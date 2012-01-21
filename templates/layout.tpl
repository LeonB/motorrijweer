<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN">
<html lang="en">
<head>
	<title>{% block title %}{% endblock %} | Hoe goed is het motorrijweer?</title>

	<!-- CSS spul -->
	<link rel="stylesheet" href="/static/stylesheets/bootstrap/1.4.0/bootstrap.min.css">
	<link rel="stylesheet" href="/static/stylesheets/template.css">
	<link rel="stylesheet" href="/static/stylesheets/visualize.css">

	<!-- Javascripts -->
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js" defer="defer"></script>
	<script src="/static/javascripts/bootstrap/1.4.0/bootstrap-twipsy.js" defer="defer"></script>
	<script src="/static/javascripts/bootstrap/1.4.0/bootstrap-alerts.js" defer="defer"></script>
	<!--<script src="https://raw.github.com/filamentgroup/jQuery-Visualize/master/js/visualize.jQuery.js" defer="defer"></script>-->

	<script src="/static/javascripts/highcharts/highcharts.js" type="text/javascript" defer="defer"></script>
	<script src="/static/javascripts/highcharts/themes/skies.js" type="text/javascript" defer="defer"></script>
	<script src="/static/javascripts/site.js" type="text/javascript" defer="defer"></script>
</head>

<body>
	<div class="container">
		<div class="content">


			{% for message in get_flashed_messages() %}
				<p class=flash>{{ message }}</p>
			{% endfor %}

			{% block body %}{% endblock %}
		</div>
	</div>

</body>
</html>
