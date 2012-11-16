(function(root) {
    var Map = {},
        layers;

    Map = function(el, l, callback) {
        MM_map = mapbox.map(el);
        MM_map.addLayer(mapbox.layer().id(l.api));

        for (var i = 0; i < l.features.length; i++) {
            switch(l.features[i]) {
                case 'zoomer':
                    MM_map.ui.zoomer.add();
                    break;
                case 'zoombox':
                    MM_map.ui.zoombox.add();
                    break;
                case 'legend':
                    MM_map.legend = MM_map.ui.legend.add();
                    break;
                case 'attribution':
                    MM_map.ui.attribution.add();
                    break;
                case 'interaction':
                    MM_map.interaction.auto();
                    break;
                case 'pointselector':
                    MM_map.ui.pointselector.add();
                    break;
                case 'hash':
                    MM_map.ui.hash.add();
                    break;
                case 'fulllscreen':
                    MM_map.ui.fullscreen.add();
                    break;
            }
        }
        MM_map.refresh()
        MM_map.setZoomRange(l.zoomRange[0],l.zoomRange[1])
        MM_map.centerzoom(l.center, l.center.zoom);
        default_center = l.center;
        default_zoom = l.center.zoom

        return Map;
    }

    Map.layers = function(x) {
    }

    Map.markers = function () {
        $.getJSON('features/obras', function(data) {
            var markerLayer = mapbox.markers.layer().features(data.features).factory(function(f){
                var d = document.createElement('div');
                d.className = 'mmg mmg-' + (ICONS[f.properties.producto] ? ICONS[f.properties.producto] : 'default');
                // Add function that centers marker on click
                MM.addEvent(d, 'click', function(e) {
                    MM_map.ease.location({
                        lat: f.geometry.coordinates[1],
                        lon: f.geometry.coordinates[0]
                    }).zoom(15).optimal();
                });
                return d;
            });
            var interaction = mapbox.markers.interaction(markerLayer);
            MM_map.addLayer(markerLayer)

            interaction.formatter(function(feature) {
                var o =  GRUPO[feature.properties.grupo][0] + '<br/>';
                $.each(feature.properties, function(key, val) {
                    if (key != 'grupo')
                        o += '<b>' + key.toUpperCase() + ':</b> ' + val + '<br/>';
                    else {
                        o += '<b>PROYECTO:</b> ' + GRUPO[val][1] + '<br/>';
                    }
                });

                return o;
            });
        })
    }

    Map.filters = function() {
        self = this;
        $("[name='prod_check']").click(function(ev) {
            if (ev.target.value == "Todos") {
                $("[name='prod_check']").each(function(o,i){i.checked = ev.target.checked});
            }
            else {
                $("#chkTodos").checked = false;
            }
            MM_map.getLayer("markers").filter(self.doFilter);
        });
        $("[name='proj_check']").click(function(ev) {
            if (ev.target.value == "Todos") {
                $("[name='proj_check']").each(function(o,i){i.checked = ev.target.checked});
            }
            else {
                $("#chkTodosP").checked = false;
            }
            MM_map.getLayer("markers").filter(self.doFilter);
        });
    }

    Map.doFilter = function(f) {
        vals = $("[name='prod_check']").map(function(o,i){if (i.value != "Todos" && i.checked) return i.value}).toArray();
        val1 = vals.length > 0 && vals.indexOf(f.properties['producto']) != -1
        vals = $("[name='proj_check']").map(function(o,i){if (i.value != "Todos" && i.checked) return i.value}).toArray();
        val2 = vals.length > 0 && vals.indexOf(GRUPO[f.properties['grupo']][1]) != -1
        return val1 && val2
    }

    Map.selects = function() {
        $("[name='departamento']").change(function (ev) {
            if (ev.target.value != "Ninguno") {
                vals = ev.target.value.split(",");
                MM_map.setExtent([{lat:Number(vals[1]) , lon: Number(vals[0])},
                    {lat: Number(vals[3]), lon:Number(vals[2])}])
            }
            else
                MM_map.centerzoom(default_center, default_zoom);
        });
    }
    root.Map = Map;
})(this);
