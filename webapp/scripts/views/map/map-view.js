/**
 * View para el mapa de openlayers.
 * @class
 * @author <a href="mailto:mxbg.py@gmail.com">Maximiliano Báez</a>
 * @name views.map.MapView
 */
define(["OpenLayers", "openlayers-layer", "text!templates/map/map-tmpl.html"],
    function (OpenLayers, Layer, tmpl) {
        return Backbone.View.extend({
            /**
             * Constructor de la clase
             * @function
             *
             * @name #initialize
             * @param options {Object}
             */
            initialize: function (options) {
                //si tiene permitido cargar este view
                this.on('allowed', this.allowed, this);
                this.setup(options);
            },
            /**
             * Json que mapea los eventos a los handlers
             * @field
             * @type Object
             * @name #events
             */
            events: {},
            /**
             * Si posee los permisos para cargar el view, se configuran
             * los eventos y se realizan las peticiones para obtener los
             * datos.
             * @function
             *
             * @name #allowed
             * @param {Object}options
             * @config {String}el la referencia al dom donde se renderiza
             *          el view.
             */
            allowed: function (options) {
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
                var compTmpl = _.template(tmpl, {});
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
            initMap: function () {
                var maxExtent = new OpenLayers.Bounds(DataSource.maxExtent);
                var projection = new OpenLayers.Projection(DataSource.projectionCode);
                var center = new OpenLayers.LonLat(DataSource.center);
                // se instancia el mapa
                var mapOptions = {
                    numZoomLevels: 21,
                    maxExtend: maxExtent,
                    //projection: "EPSG:900913",
                    //displayProjection : projection,
                    projection : projection,
                    units: 'm'
                };
                //inicializa el map
                this.map = new OpenLayers.Map("map", mapOptions);
                //se construye el base layer
                var osmLayer = new OpenLayers.Layer.OSM("Simple OSM");
                var baseLayer = new Layer.WMS(DataSource.baseLayerConf);
                //this.map.addLayer(osmLayer);
                this.map.addLayers(baseLayer);
                // Se añade el switch para las capas
                this.map.addControl(new OpenLayers.Control.LayerSwitcher());
                this.map.addControl(new OpenLayers.Control.CacheRead());
                this.map.addControl(new OpenLayers.Control.CacheWrite());
                this.map.addControl(new OpenLayers.Control.ScaleLine());
                this.map.setCenter(center, 12);
            }
        });
    }
);