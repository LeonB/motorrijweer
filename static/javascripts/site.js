//@TODO: assen van de grafieken vastzetten
jQuery(document).ready(function () {
	"use strict";

	jQuery('.cijfer .waarde').tooltip({
		placement: 'bottom',
		delay: {
			show: 1000,
			hide: 10
		},
		html: true
	});

	jQuery('.weertype img').tooltip({
		placement: 'bottom',
		delay: {
			show: 1000,
			hide: 10
		}
	});

	jQuery('.minimumtemperatuur').tooltip({
		placement: 'bottom',
		delay: {
			show: 1000,
			hide: 10
		}
	});

	jQuery('.maximumtemperatuur').tooltip({
		placement: 'bottom',
		delay: {
			show: 1000,
			hide: 10
		}
	});

	jQuery('.wind').tooltip({
		placement: 'bottom',
		delay: {
			show: 1000,
			hide: 10
		}
	});

	jQuery('.neerslagkans').tooltip({
		placement: 'bottom',
		delay: {
			show: 1000,
			hide: 10
		}
	});

	jQuery('.neerslag_in_mm').tooltip({
		placement: 'bottom',
		delay: {
			show: 1000,
			hide: 10
		}
	});

	jQuery('.zonkans').tooltip({
		placement: 'bottom',
		delay: {
			show: 1000,
			hide: 10
		}
	});

	jQuery('.bewolking').tooltip({
		placement: 'bottom',
		delay: {
			show: 1000,
			hide: 10
		}
	});

});

jQuery(document).ready(function () {
	"use strict";
	jQuery(".alert-message").alert();
});

jQuery(document).ready(function () {
	"use strict";

	jQuery('a.disabled').click(function (e) {
		e.preventDefault();
	});
});

jQuery(document).ready(function () {
	"use strict";

	if (jQuery('#twitter_stream').length > 0) {
		jQuery("#twitter_stream").tweet({
			avatar_size: 32,
			count: 6,
			query: 'motorrijweer OR motorweer OR "weer om te motorrijden" OR "weer om op de motor" OR motoweer',
			loading_text: "twitterberichten zoeken..."
		});
	}
});

jQuery(document).ready(function () {
	"use strict";
	var chart = null;
	var test = jQuery('.grafiek table thead th').map(function (i, el) {
		return jQuery(el).html();
	}).toArray();

	if (jQuery('#chart').length > 0) {
		chart = new Highcharts.Chart({
			chart: {
				renderTo: 'chart',
				zoomType: null
			},
			title: {
				text: null
			},
			xAxis: {
				categories: jQuery('.grafiek table thead th').map(function (i, el) {
					return jQuery(el).html();
				}).toArray(),
				plotBands: [{ // Light air
					from: -1,
					to: 6,
					color: 'rgba(68, 170, 213, 0.3)',
					label: {
						text: 'Ochtend'
					}
				}, { // Light breeze
					from: 6,
					to: 11,
					color: 'rgba(0, 0, 0, 0)',
					label: {
						text: 'Middag'
					}
				}, { // Light breeze
					from: 12,
					to: 17,
					color: 'rgba(68, 170, 213, 0.3)',
					label: {
						text: 'Avond'
					}
				}],
				plotLines : [{
					value : (function () {
						var d = new Date();
						if (d.getHours() < 6 || d.getHours() > 22) {
							return null;
						}
						return (d.getHours() - 6) + ((d.getMinutes() * (100 / 60)) / 100);
					}()),
					color : '#538BCC',
					dashStyle : 'shortdash',
					width : 1,
					zIndex : 0
				}]
			},
			yAxis: [{ // Primary yAxis
				labels: {
					formatter: function () {
						return this.value + ' ' + jQuery('<div />').html('&#8451;').text();
					},
					style: {
						color: '#89A54E'
					}
				},
				title: {
					text: null,
					style: {
						color: '#89A54E'
					}
				},
				gridLineWidth: 0,
				min: -5,
				max: 35
			}, { // Secondary yAxis (Neerslag)
				title: {
					text: null,
					style: {
						color: '#4572A7'
					}
				},
				labels: {
					formatter: function () {
						return this.value + ' mm';
					},
					style: {
						color: '#4572A7'
					}
				},
				opposite: true,
				gridLineWidth: 0,
				min: 0,
				max: 5
			}, { // Tertiary yAxis (weertype)
				title: {
					text: null
				},
				labels: {
					enabled: false
				},
				gridLineWidth: 0,
				startOnTick: false,
				tickLength: 0,
				opposite: true,
				min: 0,
				max: 3,
				categories: [0, 1, 2, 3],
				alternateGridColor: null
			}, { // 4e axis (windkracht)
				title: {
					text: null
				},
				labels: {
					enabled: false
				},
				gridLineWidth: 0,
				tickLength: 0,
				min: 0,
				max: 12,
				alternateGridColor: null
			}],
			tooltip: {
				formatter: function () {
					var tooltip = '';
					tooltip += this.x + ': ';

					if (this.series.name == 'Neerslag') {
						tooltip += this.y + ' mm';
					} else if (this.series.name == 'Temperatuur') {
						tooltip += this.y + ' °C';
					} else if (this.series.name == 'Windkracht') {
						tooltip += 'windkracht ' + this.y;
					} else {
						return false; //Geen tooltip laten zien
					}

					return tooltip;
				}
			},
			legend: {
				layout: 'vertical',
				align: 'left',
				x: 80,
				verticalAlign: 'top',
				y: 50,
				floating: true,
				backgroundColor: Highcharts.theme.legendBackgroundColor || '#FFFFFF',
				enabled: true
			},
			plotOptions: {
				series: {
					animation: false
				}
			},
			series: [{
				name: 'Neerslag',
				color: '#4572A7',
				type: 'column',
				yAxis: 1,
				// dit betekent aan de rechterkant!
				data: jQuery('.grafiek table tr.neerslag td span.waarde').map(function (i, el) {
					return parseFloat(jQuery(el).html());
				}).toArray()
			}, {
				name: 'Temperatuur',
				color: '#89A54E',
				type: 'spline',
				data: jQuery('.grafiek table tr.temperatuur td span.waarde').map(function (i, el) {
					return parseFloat(jQuery(el).html());
				}).toArray()
			}, {
				name: 'Weertypes',
				color: '#89A54E',
				type: 'scatter',
				yAxis: 2,
				data: jQuery('.grafiek table tr.weertype td img').map(function (i, el) {
					var icon = jQuery(el).attr('src');
					return {
						y: 2.8,
						marker: {
							symbol: 'url(' + icon + ')'
						}
					};
				}).toArray()
			}, {
				name: 'Windkracht',
				color: '#ff0000',
				type: 'spline',
				yAxis: 3,
				data: jQuery('.grafiek table tr.windkracht td span.waarde').map(function (i, el) {
					return parseFloat(jQuery(el).html());
				}).toArray()
			}]
		}, function (chart) {
			var renderer = chart.renderer;


		});
	}

	jQuery('.grafiek table').hide();
});