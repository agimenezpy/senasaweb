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
        }
    )
}

function handle_lookup() {
    var map = this.map;
    var field_name = this.field_name;
    var value = this.node.value;
    if (value.trim().length == 0)
        return;
    dojo.block("container");
    dojo.xhr.get({
        url: "/lookup/" + field_name + "/" + value,
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
                map.zoomToExtent(new OpenLayers.Bounds(itm.extension[0],
                    itm.extension[1],
                    itm.extension[2],
                    itm.extension[3]));
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

var last_func = dismissRelatedLookupPopup;
function dismissRelatedLookupPopup(win, choosenId) {
    var name = windowname_to_id(win.name);
    document.getElementById(name).focus();
    last_func(win, choosenId);
}
