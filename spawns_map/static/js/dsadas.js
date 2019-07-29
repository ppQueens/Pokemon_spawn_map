
//<![CDATA[
var geoXml = null;
var geoXmlDoc = null;
var map = null;
var myLatLng = null;
var myGeoXml3Zoom = true;
var sidebarHtml = "";
var infowindow = null;
var kmlLayer = null;
var filename = "TrashDays40.xml";
var geocoder = new google.maps.Geocoder();
  function MapTypeId2UrlValue(maptype) {
    var urlValue = 'm';
    switch(maptype){
      case google.maps.MapTypeId.HYBRID:    urlValue='h';
                        break;
      case google.maps.MapTypeId.SATELLITE: urlValue='k';
                        break;
      case google.maps.MapTypeId.TERRAIN:   urlValue='t';
                        break;
      default:
      case google.maps.MapTypeId.ROADMAP:   urlValue='m';
                        break;
    }
    return urlValue;
  }

      // ========== This function will create the "link to this page"
      function makeLink() {
//        var a="http://www.geocodezip.com/v3_MW_example_linktothis.html"
        var url = window.location.pathname;
        var a = url.substring(url.lastIndexOf('/')+1)
           + "?lat=" + map.getCenter().lat().toFixed(6)
           + "&lng=" + map.getCenter().lng().toFixed(6)
           + "&zoom=" + map.getZoom()
           + "&type=" + MapTypeId2UrlValue(map.getMapTypeId());
        if (filename != "TrashDays40.xml") a += "&filename="+filename;
        document.getElementById("link").innerHTML = '<a href="' +a+ '">Link to this page<\/a>';
      }
    function initialize() {
      myLatLng = new google.maps.LatLng(37.422104808,-122.0838851);
      // these set the initial center, zoom and maptype for the map
      // if it is not specified in the query string
      var lat = 37.422104808;
      var lng = -122.0838851;
      var zoom = 18;
      var maptype = google.maps.MapTypeId.ROADMAP;

      // If there are any parameters at eh end of the URL, they will be in  location.search
      // looking something like  "?marker=3"

      // skip the first character, we are not interested in the "?"
      var query = location.search.substring(1);

      // split the rest at each "&" character to give a list of  "argname=value"  pairs
      var pairs = query.split("&");
      for (var i=0; i<pairs.length; i++) {
        // break each pair at the first "=" to obtain the argname and value
	var pos = pairs[i].indexOf("=");
	var argname = pairs[i].substring(0,pos).toLowerCase();
	var value = pairs[i].substring(pos+1).toLowerCase();

        // process each possible argname  -  use unescape() if theres any chance of spaces
        if (argname == "id") {id = unescape(value);}
        if (argname == "filename") {
          filename = unescape(pairs[i].substring(pos+1)); // was value
          if (filename.indexOf(",") > 0) {
            filename = filename.split(",");
          }
        }
        if (argname == "marker") {index = parseFloat(value);}
        if (argname == "lat") {lat = parseFloat(value);}
        if (argname == "lng") {lng = parseFloat(value);}
        if (argname == "zoom") {
	  zoom = parseInt(value);
	  myGeoXml3Zoom = false;
	}
        if (argname == "type") {
// from the v3 documentation 8/24/2010
// HYBRID This map type displays a transparent layer of major streets on satellite images.
// ROADMAP This map type displays a normal street map.
// SATELLITE This map type displays satellite images.
// TERRAIN This map type displays maps with physical features such as terrain and vegetation.
          if (value == "m") {maptype = google.maps.MapTypeId.ROADMAP;}
          if (value == "k") {maptype = google.maps.MapTypeId.SATELLITE;}
          if (value == "h") {maptype = google.maps.MapTypeId.HYBRID;}
          if (value == "t") {maptype = google.maps.MapTypeId.TERRAIN;}

        }
      }
      if (!isNaN(lat) && !isNaN(lng)) {
        myLatLng = new google.maps.LatLng(lat, lng);
      }
                var myOptions = {
                    zoom: zoom,
                    center: myLatLng,
                    // zoom: 5,
                    // center: myLatlng,
                    mapTypeId: maptype
                };
                map = new google.maps.Map(document.getElementById("map_canvas"),
                      myOptions);
                infowindow = new google.maps.InfoWindow({});
   showLoad();
   var a = performance.now();
   geoXml = new geoXML3.parser({
                    map: map,
                    infoWindow: infowindow,
                    singleInfoWindow: true,
		    zoom: myGeoXml3Zoom,
		    markerOptions: {optimized: false},
                    afterParse: useTheData,
                    failedParse: geoxmlErrorHandler
                });
   google.maps.event.addListener(geoXml,'parsed', function() {
       var b = performance.now();
       document.getElementById('perf').innerHTML = 'load time ' + ((b - a)/1000).toFixed(2) + ' seconds';
         hideLoad();
   });
                geoXml.parse(filename);
		google.maps.event.addListener(map, "bounds_changed", makeSidebar);
		google.maps.event.addListener(map, "center_changed", makeSidebar);
		google.maps.event.addListener(map, "zoom_changed", makeSidebar);
		google.maps.event.addListenerOnce(map, "idle", makeSidebar);
      // Make the link the first time when the page opens
      makeLink();

      // Make the link again whenever the map changes
      google.maps.event.addListener(map, 'maptypeid_changed', makeLink);
      google.maps.event.addListener(map, 'center_changed', makeLink);
      google.maps.event.addListener(map, 'bounds_changed', makeLink);
      google.maps.event.addListener(map, 'zoom_changed', makeLink);
            };

