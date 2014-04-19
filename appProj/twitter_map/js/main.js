var map, heatmap, chart;
var markers = [];
var tweetsArray = [];

google.maps.event.addDomListener(window, 'load', initialize);

//Draw Chart
google.load("visualization", "1", {packages:["corechart"]});
google.setOnLoadCallback(drawChart);

$(function() {
    var keywords_dict;
    $.getJSON('/gethotkey',function(data){
        $.each(data,function(i,field) {
           keywords_dict =  field;
        });
        var available_keywords = [];
        for(var key in keywords_dict) {
            available_keywords[available_keywords.length] = {
                value: key,
                desc: keywords_dict[key]
            };
        }
        available_keywords.sort(function(a,b){return b.desc- a.desc});
        $( "#search-field" ).autocomplete({
          source: available_keywords
        })
        .data( "ui-autocomplete" )._renderItem = function( ul, item ) {
            return $( "<li>" )
            .append("<a><span class='keyword'>"+item.value +"</span><span class='description'>"
                     + item.desc + " tweets</span></a>")
            .appendTo( ul );
        };
    });
});

$(function() {
    var options = {
      language: 'en',
      pick12HourFormat: false,
      minDate: '1/1/14',               //set a minimum date
      maxDate: new Date()
    };
    $('#date-start').datetimepicker(options);
    $('#date-end').datetimepicker(options);
    $("#date-start").on("dp.change",function (e) {
       $('#date-end').data("DateTimePicker").setMinDate(e.date);
    });
    $("#date-end").on("dp.change",function (e) {
       $('#date-start').data("DateTimePicker").setMaxDate(e.date);
    });
});

$(document).ready(function(){
  $("#btn-slide-up").click(function(){
    $("#chart-panel").slideToggle("fast","linear",function(){
        chart.draw();
    });
    $("#btn-slide-up").hide();
    $("#btn-slide-down").show();
  });
  $("#btn-slide-down").click(function(){
    $("#chart-panel").slideToggle("fast","linear");
    $("#btn-slide-down").hide();
    $("#btn-slide-up").show();
  });
});

function initialize() {
  //Create map
  var mapOptions = {
    zoom: 5,
    center: new google.maps.LatLng(40.579973, -74.045534),
    mapTypeId: google.maps.MapTypeId.MAP,
    mapTypeControl: false,
    streetViewControl: false
  };
  map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);

  //Create heat map
  var pointArray = setHeatmapPointArray();
  heatmap = new google.maps.visualization.HeatmapLayer({
    map: map,
    data: pointArray,
    radius: 20
  });

  //Create point map
  setMarkerPointArray();
}

function changeMapType(id) {
    switch (id) {
        case 0:
            map.setMapTypeId(google.maps.MapTypeId.ROADMAP);
            break;
        case 1:
            map.setMapTypeId(google.maps.MapTypeId.SATELLITE);
            break;
        case 2:
            map.setMapTypeId(google.maps.MapTypeId.HYBRID);
            break;
        case 3:
            map.setMapTypeId(google.maps.MapTypeId.TERRAIN);
            break;
    }
}

function setHeatmapPointArray() {
    var tweetPoint = [];
    for(var i=0; i<tweetsArray.length; i++) {
        var tweet = tweetsArray[i];
        tweetPoint.push(new google.maps.LatLng(tweet.location.lat, tweet.location.lon));
    }
    var pointArray = new google.maps.MVCArray(tweetPoint);
    return pointArray;
}

function setMarkerPointArray() {
    clearPointmap();
    var map_value = document.getElementById("btn-pointmap").checked ? map : null;
    for(var i=0; i<tweetsArray.length; i++) {
        var tweet = tweetsArray[i];
        var markerOptions = {
          map: map_value,
          position: new google.maps.LatLng(tweet.location.lat, tweet.location.lon),
          tid: tweet.tid,
          date: new Date(tweet.date).toLocaleString(),
          icon: {
                path: google.maps.SymbolPath.CIRCLE,
                fillOpacity: 1.0,
                fillColor: '#3498db',
                strokeOpacity: 1.0,
                strokeColor: '#3498db',
                strokeWeight: 0,
                scale: 2 //pixels
          }
        };
        markers.push(new google.maps.Marker(markerOptions));
    }
    var infowindow = new google.maps.InfoWindow({
        content: ''
    });
    for(var i=0; i<markers.length; i++) {
        google.maps.event.addListener(markers[i], 'click', function() {
            $.getJSON('/display?tid='+this.tid, function(data){
                var tweet;
                $.each(data, function(i,field){
                    tweet = field;
                });
                var tweetContent = '<div id="content">'+
              '<div id="siteNotice">'+
              '</div>'+'<div id="bodyContent">'+
              '<p><b><a href="https://twitter.com/'+tweet.uname+'">'+tweet.uname+'</a></b>&nbsp;&nbsp;'+tweet.text+
              '&nbsp;&nbsp;'+new Date(tweet.date).toLocaleString()+'</p>'+'</div>'+
              '</div>';
              var windowOptions = {
                content: tweetContent,
                maxWidth: 400
              };
              infowindow.setOptions(windowOptions);

            });
            infowindow.open(map,this);
        });
    }
}

