{% extends "gis/admin/openlayers.js" %}
{% block base_layer %}new OpenLayers.Layer.XYZ("Mapbox Light",
    [
        "http://a.tiles.mapbox.com/v3/mapbox.mapbox-light/${z}/${x}/${y}.png",
        "http://b.tiles.mapbox.com/v3/mapbox.mapbox-light/${z}/${x}/${y}.png",
        "http://c.tiles.mapbox.com/v3/mapbox.mapbox-light/${z}/${x}/${y}.png",
        "http://d.tiles.mapbox.com/v3/mapbox.mapbox-light/${z}/${x}/${y}.png"
    ], {
        attribution: "Tiles &copy; <a href='http://mapbox.com/'>MapBox</a> | " +
            "Data &copy; <a href='http://www.openstreetmap.org/'>OpenStreetMap</a> " +
            "and contributors, CC-BY-SA",
        sphericalMercator: true,
        wrapDateLine: true,
        transitionEffect: "resize",
        buffer: 1
    }); OpenLayers.Projection.addTransform("EPSG:32721", "EPSG:900913", OpenLayers.Layer.SphericalMercator.projectForward);
{% endblock %}