function kmlPgClick(pm) {
   if (geoXml.docs[0].placemarks[pm].polygon.getMap()) {
      google.maps.event.trigger(geoXmlDoc.placemarks[pm].polygon,"click");
   } else {
      geoXmlDoc.placemarks[pm].polygon.setMap(map);
      google.maps.event.trigger(geoXmlDoc.placemarks[pm].polygon,"click");
   }
}
function kmlPlClick(pm) {
   if (geoXml.docs[0].placemarks[pm].polyline.getMap()) {
      google.maps.event.trigger(geoXmlDoc.placemarks[pm].polyline,"click");
   } else {
      geoXmlDoc.placemarks[pm].polyline.setMap(map);
      google.maps.event.trigger(geoXmlDoc.placemarks[pm].polyline,"click");
   }
}
function kmlClick(pm) {
   if (geoXml.docs[0].placemarks[pm].marker.getMap()) {
      google.maps.event.trigger(geoXml.docs[0].placemarks[pm].marker,"click");
   } else {
      geoXmlDoc.placemarks[pm].marker.setMap(map);
      google.maps.event.trigger(geoXmlDoc.placemarks[pm].marker,"click");
   }
}
function kmlShowPlacemark(pm) {
  if (geoXmlDoc.placemarks[pm].polygon) {
    map.fitBounds(geoXmlDoc.placemarks[pm].polygon.bounds);
  } else if (geoXmlDoc.placemarks[pm].polyline) {
    map.fitBounds(geoXmlDoc.placemarks[pm].polyline.bounds);
  } else if (geoXmlDoc.placemarks[pm].marker) {
    map.setCenter(geoXmlDoc.placemarks[pm].marker.getPosition());
  }

   for (var i=0;i<geoXmlDoc.placemarks.length;i++) {
     var placemark = geoXmlDoc.placemarks[i];
     if (i == pm) {
       if (placemark.polygon) placemark.polygon.setMap(map);
       if (placemark.polyline) placemark.polyline.setMap(map);
       if (placemark.marker) placemark.marker.setMap(map);
     } else {
       if (placemark.polygon) placemark.polygon.setMap(null);
       if (placemark.polyline) placemark.polyline.setMap(null);
       if (placemark.marker) placemark.marker.setMap(null);
     }
   }
}

var highlightOptions = {fillColor: "#FFFF00", strokeColor: "#000000", fillOpacity: 0.9, strokeWidth: 10};
var highlightLineOptions = {strokeColor: "#FFFF00", strokeWidth: 10};
function kmlHighlightPoly(pm) {
   for (var i=0;i<geoXmlDoc.placemarks.length;i++) {
     var placemark = geoXmlDoc.placemarks[i];
     if (i == pm) {
       if (placemark.polygon) placemark.polygon.setOptions(highlightOptions);
       if (placemark.polyline) placemark.polyline.setOptions(highlightLineOptions);
     } else {
       if (placemark.polygon) placemark.polygon.setOptions(placemark.polygon.normalStyle);
       if (placemark.polyline) placemark.polyline.setOptions(placemark.polyline.normalStyle);
     }
   }
}
function kmlUnHighlightPoly(pm) {
   for (var i=0;i<geoXmlDoc.placemarks.length;i++) {
     if (i == pm) {
       var placemark = geoXmlDoc.placemarks[i];
       if (placemark.polygon) placemark.polygon.setOptions(placemark.polygon.normalStyle);
       if (placemark.polyline) placemark.polyline.setOptions(placemark.polyline.normalStyle);
     }
   }
}


