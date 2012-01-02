{% extends "layout.tpl" %}
{% block title %}Index{% endblock %}
{% block body %}

{% set today = weer.today.overdag %}

	<div class="row">
		<div class="span16">
			<div class="component component-big">
				<div class="module">
					<div class="module-header">
						<h3>Weergegevens voor {{ weer.now|datetimeformat('EEEE d MMMM yyyy') }}</h3>
						<h3>&lt;&lt; Gisteren</h3>
						<h3>&gt;&gt; Morgen</h3>
					</div>
					<div class="module-body">
						<div class="row row_1">
							<div class="span2 cijfer">
								<h6>Cijfer</h6>
								<span class="waarde" title="Een 5! Dat is niet zooo goed!">
									{% if today.cijfer is not none %}
									{{ today.cijfer|round(1) }}
									{% endif %}
								</span>
							</div>
							<div class="span3 weertype">
								<!--<img src="/static/images/icons/Flat_Black/30.png" alt="Weersoort" title="Wat voor soort icoontje is dit: blalblalba uitleg" />-->
								<img src="http://icons.wxug.com/i/c/i/{{ today.weertype }}.gif" alt="Weersoort" title="Wat voor soort icoontje is dit: blalblalba uitleg" />
							</div>
							<div class="span3 temperatuur">
								<div class="minimumtemperatuur" title="Hier komt een uitleg over de minimumtemperatuur">
									<h6>Minimumtemperatuur</h6>
									{% if today.minimumtemperatuur is none %}
									<span class="waarde">N/B</span>
									{% else %}
									<span class="waarde">{{ today.minimumtemperatuur }}</span>
									<span class="eenheid celcius">&#8451;</span>
									{% endif %}
								</div>
								<div class="maximumtemperatuur" title="Hierkomt een uitleg over de maximumtemperatuur">
									<h6>Maximumtemperatuur</h6>
									{% if today.maximumtemperatuur is none %}
									<span class="waarde">N/B</span>
									{% else %}
									<span class="waarde">{{ today.maximumtemperatuur }}</span>
									<span class="eenheid celcius">&#8451;</span>
									{% endif %}
								</div>
							</div>
							<div class="span2 neerslag">
								<div class="neerslagkans" title="Blablabla uitleg neerslagkans">
									<h6>Neerslagkans</h6>
									{% if today.neerslagkans is none %}
									<span class="waarde">N/B</span>
									{% else %}
									<span class="waarde">{{ (today.neerslagkans*100)|round|int }}</span>
									<span class="eenheid percentage">%</span>
									{% endif %}
								</div>
								<div class="neerslag_in_mm" title="Blablablala neerslag in mm">
									<h6>Neerslag</h6>
									{% if today.neerslag_in_mm is none %}
									<span class="waarde">N/B</span>
									{% else %}
									<span class="waarde">{{ today.neerslag_in_mm|round(1) }}</span>
									<span class="eenheid milimeter">mm</span>
									{% endif %}
								</div>
							</div>
							<div class="span2">
								<div class="zonkans" title="Blablabla uitleg zonkans">
									<h6>Zonkans</h6>
									{% if today.zonkans is none %}
									<span class="waarde">N/B</span>
									{% else %}
									<span class="waarde">{{ (today.zonkans*100)|round|int }}</span>
									<span class="eenheid percentage">%</span>
									{% endif %}
								</div>
								<div class="bewolking" title="Blablabla uitleg bewolking">
									<h6>Bewolking</h6>
									{% if today.bewolking is none %}
									<span class="waarde">N/B</span>
									{% else %}
									<span class="waarde">{{ (today.bewolking*100)|round|int }}</span>
									<span class="eenheid percentage">%</span>
									{% endif %}
								</div>
							</div>
							<div class="span3 wind" title="Wat voor soort icoontje is dit: blalblalba uitleg" />
								<h6>Windkracht</h6>
								<div class="windkracht">
									{% if today.windkracht is none %}
									<span class="waarde">N/B</span>
									{% else %}
									<span class="waarde">{{ today.windkracht|round|int }}</span>
									<span class="beaufort"></span>
									{% endif %}
								</div>
								<img src="/static/images/wind_direction.png" alt="Wind directie">
							</div>
						</div>
					</div>

					<div class="module-body data-per-dagdeel">
						<div class="row">
							<div class="span16">
								<table class="bordered-table zebra-striped">
									<thead>
										<tr>
											<th>Gegevens per uur</th>
											<th>Ochtend</th>
											<th>Middag</th>
											<th>Avond</th>
										</tr>
									</thead>
									<tbody>
										<tr>
											<th>Weertype</th>
											{% for dagdeel in today.dagdelen.values() %}
												<td class="weertype">
													<img src="http://icons.wxug.com/i/c/i/{{ today.weertype }}.gif" alt="Weersoort" title="Wat voor soort icoontje is dit: blalblalba uitleg" />
													<!--<img src="/static/images/icons/Flat_Black/3.png" width="32" height="32" title="En de leste voor deze regel"/>-->
												</td>
											{% endfor %}
										</tr>
										<tr>
											<th>Temperatuur</th>
											{% for dagdeel in today.dagdelen.values() %}
												<td>
													{% if dagdeel.minimumtemperatuur is none %}
													<span class="waarde">N/B</span>
													{% else %}
													<span class="waarde">{{ dagdeel.minimumtemperatuur}}</span>
													<span class="eenheid celcius">&#8451;</span>
													{% endif %}
													<span>/</span>
													{% if dagdeel.maximumtemperatuur is none %}
													<span class="waarde">N/B</span>
													{% else %}
													<span class="waarde">{{ dagdeel.maximumtemperatuur}}</span>
													<span class="eenheid celcius">&#8451;</span>
													{% endif %}
												</td>
											{% endfor %}
										</tr>
										<tr>
											<th>Kans op neerslag</th>
											{% for dagdeel in today.dagdelen.values() %}
												<td>
													{% if dagdeel.neerslagkans is none %}
													<span class="waarde">N/B</span>
													{% else %}
													<span class="waarde">{{ (dagdeel.neerslagkans*100)|round|int }}</span>
													<span class="eenheid percentage">%</span>
													{% endif %}
												</td>
											{% endfor %}
										</tr>
										<tr>
											<th>Neerslag in mm</th>
											{% for dagdeel in today.dagdelen.values() %}
												<td>
													{% if dagdeel.neerslag_in_mm is none %}
													<span class="waarde">N/B</span>
													{% else %}
													<span class="waarde">{{ dagdeel.neerslag_in_mm|round(1)}}</span>
													<span class="eenheid milimeter">mm</span>
													{% endif %}
												</td>
											{% endfor %}
										</tr>
										<tr>
											<th>Bewolking</th>
											{% for dagdeel in today.dagdelen.values() %}
												<td>
													{% if dagdeel.bewolking is none %}
													<span class="waarde">N/B</span>
													{% else %}
													<span class="waarde">{{ (dagdeel.bewolking*100)|round|int }}</span>
													<span class="eenheid percentage">%</span>
													{% endif %}
												</td>
											{% endfor %}
										</tr>
										<tr>
											<th>Kans op zon</th>
											{% for dagdeel in today.dagdelen.values() %}
												<td>
													{% if dagdeel.zonkans is none %}
													<span class="waarde">N/B</span>
													{% else %}
													<span class="waarde">{{ (dagdeel.zonkans*100)|round|int }}</span>
													<span class="eenheid percentage">%</span>
													{% endif %}
												</td>
											{% endfor %}
										</tr>
										<tr>
											<th>Windkracht</th>
											{% for dagdeel in today.dagdelen.values() %}
												<td>
													{% if dagdeel.windkracht is none %}
													<span class="waarde">N/B</span>
													{% else %}
													<span class="waarde">{{ (dagdeel.windkracht)|round }}</span>
													{% endif %}
												</td>
											{% endfor %}
										</tr>
										<tr>
											<th>Windrichting</th>
											{% for dagdeel in today.dagdelen.values() %}
												<td>
													{% if dagdeel.windkracht is none %}
													<span class="waarde">N/B</span>
													{% else %}
													<span class="waarde">{{ dagdeel.windrichting }}</span>
													{% endif %}
												</td>
											{% endfor %}
										</tr>
										<tr>
											<th>Gevoelstemperatuur</th>
											{% for dagdeel in today.dagdelen.values() %}
												<td>
													{% if dagdeel.gevoelstemperatuur is none %}
													<span class="waarde">N/B</span>
													{% else %}
													<span class="waarde">{{ dagdeel.gevoelstemperatuur }}</span>
													<span class="eenheid celcius">&#8451;</span>
													{% endif %}
												</td>
											{% endfor %}
										</tr>
										<tr>
											<th>Cijfer</th>
											{% for dagdeel in today.dagdelen.values() %}
												<td>
													{% if dagdeel.cijfer is none %}
													<span class="waarden">N/B</span>
													{% else %}
													<span class="waarde">{{ dagdeel.cijfer|round|int }}</span>
													{% endif %}
												</td>
											{% endfor %}
										</tr>
									</tbody>
								</table>
							</div>
						</div>
					</div>

					<div class="module-body grafiek">
						<div class="row">
							<div class="span16">
								<p>Nog een grafieK!!??!!?/</p>
								<p>Neerslag(kans), cijfer, weersoort + wind (weeronline): hoe ga ik % met getallen mixxen? Of nie?</p>

								<table class="bordered-table">
									<thead>
										<tr>
											<td></td>
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
										<tr>
											<th scope="row">Neerslag</th>
											{% for forecast in today.forecasts %}
											<td>{{ forecast.neerslag_in_mm }}</td>
											{% endfor %}
										</tr>

									</tbody>
								</table>
							</div>
						</div>
					</div>

					<div class="module-footer">
						<!--{{ today.droog_tot }}-->
						<!--{{ today.droog_om }}-->
						{% if not today.droog_tot and not today.droog_om %}
							<span>Het blijft de hele dag regenen :(</span>
						{% elif not today.droog_tot %}
							<span>Het is weer droog om: {{ today.droog_om.strftime('%H:%M') }}</span>
						{% else %}
							<span>Het is droog tot: {{ today.droog_tot }}
						{% endif %}
					</div>	
				</div>
			</div>
		</div>
	</div>

	<div class="row">
		<div class="span8">
			<div class="component-small component-small-1">
				<div class="module">
					<div class="module-header">
						<h3>Woensdag 13 april 2011</h3>
					</div>
					<div class="module-body">
						<p>IETS VEEL SIMPELERS?!?</p>
						<p>Iets met een kaartje!?</p>
					</div>	
					<div class="module-footer"></div>	
				</div>
			</div>
		</div>

		<div class="span8">
			<div class="component-small">
				<div class="module">
					<div class="module-header">
						<h3>Donderdag 14 april 2011</h3>
						<h3>Op dit moment!!</h3>
					</div>
					<div class="module-body">
						<p>IETS VEEL SIMPELERS!?!?</p>
					</div>	
					<div class="module-footer"></div>	
				</div>
			</div>
		</div>
	</div>

	<div class="row">
		<div class="span16">
			<div class="component-big">
				<div class="module">
					<div class="module-body">
						<a href="http://www.wunderground.com" target="_blank">
							<img src="/static/images/wundergroundLogo_4c_horz.jpg" alt="Weather underground" />
						</a>
						<img src="http://code.google.com/appengine/images/appengine-silver-120x30.gif" alt="Powered by Google App Engine" />
					</div>
				</div>
			</div>
		</div>
	</div>

{% endblock %}
