/**
 * Descripción del view
 * @class
 * @author <a href="mailto:mxbg.py@gmail.com">Maximiliano Báez</a>
 * @name nombre del view
 */
define(["text!templates/procesos/muestras-box-tmpl.html",
        "openlayers-style",
        "scripts/models/muestra-model"
       ],
    function (tmpl, Style, MuestraModel) {
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
            events: {
                "click #centrar-mapa": "onCentrarMapa",
                "onChange #select-dias": "getInterpolationLayer"
            },
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
                this.params = options;
                this.render(options);
            },

            /**
             * Este metodo se encarga de contruir el view a partir del
             * template.
             * @function
             *
             * @public
             * @name #render
             */
            render: function (options) {
                var compTmpl = _.template(tmpl, {
                    data: options
                });
                this.$el.html(compTmpl);
                return this;
            },

            /**
             * Inicializa los layers
             * @function
             *
             * @name #initLayers
             */
            initLayers: function () {
                var thiz = this;
                $("body").on('on-layer-ready', function (event) {
                    thiz.buildTable(event.layer);
                });
                var style = new Style.Layer('/geodengue/sld/pixel.xml');
                this.puntosControl = new Layer.Vector(DataSource.puntosControlLayerConf);
                this.puntosControl.styleMap = style.styleMap;
                this.params.map.addLayer(this.puntosControl);
            },

            /**
             * Se encarga de hacer un post para obtener el layer correspondiente
             * a la muestra, proceso y día
             * @function
             *
             * @name #getInterpolationLayer
             */
            getInterpolationLayer: function () {
                var dia = $("#select-dias").val();
                var data = {};
                data.dia = dia.trim();
                data.id_muestra = this.params.proceso.id_muestra;
                data.codigo = this.params.proceso.codigo;

                this.model = new MuestraModel();
                // se añade el handler del model
                this.model.on('ready', this.onReadyLayer, this);
                this.model.on('error', this.error, this);
                // se hace el post
                this.model.getLayerFoco(data);
            },
            /**
             * Se encarga de disparar el evento `on-ready-layer`
             * @function
             *
             * @name #onReadyLayer
             */
            onReadyLayer: function () {
                this.trigger('on-ready-layer', this.model.toJSON());
            },

            /**
             * Se encarga de centrar el mapa con zoom a la extensión del layer.
             * @function
             *
             * @name #onCentrarMapa
             */
            onCentrarMapa: function () {
                var bounds = this.puntosControl.getDataExtent();
                this.params.map.zoomToExtent(bounds);
            }

        });
    }
);
