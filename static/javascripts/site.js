jQuery(document).ready(function() {

	jQuery('.cijfer .waarde').twipsy({
		placement: 'below',
		delayIn: 1000,
	  html: true
	});

	jQuery('.weertype img').twipsy({
		placement: 'below',
		delayIn: 1000
	});

	jQuery('.minimumtemperatuur').twipsy({
		placement: 'below',
		delayIn: 1000
	});

	jQuery('.maximumtemperatuur').twipsy({
		placement: 'below',
		delayIn: 1000
	});

	jQuery('.wind').twipsy({
		placement: 'below',
		delayIn: 1000
	});

	jQuery('.neerslagkans').twipsy({
		placement: 'below',
		delayIn: 1000
	});

	jQuery('.neerslag_in_mm').twipsy({
		placement: 'below',
		delayIn: 1000
	});

	jQuery('.zonkans').twipsy({
		placement: 'below',
		delayIn: 1000
	});

	jQuery('.bewolking').twipsy({
		placement: 'below',
		delayIn: 1000
	});

});

jQuery(document).ready(function() {
		jQuery(".alert-message").alert();
});

jQuery(document).ready(function() {
		//
		// Disable certain links in docs
		// =============================
		// Please do not carry these styles over to your projects, it's merely here to prevent button clicks form taking you away from your spot on page

		jQuery('a.disabled').click(function (e) {
				e.preventDefault()
		});
});

jQuery(document).ready(function() {
	//jQuery('.grafiek table').visualize({
		//type: 'line',
		//width: '905px'
	//});
	//jQuery('.grafiek table').css('display', 'none');
});
var chart;
var test = jQuery('.grafiek table thead th').map(function(i, el){
	return jQuery(el).html();
}).toArray();

//jQuery(document).ready(function() {
   //chart = new Highcharts.Chart({
      //chart: {
         //renderTo: 'chart',
         //defaultSeriesType: 'line',
         //marginRight: 0,
         //marginBottom: 25
      //},
      //title: {
         //text: 'Monthly Average Temperature',
         //x: -20 //center
      //},
      //subtitle: {
         //text: 'Source: WorldClimate.com',
         //x: -20
      //},
      //xAxis: {
         //categories: jQuery('.grafiek table thead th').map(function(i, el){
						 //return jQuery(el).html();
					 //}).toArray()
      //},
      ////yAxis: {
         ////title: {
            ////text: 'Temperature (°C)'
         ////},
         ////plotLines: [{
            ////value: 0,
            ////width: 1,
            ////color: '#808080'
         ////}]
      ////},
      //yAxis: [{ // Primary yAxis
         //labels: {
            //formatter: function() {
               //return this.value +'°C';
            //},
            //style: {
               //color: '#89A54E'
            //}
         //},
         //title: {
            //text: 'Temperature',
            //style: {
               //color: '#89A54E'
            //}
         //}
      //}, { // Secondary yAxis
         //labels: {
            //formatter: function() {
               //return this.value +' mm';
            //},
            //style: {
               //color: '#4572A7'
            //}
         //},
         //title: {
            //text: 'Rainfall',
            //style: {
               //color: '#4572A7'
            //}
         //},
         //opposite: true
      //}],
      //tooltip: {
         //formatter: function() {
                   //return '<b>'+ this.series.name +'</b><br/>'+
               //this.x +': '+ this.y +'Â°C';
         //}
      //},
      //legend: {
         //layout: 'vertical',
         //align: 'right',
         //verticalAlign: 'top',
         //x: -10,
         //y: 100,
         //borderWidth: 0
      //},
      //series: [{
         //name: 'Temperatuur',
         //data: jQuery('.grafiek table tr.temperatuur').map(function(i, el){
						 //return jQuery(el).html();
					 //}).toArray()
      //}, {
         //name: 'New York',
         //data: [-0.2, 0.8, 5.7, 11.3, 17.0, 22.0, 24.8, 24.1, 20.1, 14.1, 8.6, 2.5]
      //}, {
         //name: 'Berlin',
         //data: [-0.9, 0.6, 3.5, 8.4, 13.5, 17.0, 18.6, 17.9, 14.3, 9.0, 3.9, 1.0]
      //}, {
         //name: 'London',
         //data: [3.9, 4.2, 5.7, 8.5, 11.9, 15.2, 17.0, 16.6, 14.2, 10.3, 6.6, 4.8]
      //}, {
         //name: 'Rainfall',
         //color: '#89A54E',
         //type: 'spline',
         //data: [7.0, 6.9, 9.5, 14.5, 18.2, 21.5, 25.2, 26.5, 23.3, 18.3, 13.9, 9.6]
      //}]
   //});


