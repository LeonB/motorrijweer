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

StationOverlay = function (options) {
	"use strict";
	google.maps.OverlayView.call(this);

	// Now initialize all properties.
	this.map = options.map;
	this.txt = options.txt;
	this.cls = options.cls;
	this.latlng = options.latlng;

	// We define a property to hold the image's
	// div. We'll actually create this div
	// upon receipt of the add() method so we'll
	// leave it null for now.
	this.div = null;

	// Explicitly call setMap() on this overlay
	this.setMap(this.map);

	this.onAdd = function () {
		// Note: an overlay's receipt of onAdd() indicates that
		// the map's panes are now available for attaching
		// the overlay to the map via the DOM.

		// Create the DIV and set some basic attributes.
		var div = document.createElement('DIV');
		div.className = this.cls;
		div.innerHTML = this.txt;

		// Set the overlay's div property to this DIV
		this.div = div;

		// We add an overlay to a map via one of the map's panes.
		var panes = this.getPanes();
		panes.floatPane.appendChild(div);
	};


	this.draw = function () {
		var overlayProjection = this.getProjection();

		// Retrieve the southwest and northeast coordinates of this overlay
		// in latlngs and convert them to pixels coordinates.
		// We'll use these coordinates to resize the DIV.
		var position = overlayProjection.fromLatLngToDivPixel(this.latlng);


		var div = this.div;
		div.style.position = 'absolute';

		// Get the width and height of the div
		// Have to be inserted in the dom to do that
		jQuery('#fixture').remove();
		var fixture = jQuery(document.createElement('div'));
		fixture.attr('id', 'fixture');
		fixture.append(jQuery(div).clone());
		jQuery('body').append(fixture);
		var width = fixture.find('div').width();
		var height = fixture.find('div').height();
		jQuery('#fixture').remove();

		this.div.style.width = width + 'px';
		this.div.style.height = height + 'px';

		// Coordinate = bottom, right of div
		var left = (position.x - (width / 2));
		var top = (position.y - (width / 2));

		// Kijken of de boel erop past
		if (left < 0) {
			left = position.x;
			if (left < 0) {
				left = 0;
			}
		}

		// echt toekennen
		div.style.left = left + 'px';
		div.style.top = top + 'px';

		// div.style.left = position.x + 'px';
		// div.style.top = position.y + 'px';
	};

	this.onRemove = function () {
		this.div.parentNode.removeChild(this.div);
		this.div = null;
	};

	this.hide = function () {
		if (this.div) {
			this.div.style.visibility = "hidden";
		}
	};

	this.show = function () {
		if (this.div) {
			this.div.style.visibility = "visible";
		}
	};

	this.toggleDOM = function () {
		if (this.getMap()) {
			this.setMap(null);
		} else {
			this.setMap(this.map);
		}
	};
};
StationOverlay.prototype = google.maps.OverlayView.prototype;

Weerkaart = function (div_id, center_point) {
	"use strict";

	this.center_point = center_point;
	this.div_id = div_id;
	this.stations = new Array();

	this.add_station = function (station) {
		if (!this.map) {
			this.map = this.draw();
		}

		this.stations.push(station);

		var latitude = jQuery(station.latitude).text();
		var longitude = jQuery(station.longitude).text();
		var latlng = new google.maps.LatLng(latitude, longitude);

		//&deg;

		var minimumtemperatuur = jQuery.trim(jQuery(station.minimumtemperatuur)[0].innerHTML);
		var maximumtemperatuur = jQuery.trim(jQuery(station.maximumtemperatuur)[0].innerHTML);
		var customTxt = station.weertype + '<br />' + minimumtemperatuur + '&deg;' + '/' + maximumtemperatuur + '&deg;';

		new StationOverlay(
			{
				map: this.map,
				cls: "station_overlay",
				latlng: latlng,
				txt: customTxt
			}
		);
	};

	this.style = function () {
		return [
			{
				featureType: "administrative",
				elementType: "all",
				stylers: [
					{ visibility: "off" }
				]
			}, {
				featureType: "administrative.country",
				elementType: "all",
				stylers: [
					{ visibility: "on" }
				]
			}, {
				featureType: "administrative.province",
				elementType: "all",
				stylers: [
					{ visibility: "on" }
				]
			}, {
				featureType: "landscape",
				elementType: "all",
				stylers: [
					{ visibility: "off" }
				]
			}, {
				featureType: "landscape.man_made",
				elementType: "all",
				stylers: [
					{ visibility: "off" }
				]
			}, {
				featureType: "landscape.natural",
				elementType: "all",
				stylers: [
					{ visibility: "off" },
					{ hue: "#1aff00" },
					{ lightness: -17 },
					{ gamme: 0 }
				]
			}, {
				featureType: "transit",
				elementType: "all",
				stylers: [
					{ visibility: "off" }
				]
			}, {
				featureType: "poi",
				elementType: "all",
				stylers: [
					{ visibility: "off" }
				]
			}, {
				featureType: "water",
				elementType: "labels",
				stylers: [
					{ visibility: "off" }
				]
			}, {
				featureType: "road",
				elementType: "all",
				stylers: [
					{ visibility: "off" }
				]
			}
		];
	};

	this.draw = function () {
		// Google maps aanroepen
		var map = new google.maps.Map(document.getElementById(this.div_id), {
			mapTypeControlOptions: {
				mapTypeIds: ['sober']
			},
			center: new google.maps.LatLng(30, 0),
			zoom: 8,
			mapTypeId: 'sober',
			disableDoubleClickZoom: true,
			zoomControl: false,
			streetViewControl: false,
			mapTypeControl: false,
			panControl: false,
			scrollwheel: false,
			draggable: false
		});

		// Style aanpassen
		map.mapTypes.set('sober', new google.maps.StyledMapType(this.style(), { name: 'sober' }));

		//Middenpunt van de kaart neerzetten
		var geocoder = new google.maps.Geocoder();
		geocoder.geocode({ 'address': this.center_point}, function (results, status) {
			if (status == google.maps.GeocoderStatus.OK) {
				map.setCenter(results[0].geometry.location);
			}
		});

		return map;
	};

};

jQuery(document).ready(function () {
	"use strict";

	if (jQuery('#weerkaart').length > 0) {
		var div = jQuery('#weerkaart');
		var center_point = div.find('h2').text();
		var weerkaart = new Weerkaart('weerkaart', center_point);

		var stations = new Array();

		// namen vinden
		jQuery.each(div.find('thead th'), function (index, value) {
			var station = {};
			var element = jQuery(value);
			station.name = jQuery.trim(element.text());
			stations[index] = station;
		});

		// Over alle rijen loopen en alle values vinden
		jQuery.each(div.find('tr th[scope=row]'), function (index, value) {
			var th = jQuery(value);
			var attribute = jQuery.trim(th.parent('tr').attr('class'));
			
			jQuery.each(th.siblings('td'), function (index, value) {
				var element = jQuery(value);
				var attribute_value = jQuery.trim(element[0].innerHTML);
				stations[index][attribute] = attribute_value; //obj.asd == obj['asd']
			});
		});

		jQuery.each(stations, function (index, station) {
			weerkaart.add_station(station);
		});
	};
});