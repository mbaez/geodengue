/**
 * View para el mapa de openlayers.
 * @class
 * @author <a href="mailto:mxbg.py@gmail.com">Maximiliano Báez</a>
 * @name views.map.MapView
 */
define(["libs/jquery",
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
                this.initMap();
                return this;
            },
            /**
             * Este metodo se encarga de inicializar el mapa de OpenLayers
             * @function
             *
             * @public
             * @name views.map.MapView#initOpenLayersMap
             * @author <a href="mailto:mxbg.py@gmail.com">Maximiliano Báez</a>
             */
            initMap : function(){
                var maxExtent =  new OpenLayers.Bounds(DataSource.maxExtent);
                // se instancia el mapa
                var mapOptions = {
                    numZoomLevels : 21,
                    //~ controls : [],
                    maxExtend : maxExtent,
                    projection: DataSource.projectionCode,
                    units : 'm'
                };
                //inicializa el map
                this.map = new OpenLayers.Map("map", mapOptions);
                //se construye el base layer
                var baseLayer = new Layer.WMS({
                    name : DataSource.baseLayerConf,
                    base : true
                });
                this.map.addLayers(baseLayer);
                // Se añade el switch para las capas
                this.map.addControl(new OpenLayers.Control.LayerSwitcher());
                this.map.addControl(new OpenLayers.Control.CacheRead());
                this.map.addControl(new OpenLayers.Control.CacheWrite());
                //se realiza un zoom  para que centrar el mapa
                this.map.zoomToExtent(maxExtent);
            }
        });
    }
);
