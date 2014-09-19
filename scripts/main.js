(function (window, document, L, undefined) {
    'use strict';

    var getColor = function (d) {
        return d < 3   ? '#fee5d9' :
               d < 4.5 ? '#fcae91' :
               d < 6   ? '#fb6a4a' :
                         '#cb181d'
    }

    var onEachFeature = function (feature, layer) {
        if (feature.properties) {
            var props = feature.properties,
                content = '<strong>' +
                props.zip + '</strong><br>' +
                (props.handguns / props.pop * 1000).toFixed(1) + ' handguns per 1,000 residents<br>' +
                props.handguns + ' total guns';
            layer.bindPopup(content);
        }
    }

    /* create leaflet map */
    var map = L.map('map', {
        center: [38.895111, -77.036667],
        zoom: 11
    });

    /* add tile layer */
    new L.tileLayer('http://{s}.tile.stamen.com/toner-background/{z}/{x}/{y}.png', {
        minZoom: 0,
        maxZoom: 18,
        attribution: 'Tiles by <a href="http://stamen.com/">Stamen Design</a> | Data by <a href="http://www.openstreetmap.org">OpenStreetMap</a>'
    }).addTo(map);

    /* add data layer */
    new L.geoJson(data, {
        style: function (feature) {
            var percapita = feature.properties.handguns / feature.properties.pop * 1000
            return {
                weight: 2,
                color: '#fff',
                opacity: 1,
                fillOpacity: .7,
                fillColor: getColor(percapita)
            };
        },
        onEachFeature: onEachFeature
    }).addTo(map)

    /* add legend */
    var legend = L.control({position: "bottomleft"});

    legend.onAdd = function (map) {
        var div = L.DomUtil.create('div', 'info legend'),
            start = 1.5,
            interval = 1.5,
            count = 4;

        for (var i = 0; i < count; i++) {
            div.innerHTML +=
                '<i style="background:' +
                getColor(start + (interval * i)) + '"></i> ' +
                (start + (interval * i)).toFixed(1) + ' &ndash; ' +
                (start + (interval * (i + 1))).toFixed(1) + '<br>';
        }

        return div;
    };

    legend.addTo(map);

}(window, document, L));