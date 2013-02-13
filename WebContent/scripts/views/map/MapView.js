/**
 * View para el mapa de openlayers.
 * @class
 * @author <a href="mailto:mxbg.py@gmail.com">Maximiliano Báez</a>
 * @name views.map.MapView
 */
define(["libs/JQuery/js/jquery",
        "libs/underscore",
        "libs/backbone",
        "libs/OpenLayers/OpenLayers",
        "scripts/common/Layer",
        "text!templates/map/MapTmpl.html"],
       function($,_,Backbone,OpenLayers,Layer,tmpl) {
        return Backbone.View.extend({
            /**
             * Constructor de la clase
             * @function
             *
             * @name views.map.MapView#initialize
             */
            initialize: function() {
                this.render();
            },
            events : {
            },
            /**
             * Este metodo se encarga de contruir el view a partir del
             * template.
             * @function
             *
             * @public
             * @name views.map.MapView#render
             * @author <a href="mailto:mxbg.py@gmail.com">Maximiliano Báez</a>
             */
            render: function () {
                var compTmpl = _.template(tmpl,{});
                this.$el.html(compTmpl);
                this.initOpenLayersMap();
                return this;
            },
            initOpenLayersMap : function(){
                var maxExtent = new OpenLayers.Bounds(
                    -8200730, 456498.1875,
                    -8190695.5, 465909.03125
                );
                // se instancia el mapa
                var mapOptions = {
                    numZoomLevels : 21,
                    projection : new OpenLayers.Projection(DataSource.projectionCode),
                    //maxResolution:  config.maxResolution,
                    maxExtend : maxExtent,
                    units : 'm'
                    //size : new OpenLayers.Size(150, 150)
                };
                //inicializa el map
                this.map = new OpenLayers.Map("map", mapOptions);
                var layersNames = [ DataSource.baseLayerConf];
                var baseLayer = new Layer.WMS({
                    names : layersNames,
                    base : true
                });
                this.map.addLayers(baseLayer);
                this.map.addLayers(new Layer.WMS({names:[DataSource.larvitrampasLayerConf]}));
                // Se añade el switch para las capas
                this.map.addControl(new OpenLayers.Control.Navigation());
                this.map.addControl(new OpenLayers.Control.LayerSwitcher());
                //this.map.addControl(new OpenLayers.Control.CacheRead());
                //this.map.addControl(new OpenLayers.Control.CacheWrite());
                this.map.zoomToExtent(maxExtent)
            }
        });
    }
);
