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
        "scripts/models/muestra-collection",
        //se incluyen los views necesarios,
        "scripts/views/map/map-view",
        "scripts/views/common/navbar-view",
        "scripts/views/common/search-view",
        "scripts/views/procesos/procesos-form-view",
        "scripts/views/procesos/tabla-procesos-muestra-view",
        ],
    function (template,
        Layer, Style,
        // models
        MuestraModel, MuestraCollection,
        //Se incluyen los Views
        MapView, NavbarView, SearchView,
        ProcesosFormView, ProcesosMuestraView) {
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
                this.pointStyle = new Style.Layer('/geodengue/sld/point.xml');
                var view = new NavbarView({
                    el: $("#appHeader")
                });
                this.mapPanel = new MapView({
                    el: $("#focos-infestacion")
                });

                var view = this.getAllMuestras();

                this.form = new ProcesosFormView({
                    el: $("#form")
                });

                //se añade el handler del view
                this.form.on("on-crear-proceso", this.onCrearProceso, this);
                view.on("on-search", this.buildTablaProcesos, this);
                //se retorna la referencia al view.
                return this;
            },
            /**
             * Se ecarga de obtener todas las muestras disponibles
             * @function
             *
             * @name #getAllMuestras
             */
            getAllMuestras: function () {
                this.collection = new MuestraCollection();
                var view = new SearchView({
                    el: $("#selector-muestras"),
                    collection: this.collection,
                    attr: "descripcion",
                    placeholder: "Muestras"
                });
                return view;
            },

            /**
             * Se ecarga de obtener todas los porocesos iniciados para una muestra
             * @function
             *
             * @name #buildTablaProcesos
             */
            buildTablaProcesos: function (muestra) {
                this.muestra = muestra;
                if (typeof this.procesoView != "undefined") {
                    this.procesoView.close();
                }

                this.procesoView = new ProcesosMuestraView({
                    el: $("#lista-procesos"),
                    muestra: muestra
                });

                //this.procesoView.on("on-select-proceso", this.buildProcesoDia, this);
                this.procesoView.on("on-ready-layer", this.addRasterLayer, this);
                this.procesoView.on("on-change", this.addVectorLayer, this);
            },


            /**
             * Añade una capa raster al mapa.
             *
             * @function
             *
             * @name #addRasterLayer
             * @author <a href="mxbg.py@gmail.com">Maximiliano Báez</a>
             */
            addRasterLayer: function (layer) {
                var conf = $.extend({}, DataSource.rasterLayerConf);
                conf.name = layer.layer_name;
                var raster = new Layer.WMS([conf]);
                // se añade el layer al mapa
                this.mapPanel.map.addLayers(raster);
            },

            /**
             * Inicializa los layers
             * @function
             *
             * @name #addVectorLayer
             * @params data
             * @config {String}codigo
             * @config {Number}dia
             * @config {Number}id_muestra
             */
            addVectorLayer: function (data) {
                var filterCod = new OpenLayers.Filter.Comparison({
                    type: OpenLayers.Filter.Comparison.EQUAL_TO,
                    property: "codigo",
                    value: data.codigo
                });

                var filterDia = new OpenLayers.Filter.Comparison({
                    type: OpenLayers.Filter.Comparison.EQUAL_TO,
                    property: "dia",
                    value: data.dia
                });

                var filterMuestra = new OpenLayers.Filter.Comparison({
                    type: OpenLayers.Filter.Comparison.EQUAL_TO,
                    property: "id_muestra",
                    value: data.id_muestra
                });

                var filter = new OpenLayers.Filter.Logical({
                    type: OpenLayers.Filter.Logical.AND,
                    filters: [filterCod, filterDia]
                });
                
                var configAdultos = $.extend({}, DataSource.eventosAdultosLayerConf);
                configAdultos.filter = filter;
                configAdultos.displayName = 'adultos-' + data.dia + "-" + data.codigo;

                var configInmaduras = $.extend({}, DataSource.eventosInmadurasLayerConf);
                configInmaduras.filter = filter;
                configInmaduras.displayName = 'inmaduras-' + data.dia + "-" + data.codigo;

                var adultos = new Layer.Vector(configAdultos);
                adultos.styleMap = this.pointStyle.styleMap;
                
                this.adultos = adultos
                var thiz = this;
                this.adultos.events.register('loadend', this.adultos, function (evt) {
                    if(thiz.adultos.features.length > 0){
                        thiz.mapPanel.map.zoomToExtent(thiz.adultos.getDataExtent());
                    }
                });
                
                var inmaduras = new Layer.Vector(configInmaduras);
                inmaduras.styleMap = this.style.styleMap;
                this.mapPanel.map.addLayers([adultos, inmaduras]);
                
                GeoDengue.map = this.mapPanel.map;

            },
            /**
             * Este método se encarga de manejar el evento 'on-execute' disparado
             * desde el from view.
             * @function
             *
             * @name #onCrearProceso
             * @author <a href="mxbg.py@gmail.com">Maximiliano Báez</a>
             * @params {Object}data
             * @config {String}nombre El nombre del proceso a iniciar
             */
            onCrearProceso: function (data) {
                if (typeof this.muestra == "undefined") {
                    return;
                }
                data.id_muestra = this.muestra.codigo;
                this.model = new MuestraModel();
                // se añade el handler del model
                this.model.on('ready', this.onProcesoReady, this);
                this.model.on('error', this.error, this);
                // se hace el post
                this.model.crearProceso(data);
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
                $("#crear-proceso").button("reset");
            }
        });
    });
