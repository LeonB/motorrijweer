<table class="bordered-table">
		<thead>
				<tr>
						<td></td>
						<th scope="col">06.00</th>
						<th scope="col">07.00</th>
						<th scope="col">08.00</th>
						<th scope="col">09.00</th>
						<th scope="col">10.00</th>
						<th scope="col">11.00</th>
						<th scope="col">12.00</th>
						<th scope="col">13.00</th>
						<th scope="col">14.00</th>
						<th scope="col">15.00</th>
						<th scope="col">16.00</th>
						<th scope="col">17.00</th>
						<th scope="col">18.00</th>
						<th scope="col">19.00</th>
						<th scope="col">20.00</th>
						<th scope="col">21.00</th>
						<th scope="col">22.00</th>
				</tr>
		</thead>
		<tbody>

				<tr class="weertype">
						<th scope="row">Weertype</th>
						{% for forecast in today.forecasts %}
						<td>
								{% if forecast.weertype is none %}
								<span class="waarde">N/B</span>
								{% else %}
								<img src="http://icons.wxug.com/i/c/i/{{ forecast.weertype }}.gif" alt="Weersoort" title="{{ forecast.omschrijving }}" />
								{% endif %}
						</td>
						{% endfor %}
				</tr>

				<tr class="omschrijving">
						<th scope="row">Omschrijving</th>
						{% for forecast in today.forecasts %}
						<td>
								{% if forecast.omschrijving is none %}
								<span class="waarde">N/B</span>
								{% else %}
								<span class="waarde">{{ forecast.omschrijving }}</span>
								{% endif %}
						</td>
						{% endfor %}
				</tr>

				<tr class="temperatuur">
						<th scope="row">Temperatuur</th>
						{% for forecast in today.forecasts %}
						<td>
								{% if forecast.temperatuur is none %}
								<span class="waarde">N/B</span>
								{% else %}
								<span class="waarde">{{ forecast.temperatuur }}</span>
								<span class="eenheid celcius">&#8451;</span>
								{% endif %}
						</td>
						{% endfor %}
				</tr>

				<tr class="neerslag">
						<th scope="row">Neerslag</th>
						{% for forecast in today.forecasts %}
						<td>
								{% if forecast.neerslag_in_mm is none %}
								<span class="waarde">N/B</span>
								{% else %}
								<span class="waarde">{{ forecast.neerslag_in_mm }}</span>
								<span class="eenheid mm">mm</span>
								{% endif %}
						</td>
						{% endfor %}
				</tr>

				<tr class="bewolking">
						<th scope="row">Bewolking</th>
						{% for forecast in today.forecasts %}
						<td>
								{% if forecast.bewolking is none %}
								<span class="waarde">N/B</span>
								{% else %}
								<span class="waarde">{{ (forecast.bewolking*100)|round|int }}</span>
								<span class="eenheid percentage">%</span>
								{% endif %}
						</td>
						{% endfor %}
				</tr>

				<tr class="windkracht">
						<th scope="row">Windkracht</th>
						{% for forecast in today.forecasts %}
						<td>
								{% if forecast.windkracht is none %}
								<span class="waarde">N/B</span>
								{% else %}
								<span class="waarde">{{ forecast.windkracht|kmh_to_beaufort }}</span>
								<span class="beaufort"></span>
								{% endif %}
						</td>
						{% endfor %}
				</tr>

				<tr>
						<th scope="row">Cijfer</th>
						{% for forecast in today.forecasts %}
						<td>
								{% if forecast.cijfer is none %}
								<span class="waarde">N/B</span>
								{% else %}
								<span class="waarde">{{ forecast.cijfer|round|int }}</span>
								{% endif %}
						</td>
						{% endfor %}
				</tr>

		</tbody>
</table>