function reloadHeatmapData(newPoints) {
    heatmap.setData(newPoints);
}

function toggleHeatmap() {
  heatmap.setMap(heatmap.getMap() ? null : map);
}

function togglePointmap() {
    for(var i=0; i<markers.length; i++) {
        markers[i].setMap(markers[i].getMap() ? null : map);
    }
}

function clearPointmap() {
    for(var i=0; i<markers.length; i++) {
        markers[i].setMap(null);
    }
    markers = [];
}

function changeGradient() {
  var gradient = [
    'rgba(0, 255, 255, 0)',
    'rgba(0, 255, 255, 1)',
    'rgba(0, 191, 255, 1)',
    'rgba(0, 127, 255, 1)',
    'rgba(0, 63, 255, 1)',
    'rgba(0, 0, 255, 1)',
    'rgba(0, 0, 223, 1)',
    'rgba(0, 0, 191, 1)',
    'rgba(0, 0, 159, 1)',
    'rgba(0, 0, 127, 1)',
    'rgba(63, 0, 91, 1)',
    'rgba(127, 0, 63, 1)',
    'rgba(191, 0, 31, 1)',
    'rgba(255, 0, 0, 1)'
  ]
  heatmap.set('gradient', heatmap.get('gradient') ? null : gradient);
}

function changeRadius() {
  heatmap.set('radius', heatmap.get('radius') ? null : 20);
}

function changeOpacity() {
  heatmap.set('opacity', heatmap.get('opacity') ? null : 0.2);
}


function setChartDataArray() {
    var data = new google.visualization.DataTable();
    data.addColumn('date', 'Date');
    data.addColumn('number', 'Amount');
    for(var i=0; i<tweetsArray.length; i++) {
        var tweet = tweetsArray[i];
        data.addRow([new Date(tweet.date), 1]);
    }
    var result = google.visualization.data.group(
      data,
      [{'column': 0, 'modifier': ignoreSeconds, 'type': 'date'}],
      [{'column': 1, 'aggregation': google.visualization.data.sum, 'type': 'number'}]
    );
    var formatter = new google.visualization.DateFormat({pattern: "d/MM/y HH:mm"});
    formatter.format(result, 0);
    return result;
}

function drawChart() {
    var dataArray = setChartDataArray();
    var wrapperOptions = {
      chartType: 'LineChart',
      dataTable: dataArray,
      options: {title: 'Twitter Trends',
                backgroundColor: { fill:'white' },
                hAxis: {title: 'Time', textPosition: 'in',
                    format:'d/MM/y HH:mm', showTextEvery: 1, slantedText: true},
                vAxis: {title: 'Amount'},
                legend: {position:'none'},
                explorer: {actions: ['dragToZoom', 'rightClickToReset'], axis: 'horizontal', maxZoomIn: 0.01}
                },
      containerId: 'chart-div'
    };
    chart = new google.visualization.ChartWrapper(wrapperOptions);
    chart.draw();
}

function ignoreSeconds(date) {
    date.setUTCSeconds(0);
    return date;
}

function ignoreHours(date) {
    date.setUTCHours(0,0,0);
    return date;
}

function reloadChartData(newData) {
    chart.setDataTable(newData);
    chart.draw();
}

function search() {
    var keyword = document.getElementById("search-field").value;
    var startDate = document.getElementById("date-start").value;
    var endDate = document.getElementById("date-end").value;
    hideSearchbar();
    $.getJSON("/search?keyword="+keyword+"&startDate="+startDate+"&endDate="+endDate, function(data){
        $.each(data,function(i,field) {
            tweetsArray = field;
        });
        var newPointArray = setHeatmapPointArray();
        reloadHeatmapData(newPointArray);
        setMarkerPointArray();
        var newChartData = setChartDataArray();
        reloadChartData(newChartData);
    });
}

function showSearchbar() {
    var env = getEnv();
    if(env == 'xs' || env == 'sm') {
        $("#date-start").show();
        $("#date-end").show();
        $("#cancel-btn").show();
    }
}

function hideSearchbar() {
    var env = getEnv();
    if(env == 'xs' || env == 'sm') {
        $("#date-start").hide();
        $("#date-end").hide();
        $("#cancel-btn").hide();
    }
}

function getEnv() {
    var envs = ['xs', 'sm', 'md', 'lg'];

    $el = $('<div>');
    $el.appendTo($('body'));

    for (var i = envs.length - 1; i >= 0; i--) {
        var env = envs[i];

        $el.addClass('hidden-'+env);
        if ($el.is(':hidden')) {
            $el.remove();
            return env
        }
    }
}