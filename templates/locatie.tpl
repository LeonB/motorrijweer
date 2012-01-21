{% extends "layout.tpl" %}
{% block title %}Index{% endblock %}
{% block body %}

{% set weer = weer.overdag %}

{{ weer.forecasts|count }}

	<div class="row">
		<div class="span16">

			{% include 'blocks/message_motorrijweer.tpl' %}

			<div class="component component-big">
				<div class="module">
					<div class="module-header">
						<h3>Weergegevens voor {{ weer.now|datetimeformat('EEEE d MMMM yyyy') }}</h3>
						<h3>&lt;&lt; Gisteren</h3>
						<h3>&gt;&gt; Morgen</h3>
						<p>Laatst geupdate: ikweetutnie</p>
					</div>
					<div class="module-body">
						<div class="row row_1">
							<div class="span2 cijfer">
								<h6>Cijfer</h6>
								<span class="waarde" title="Een 5! Dat is niet zooo goed!">
									{% if weer.cijfer is not none %}
									{{ weer.cijfer|round(1) }}
									{% endif %}
								</span>
							</div>
							<div class="span3 weertype">
								<!--<img src="/static/images/icons/Flat_Black/30.png" alt="Weersoort" title="Wat voor soort icoontje is dit: blalblalba uitleg" />-->
								<img src="http://icons.wxug.com/i/c/i/{{ weer.weertype }}.gif" alt="Weersoort" title="{{ weer.omschrijving }}" />
							</div>
							<div class="span3 temperatuur">
								<div class="minimumtemperatuur" title="Hier komt een uitleg over de minimumtemperatuur">
									<h6>Minimumtemperatuur</h6>
									{% if weer.minimumtemperatuur is none %}
									<span class="waarde">N/B</span>
									{% else %}
									<span class="waarde">{{ weer.minimumtemperatuur }}</span>
									<span class="eenheid celcius">&#8451;</span>
									{% endif %}
								</div>
								<div class="maximumtemperatuur" title="Hierkomt een uitleg over de maximumtemperatuur">
									<h6>Maximumtemperatuur</h6>
									{% if weer.maximumtemperatuur is none %}
									<span class="waarde">N/B</span>
									{% else %}
									<span class="waarde">{{ weer.maximumtemperatuur }}</span>
									<span class="eenheid celcius">&#8451;</span>
									{% endif %}
								</div>
							</div>
							<div class="span2 neerslag">
								<div class="neerslagkans" title="Blablabla uitleg neerslagkans">
									<h6>Neerslagkans</h6>
									{% if weer.neerslagkans is none %}
									<span class="waarde">N/B</span>
									{% else %}
									<span class="waarde">{{ (weer.neerslagkans*100)|round|int }}</span>
									<span class="eenheid percentage">%</span>
									{% endif %}
								</div>
								<div class="neerslag_in_mm" title="Blablablala neerslag in mm">
									<h6>Neerslag</h6>
									{% if weer.neerslag_in_mm is none %}
									<span class="waarde">N/B</span>
									{% else %}
									<span class="waarde">{{ weer.neerslag_in_mm|round(1) }}</span>
									<span class="eenheid milimeter">mm</span>
									{% endif %}
								</div>
							</div>
							<div class="span2">
								<div class="zonkans" title="Blablabla uitleg zonkans">
									<h6>Zonkans</h6>
									{% if weer.zonkans is none %}
									<span class="waarde">N/B</span>
									{% else %}
									<span class="waarde">{{ (weer.zonkans*100)|round|int }}</span>
									<span class="eenheid percentage">%</span>
									{% endif %}
								</div>
								<div class="bewolking" title="Blablabla uitleg bewolking">
									<h6>Bewolking</h6>
									{% if weer.bewolking is none %}
									<span class="waarde">N/B</span>
									{% else %}
									<span class="waarde">{{ (weer.bewolking*100)|round|int }}</span>
									<span class="eenheid percentage">%</span>
									{% endif %}
								</div>
							</div>
							<div class="span3 wind" title="Wat voor soort icoontje is dit: blalblalba uitleg" />
								<h6>Windkracht</h6>
								<div class="windkracht">
									{% if weer.windkracht is none %}
									<span class="waarde">N/B</span>
									{% else %}
									<span class="waarde">{{ weer.windkracht|kmh_to_beaufort }}</span>
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
								{% include 'blocks/data_per_dagdeel.tpl' %}
							</div>
						</div>
					</div>

					<div class="module-body grafiek">
						<div class="row">
							<div class="span16">
								<p>Nog een grafieK!!??!!?/</p>
								<p>Neerslag(kans), cijfer, weersoort + wind (weeronline): hoe ga ik % met getallen mixxen? Of nie?</p>

								<div id="chart"></div>

								{% include 'blocks/data_per_uur.tpl' %}

							</div>
						</div>
					</div>

					<div class="module-footer">
						<!--{{ weer.droog_tot }}-->
						<!--{{ weer.droog_om }}-->
						{% if not weer.droog_tot and not weer.droog_om %}
							<span>Het blijft de hele dag regenen :(</span>
						{% elif not weer.droog_tot %}
							<span>Het is weer droog om: {{ weer.droog_om.strftime('%H:%M') }}</span>
						{% else %}
							<span>Het is droog tot: {{ weer.droog_tot }}
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