function showAll() {
   map.fitBounds(geoXmlDoc.bounds);
   for (var i=0;i<geoXmlDoc.placemarks.length;i++) {
     var placemark = geoXmlDoc.placemarks[i];
     if (placemark.polygon) placemark.polygon.setMap(map);
     if (placemark.polyline) placemark.polyline.setMap(map);
     if (placemark.marker) placemark.marker.setMap(map);
   }
}

function highlightPoly(poly, polynum) {
  //    poly.setOptions({fillColor: "#0000FF", strokeColor: "#0000FF", fillOpacity: 0.3}) ;
  google.maps.event.addListener(poly,"mouseover",function() {
    var rowElem = document.getElementById('row'+polynum);
    if (rowElem) rowElem.style.backgroundColor = "#FFFA5E";
    if (geoXmlDoc.placemarks[polynum].polygon) {
      poly.setOptions(highlightOptions);
    } else if (geoXmlDoc.placemarks[polynum].polyline) {
      poly.setOptions(highlightLineOptions);
    }
  });
  google.maps.event.addListener(poly,"mouseout",function() {
    var rowElem = document.getElementById('row'+polynum);
    if (rowElem) rowElem.style.backgroundColor = "#FFFFFF";
    poly.setOptions(poly.normalStyle);
  });
}

// == rebuilds the sidebar to match the markers currently displayed ==
function makeSidebarPolygonEntry(i) {
  var name = geoXmlDoc.placemarks[i].name;
   if (!name  || (name.length == 0)) name = "polygon #"+i;
   // alert(name);
   sidebarHtml += '<tr id="row'+i+'"><td onmouseover="kmlHighlightPoly('+i+');" onmouseout="kmlUnHighlightPoly('+i+');"><a href="javascript:kmlPgClick('+i+');">'+name+'</a> - <a href="javascript:kmlShowPlacemark('+i+');">show</a></td></tr>';

}
function makeSidebarPolylineEntry(i) {
  var name = geoXmlDoc.placemarks[i].name;
   if (!name  || (name.length == 0)) name = "polyline #"+i;
   // alert(name);
   sidebarHtml += '<tr id="row'+i+'"><td onmouseover="kmlHighlightPoly('+i+');" onmouseout="kmlUnHighlightPoly('+i+');"><a href="javascript:kmlPlClick('+i+');">'+name+'</a> - <a href="javascript:kmlShowPlacemark('+i+');">show</a></td></tr>';

}
function makeSidebarEntry(i) {
  var name = geoXmlDoc.placemarks[i].name;
   if (!name  || (name.length == 0)) name = "marker #"+i;
   // alert(name);
   sidebarHtml += '<tr id="row'+i+'"><td><a href="javascript:kmlClick('+i+');">'+name+'</a></td></tr>';
}

function makeSidebar() {
  sidebarHtml = '<table><tr><td><a href="javascript:showAll();">Show All</a></td></tr>';
  var currentBounds = map.getBounds();
// if bounds not yet available, just use the empty bounds object;
if (!currentBounds) currentBounds=new google.maps.LatLngBounds();
if (geoXmlDoc && geoXmlDoc.placemarks) {
  for (var i=0; i<geoXmlDoc.placemarks.length; i++) {
    if (geoXmlDoc.placemarks[i].polygon) {
      if (currentBounds.intersects(geoXmlDoc.placemarks[i].polygon.bounds)) {
         makeSidebarPolygonEntry(i);
      }
    }
    if (geoXmlDoc.placemarks[i].polyline) {
      if (currentBounds.intersects(geoXmlDoc.placemarks[i].polyline.bounds)) {
         makeSidebarPolylineEntry(i);
      }
    }
    if (geoXmlDoc.placemarks[i].marker) {
      if (currentBounds.contains(geoXmlDoc.placemarks[i].marker.getPosition())) {
         makeSidebarEntry(i);
      }
    }
  }
}
  sidebarHtml += "</table>";
  document.getElementById("sidebar").innerHTML = sidebarHtml;
}

function geoxmlErrorHandler(doc){
  showParseError();
  alert("GEOXML3: failed parse");
}

