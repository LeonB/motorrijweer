{% extends "layout.tpl" %}
{% block title %}Index{% endblock %}
{% block body %}

{% set weer = weer.overdag %}

	<div class="row">
		<div class="span16">

			{% include 'blocks/message_motorrijweer.tpl' %}

			<div class="component component-big">
				<div class="module">
					<div class="module-header">
						<h3>Weergegevens voor {{ weer.now|dateformat('EEEE d MMMM yyyy') }}</h3>
						<p>Laatst geupdate: {{ weer.last_update|datetimeformat('d MMMM yyyy') }} om {{ weer.last_update|datetimeformat('HH:mm') }}</p>
					</div>

					<div class="module-body">
						{% include 'blocks/summary.tpl' %}
					</div>

					<div class="module-footer">
						{% include 'blocks/pijltjes.tpl' %}
					</div>
				</div>
			</div>

			{% include 'blocks/weerkaart.tpl' %}

			<div class="component component-big">
				<div class="module">
					<div class="module-body data-per-dagdeel">
						<div class="row">
							<div class="span16">
								{% include 'blocks/data_per_dagdeel.tpl' %}
							</div>
						</div>
					</div>
				</div>
			</div>

			<div class="component component-big">
				<div class="module">
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

	{% include 'blocks/footer.tpl' %}

{% endblock %}
