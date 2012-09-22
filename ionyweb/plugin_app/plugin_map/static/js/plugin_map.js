var geocoder;
var map;
var marker;

function map_selector_init(lat, lon) {
    if(isNaN( parseFloat(lat) )) {
	lat = 47.5335;
	lon = 7.2139;
    } else {
	lat = parseFloat(lat);
	lon = parseFloat(lon);
    }

    var latlng = new google.maps.LatLng(lat, lon);
	var myOptions = {
		'zoom': 13,
		'center': latlng,
		'mapTypeId': google.maps.MapTypeId.ROADMAP,
		'mapTypeControl': true,
		'mapTypeControlOptions': {style: google.maps.MapTypeControlStyle.DROPDOWN_MENU},
		'navigationControl': true,
		'navigationControlOptions': {style: google.maps.NavigationControlStyle.SMALL}
	}
	map = new google.maps.Map(document.getElementById('map'), myOptions);

	marker = new google.maps.Marker({
		draggable: true,
		map: map,
		position: map.getCenter()
	});

	writeLL(latlng);

	(function (map, marker){
		google.maps.event.addListener(marker, 'dragend', function(){
			var pt = marker.getPosition();
			map.panTo(pt);
			writeLL(pt);
		});
	})(map, marker);

	(function (map, marker){
		google.maps.event.addListener(map, 'dragend', function(){
			marker.setPosition(map.getCenter());
			writeLL(marker.getPosition());
		});
	})(map, marker);
}

function writeLL(pt){
		document.getElementById("id_map_lat").value = pt.lat().toFixed(7);
		document.getElementById("id_map_lon").value = pt.lng().toFixed(7);
	}

function codeAddress(){
	var address = document.getElementById("address").value;
	if (geocoder) {
		geocoder.geocode( { 'address': address}, function(results, status) {
			if (status == google.maps.GeocoderStatus.OK) {
				var center = results[0].geometry.location;
				map.setCenter(center);
				writeLL(center);
				marker.setPosition(center);
			} else {
			    message = document.getElementById("map-message");
			    message.innerHTML = 'Impossible de trouver '+address;
			    
			}
		});
	}
    return false;
}