last_values = {}
function handle_lookup(evt) {
    var $ = evt.data.jquery;
    var map = evt.data.map;
    var input_field = evt.data.target;
    var field_name = input_field.name;
    var value = input_field.value;
    if (!map || value.trim().length == 0 || value == last_values[field_name])
        return;
    last_values[field_name] = value;
    dojo.block("container");
    $.getJSON(window.__prefix__ + "/lookup/" + field_name + "/" + value,function(data, ioArgs) {
            dojo.unblock("container");
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
        },
        function(err, ioArgs) {
            dojo.unblock("container");
    });
}

function dismissRelatedLookupPopup(win, chosenId) {
    var name = windowname_to_id(win.name);
    var elem = document.getElementById(name);
    if (elem.className.indexOf('vManyToManyRawIdAdminField') != -1 && elem.value) {
        elem.value += ',' + chosenId;
    } else {
        document.getElementById(name).value = chosenId;
    }
    elem.focus();
    win.close();
}

function removeRelatedObject(triggeringLink) {
    var id = triggeringLink.id.replace(/^remove_/, '');
    var elem = document.getElementById(id);
    elem.value = "";
    elem.focus();
}