//});

var chart;
$(document).ready(function() {
	chart = new Highcharts.Chart({
		chart: {
				   renderTo: 'chart',
		  zoomType: 'xy',
		  events: {
			  load: function() {

						pl = this.plotLeft;
						pt = this.plotTop + this.plotHeight;

						x = pl + this.xAxis[0].translate(4);
						y = pt - this.yAxis[1].translate(1);
						y = this.plotHeight + 100;
						this.renderer.circle(x, y, 9).attr({
							fill: 'red',
							zIndex: 9
						}).add();
					},
		  redraw: function() {
				  }
		  }
			   },
			title: {
					   text: null
				   },
			//subtitle: {
			//text: 'Source: WorldClimate.com'
			//},
			xAxis: {
					   categories: jQuery('.grafiek table thead th').map(function(i, el){
									   return jQuery(el).html();
								   }).toArray(),


					   plotBands: [{ // Light air
									  from: -1,
									  to: 6,
									  color: 'rgba(68, 170, 213, 0.3)',
									  label: {
										  text: 'Ochtend',
									  },
								  }, { // Light breeze
									  from: 6,
									  to: 11,
									  color: 'rgba(0, 0, 0, 0)',
									  label: {
										  text: 'Middag',
									  }
								  }, { // Light breeze
									  from: 12,
									  to: 17,
									  color: 'rgba(68, 170, 213, 0.3)',
									  label: {
										  text: 'Avond',
									  }
								  }],







				   },
			yAxis: [{ // Primary yAxis
					   labels: {
								   formatter: function() {
												  return this.value + ' ' + jQuery('<div />').html('&#8451;').text();
											  },
								   style: {
											  color: '#89A54E'
										  }
							   },
					   title: {
								  text: 'Temperatuur',
								  style: {
									  color: '#89A54E'
								  }
							  },
					   gridLineWidth: 0
				   }, { // Secondary yAxis (Neerslag)
					   title: {
								  text: 'Neerslag in mm',
								  style: {
									  color: '#4572A7'
								  }
							  },
					   labels: {
								   formatter: function() {
												  return this.value +' mm';
											  },
								   style: {
											  color: '#4572A7'
										  }
							   },
					   opposite: true,
					   gridLineWidth: 0
				   }, { // Tertiary yAxis (weertype)
					   title: {
								  text: null,
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
								  text: null,
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
								formatter: function() {
												 var tooltip = '';
												 tooltip += this.x + ': ';

												 if (this.series.name == 'Neerslag') {
														 tooltip += this.y + ' mm';
												 } else if (this.series.name == 'Temperatuur') {
														tooltip += this.y + ' °C';
												 } else if (this.series.name == 'Windkracht') {
														tooltip += 'windkracht ' + this.y;
												 } else {
														 return null;
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
				   series: [{
							   name: 'Neerslag',
							   color: '#4572A7',
							   type: 'column',
							   yAxis: 1, // dit betekent aan de rechterkant!
							   data: jQuery('.grafiek table tr.neerslag td span.waarde').map(function(i, el){
								   return parseFloat(jQuery(el).html());
							   }).toArray()
						   }, {
							   name: 'Temperatuur',
							   color: '#89A54E',
							   type: 'spline',
							   data: jQuery('.grafiek table tr.temperatuur td span.waarde').map(function(i, el){
								   return parseFloat(jQuery(el).html())
							   }).toArray()
						   }, {
							   name: 'Weertypes',
							   color: '#89A54E',
							   type: 'scatter',
							   yAxis: 2,
							   data: jQuery('.grafiek table tr.weertype td img').map(function(i, el){
										 var icon = jQuery(el).attr('src');
										 return {y: 2.8, marker: {symbol: 'url('+icon+')'}}
							   }).toArray()
						   }, {
							   name: 'Windkracht',
							   color: '#ff0000',
							   type: 'spline',
							   yAxis: 3,
							   data: jQuery('.grafiek table tr.windkracht td span.waarde').map(function(i, el){
								   return parseFloat(jQuery(el).html())
							   }).toArray()
						   }]
	}, function(chart) {
		var renderer = chart.renderer;


	}
	);

	jQuery('.grafiek table').hide();
});