function useTheData(doc){
  var currentBounds = map.getBounds();
  if (!currentBounds) currentBounds=new google.maps.LatLngBounds();
  // Geodata handling goes here, using JSON properties of the doc object
  sidebarHtml = '<table><tr><td><a href="javascript:showAll();">Show All</a></td></tr>';
//  var sidebarHtml = '<table>';
  geoXmlDoc = doc[0];
  if (!geoXmlDoc || !geoXmlDoc.placemarks) return;
  for (var i = 0; i < geoXmlDoc.placemarks.length; i++) {
    // console.log(doc[0].markers[i].title);
    var placemark = geoXmlDoc.placemarks[i];
    if (placemark.polygon) {
      if (currentBounds.intersects(placemark.polygon.bounds)) {
        makeSidebarPolygonEntry(i);
      }
      var normalStyle = {
          strokeColor: placemark.polygon.get('strokeColor'),
          strokeWeight: placemark.polygon.get('strokeWeight'),
          strokeOpacity: placemark.polygon.get('strokeOpacity'),
          fillColor: placemark.polygon.get('fillColor'),
          fillOpacity: placemark.polygon.get('fillOpacity')
          };
      placemark.polygon.normalStyle = normalStyle;

      highlightPoly(placemark.polygon, i);
    }
    if (placemark.polyline) {
      if (currentBounds.intersects(placemark.polyline.bounds)) {
         makeSidebarPolylineEntry(i);
      }
      var normalStyle = {
          strokeColor: placemark.polyline.get('strokeColor'),
          strokeWeight: placemark.polyline.get('strokeWeight'),
          strokeOpacity: placemark.polyline.get('strokeOpacity')
          };
      placemark.polyline.normalStyle = normalStyle;

      highlightPoly(placemark.polyline, i);
    }
    if (placemark.marker) {
      if (currentBounds.contains(placemark.marker.getPosition())) {
         makeSidebarEntry(i);
      }
    }

/*    doc[0].markers[i].setVisible(false); */
  }
  sidebarHtml += "</table>";
  document.getElementById("sidebar").innerHTML = sidebarHtml;
};


   function hide_kml(){

            geoXml.hideDocument();

   }

   function unhide_kml(){

            geoXml.showDocument();

   }
function reload_kml(){
   geoXml.hideDocument();
   delete geoXml;
   geoXml = new geoXML3.parser({
                    map: map,
                    singleInfoWindow: true,
                    afterParse: useTheData
   });
   geoXml.parse(filename);

}

   function hide_polys_kml(){
     for (var i=0;i<geoXmlDoc.gpolylines.length;i++) {
       geoXmlDoc.gpolylines[i].setMap(null);
     }
   }

   function unhide_polys_kml(){
     for (var i=0;i<geoXmlDoc.gpolylines.length;i++) {
       geoXmlDoc.gpolylines[i].setMap(map);
     }
   }


// A function to hide the loading message
function hideLoad()
{
   var loaddiv = document.getElementById("loaddiv");
   if (loaddiv == null)
   {
      alert("Sorry can't find the loaddiv");
      return;
   }
   //div found
   loaddiv.style.visibility="hidden";
}

// A function to hide the loading message
function showLoad()
{
   var loaddiv = document.getElementById("loaddiv");
   if (loaddiv == null)
   {
      alert("Sorry can't find your loaddiv");
      return;
   }
   //div found
   loaddiv.style.visibility="visible";
}
function showParseError()
{
   var loaddiv = document.getElementById("loaddiv");
   if (loaddiv == null)
   {
      alert("Sorry can't find your loaddiv");
      return;
   }
   //div found
   loaddiv.style.visibility="visible";
   loaddiv.innerHTML = "<b>XML parse error</b>";
}
function codeAddress() {
  var address = document.getElementById('address').value;
  geocoder.geocode( { 'address': address}, function(results, status) {
    if (status == google.maps.GeocoderStatus.OK) {
      var marker = new google.maps.Marker({
          map: map,
          position: results[0].geometry.location
      });
      if (results[0].geometry.viewport)
        map.fitBounds(results[0].geometry.viewport);
      else if (results[0].geometry.bounds)
        map.fitBounds(results[0].geometry.bounds);
      else
        map.setCenter(results[0].geometry.location);

    } else {
      alert('Geocode was not successful for the following reason: ' + status);
    }
  });
}
//]]>
