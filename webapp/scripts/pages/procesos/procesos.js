/**
 * Inicializador de la página de inicio
 * @class
 * @author <a href="mxbg.py@gmail.com">Maximiliano Báez</a>
 */
define(['text!pages/procesos/procesos.html',
        //se incluyen los modulos gis necesarios
        "openlayers-layer",
        'openlayers-style',
        //se incluyen los models necesarios,
        "scripts/models/muestra-model",
        //se incluyen los views necesarios,
        "scripts/views/map/map-view",
        "scripts/views/common/navbar-view",
        "scripts/views/procesos/procesos-form-view",
        "scripts/views/procesos/muestras-box-view",
        ],
    function (template,
        Layer, Style,
        // models
        MuestraModel,
        //Se incluyen los Views
        MapView, NavbarView, ProcesosFormView, MuestrasBoxView) {
        "use strict";
        return Backbone.Page.extend({
            /**
             * Tempalte de la página actual.
             * @type String
             * @field
             * @name template
             */
            template: template,
            /**
             * Constructor de la clase
             * @function
             *
             * @name #inicialize
             */
            initialize: function () {
                this.open();
                this.render();
            },

            /**
             * Este metodo se encarga de contruir de incializar el page a
             * partir del template y cargar los views correspondientes.
             * @function
             *
             * @public
             * @name #render
             */
            render: function () {
                this.style = new Style.Layer('/geodengue/sld/pixel.xml');
                var view = new NavbarView({
                    el: $("#appHeader")
                });
                this.mapPanel = new MapView({
                    el: $("#incioContent")
                });
                var form = new ProcesosFormView({
                    el: $("#form")
                });

                var view = new MuestrasBoxView({
                    el: $("#muestras-box"),
                    map: this.mapPanel.map
                });
                //se añade el handler del view
                form.on("on-execute", this.onEjecutarProceso, this);
                //se retorna la referencia al view.
                return this;
            },
            /**
             * Este método se encarga de manejar el evento 'on-execute' disparado
             * desde el from view.
             * @function
             *
             * @name #onEjecutarProceso
             * @author <a href="mxbg.py@gmail.com">Maximiliano Báez</a>
             * @params {Object}data
             * @config {String}proceso El nombre del proceso a iniciar
             */
            onEjecutarProceso: function (data) {
                this.model = new MuestraModel();
                this.model.set({
                    idMuestra: 1
                });
                // se obtiene la url base del model
                var urlBase = this.model.url();
                //se sobreescribe la url para invocar al proceso correspondiente
                this.model.url = function () {
                    return urlBase + "/" + data.proceso;
                }
                // se añade el handler del model
                this.model.on('ready', this.onProcesoReady, this);
                this.model.on('error', this.error, this);
                // se hace el post
                this.model.save(null, GeoDengue.callback);
            },

            /**
             * Este método se encarga de manejar el evento 'ready' de la
             * petición realizada con el model.
             *
             * @function
             *
             * @name #onProcesoReady
             * @author <a href="mxbg.py@gmail.com">Maximiliano Báez</a>
             */
            onProcesoReady: function () {
                //se reinicia los botones
                $(".btn").button("reset");
                var conf = $.extend({}, DataSource.rasterLayerConf);
                conf.name = this.model.get("layer");
                var geojsonFormat = new OpenLayers.Format.GeoJSON();
                var vectorLayer = new OpenLayers.Layer.Vector();
                vectorLayer.styleMap = this.style.styleMap;
                this.mapPanel.map.addLayer(vectorLayer);
                var data = this.model.get("mosquitos");
                if (typeof data != 'undefined') {
                    vectorLayer.addFeatures(geojsonFormat.read(data));
                }
                //se construye el raster layer
                var raster = new Layer.WMS([conf]);
                // se añade el layer al mapa
                this.mapPanel.map.addLayers(raster);
            },

            /**
             * Este método se encarga de manejar el evento 'error' de la
             * petición realizada con el model.
             *
             * @function
             *
             * @name #error
             * @author <a href="mxbg.py@gmail.com">Maximiliano Báez</a>
             */
            error: function () {
                $(".btn").button("reset");
                console.error("Error");
            }
        });
    });