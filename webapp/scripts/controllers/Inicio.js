/**
 * Inicializador de la página de inicio
 * @class
 * @author <a href="mailto:mbaez@konecta.com.py">Maximiliano Báez</a>
 * @name controllers.Inicio
 */
define([    'libs/JQuery/js/jquery',
            'libs/underscore',
            'libs/backbone',
            'scripts/common/Style',
            "scripts/views/map/MapView",
            "text!templates/map/MapTmpl.html"
        ], function ($,_,Backbone,
            Style,
            MapView, MapTmpl
        ) {
    "use strict";
    var thiz ={};

    thiz.interpolarIdw = function(metodo){
        var geojson_format = new OpenLayers.Format.GeoJSON();
        var vector_layer = new OpenLayers.Layer.Vector(metodo);
        thiz.mapPanel.map.addLayer(vector_layer);
        var style = new Style.Layer('/geodengue/sld/pixel.xml');
        vector_layer.styleMap = style.styleMap;
        $.ajax({
            type: "GET",
            cache: false,
            dataType:"text",
            url : '/geodengue/rest/larvitrampas/interpolar/'+metodo,
            success : function(data){
                vector_layer.addFeatures(geojson_format.read(data));
            }
        });
    };

    thiz.mapPanel = new MapView ({el : $("#incioContent")});
    thiz.interpolarIdw("voronoi");
    thiz.interpolarIdw("idw");
    // se retorna el json que contiene los metodos de los eventos
    return thiz;
});
