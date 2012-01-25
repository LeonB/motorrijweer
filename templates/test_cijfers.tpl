{% extends "layout.tpl" %}
{% block body %}
	<div class="row">
		<div class="span16">
			<div class="component component-big">
				<div class="module">
					<div class="module-header">
						<h3>Cijfers</h3>
					</div>
					<div class="module-body">
						{% for temp_i, temp in gegevens|dictsort %}
							<h2>{{temp_i}} graden &#8451;</h2>
							<table>
							{% for neerslagkans_i, neerslagkans in temp|dictsort %}

								{% if loop.index == 1 %}
									<th>windkracht&rarr;<br />neerslag per uur&darr;</th>
									{% for windkracht_i, windkracht in neerslagkans|dictsort %}
										<th>{{ loop.index0 }} <sub>({{windkracht_i }})</sub></th>
									{% endfor %}
								{% endif %}

								<tr>
									<th>{{ neerslagkans_i }}</th>
									{% for windkracht_i, windkracht in neerslagkans|dictsort %}

										{% for obj in windkracht %}
											<td class="cijfer cijfer-{{ obj.cijfer|round|int }}">{{ obj.cijfer|round(1) }}</td>
										{% endfor %}
									{% endfor %}
								</tr>
							{% endfor %}
							</table>
						{% endfor %}
					</div>

					<div class="module-body grafiek">
						<table>
								{% for temp_i, temp in gegevens|dictsort %}
								{% if temp_i == 9 %}
								{% for neerslagkans_i, neerslagkans in temp|dictsort %}

								{% if loop.index == 1 %}
								<thead>
								<tr>
								<th>1</th>
								{% for windkracht_i, windkracht in neerslagkans|dictsort %}
								<th scope="col">{{ windkracht_i }}</th>
								{% endfor %}
								</tr>
								</thead>

								<tbody>
								<tr>
								<th scope="row"></th>
								{% for windkracht_i, windkracht in neerslagkans|dictsort %}
								{% for obj in windkracht %}
								{% if loop.index == 1 %}
								<td>{{ obj.cijfer|round(1) }}</td>
								{% endif %}
								{% endfor %}
								{% endfor %}
								</tr>
								</tbody>

								{% endif %}
								{% endfor %}
								{% endif %}
								{% endfor %}
						</table>

						<table>
								{% for temp_i, temp in gegevens|dictsort %}
								{% if temp_i == 24 %}
								{% for neerslagkans_i, neerslagkans in temp|dictsort %}

								{% if loop.index == 1 %}
								<thead>
								<tr>
								<th>1</th>
								{% for windkracht_i, windkracht in neerslagkans|dictsort %}
								<th scope="col">{{ windkracht_i }}</th>
								{% endfor %}
								</tr>
								</thead>

								<tbody>
								<tr>
								<th scope="row"></th>
								{% for windkracht_i, windkracht in neerslagkans|dictsort %}
								{% for obj in windkracht %}
								{% if loop.index == 1 %}
								<td>{{ obj.cijfer|round(1) }}</td>
								{% endif %}
								{% endfor %}
								{% endfor %}
								</tr>
								</tbody>

								{% endif %}
								{% endfor %}
								{% endif %}
								{% endfor %}
						</table>
					</div>

				</div>
			</div>
		</div>
	</div>
{% endblock %}
