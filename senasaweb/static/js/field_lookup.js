last_values = {}
function prepare_lookup() {
    var map = null;
    if (this['geodjango_geom'])
        map = this['geodjango_geom'].map
    if (this['geodjango_ubicacion'])
        map = this['geodjango_ubicacion'].map
    dojo.query(".vForeignKeyRawIdAdminField").forEach(
        function(node, index, nodeList) {
            field_name = node.id.split("_")[1];
            dojo.connect(node, "onblur", {"node": node, "map" : map, "field_name" : field_name}, handle_lookup);
            dojo.connect(node, "onfocus", {"node": node, "map" : map, "field_name" : field_name}, handle_lookup);
        }
    )
    if (map) {
        dojo.connect(dojo.byId("centerPanel"),"scroll",map,function(obj){map.updateSize()})
    }
}

function handle_lookup() {
    var map = this.map;
    var field_name = this.field_name;
    var value = this.node.value;
    if (value.trim().length == 0 || value == last_values[field_name])
        return;
    last_values[field_name] = value;
    dojo.block("container");
    dojo.xhr.get({
        url: window.__prefix__ + "/lookup/" + field_name + "/" + value,
        handleAs: "json",
        load: function(data, ioArgs) {
            dojo.unblock("container");
            if (data.items.length == 0) {
                var lbl = dojo.query(".field-" + field_name + " strong").empty();
                if (lbl.length != 0) {
                    lbl.empty();
                    lbl.innerHTML("Valor no econtrado");
                }
                else {
                    dojo.query(".field-" + field_name + " a").after("<strong>Valor no econtrado</strong>");
                }
                return;
            }
            var itm = data.items[0]
            if (map && field_name.match("localidad|departamento|distrito")) {
                prj = new OpenLayers.Projection("EPSG:4326");
                bb = new OpenLayers.Bounds(itm.extension[0],
                    itm.extension[1],
                    itm.extension[2],
                    itm.extension[3]);
                bb.transform(prj,map.getProjectionObject());
                map.zoomToExtent(bb);
            }
            var lbl = dojo.query(".field-" + field_name + " strong");
            if (lbl.length != 0) {
                lbl.empty();
                lbl.innerHTML(itm[data.label]);
            }
            else {
                dojo.query(".field-" + field_name + " a").after("<strong>"+itm[data.label]+"</strong>");
            }
        },
        error : function(err, ioArgs) {
            dojo.unblock("container");
            var lbl = dojo.query(".field-" + field_name + " strong");
            if (lbl.length != 0) {
                lbl.empty();
                lbl.innerHTML("Valor no econtrado");
            }
            else {
                dojo.query(".field-" + field_name + " a").after("<strong>Valor no econtrado</strong>");
            }
        }
    })
}

function dismissRelatedLookupPopup(win, chosenId) {
    var name = windowname_to_id(win.name);
    var elem = document.getElementById(name);
    if (elem.className.indexOf('vManyToManyRawIdAdminField') != -1 && elem.value) {
        elem.value += ',' + chosenId;
    } else {
        document.getElementById(name).value = chosenId;
    }
    elem.focus()
    win.close();
}