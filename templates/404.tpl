{% extends "layout.tpl" %}
{% block title %}Page Not Found{% endblock %}
{% block body %}
  <div class="alert-message error">
	  <a class="close" href="#">×</a>
	  <p><strong>Holy guacamole!</strong> Best check yo self, you’re not looking too good.</p>
  </div> 
  <div class="row">
	  <div class="span16">
		  <div class="component component-big">
			  <div class="module">
				  <h1>Page Not Found</h1>
				  <p><a href="{{ url_for('index') }}">go somewhere nice</a></p>
			  </div>
		  </div>
	  </div>
  </div>

{% endblock %}
