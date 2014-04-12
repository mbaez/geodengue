/**
 * Descripción del view
 * @class
 * @author <a href="mailto:correo@autor">Nombre del autor</a>
 * @name nombre del view
 */
define(["text!templates/procesos/muestras-box-tmpl.html", 'openlayers-style',
        "scripts/models/muestra-collection", "scripts/views/common/search-view"],
    function (tmpl, Style, MuestraCollection, SearchView) {
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
                "click a.list-group-item": "onClick"
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
                this.render();
            },

            /**
             * Este metodo se encarga de contruir el view a partir del
             * template.
             * @function
             *
             * @public
             * @name #render
             */
            render: function () {
                var compTmpl = _.template(tmpl, {});
                this.$el.html(compTmpl);
                this.getAllMuestras();
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
                //se añade el handler
                view.on("on-search", this.initLayers, this);
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
             * Se encarga de centrar el mapa cuando se hace click en la tabla de puntos de
             * control.
             * @function
             *
             * @name #onClick
             */
            onClick: function (events) {
                //se desactiva el item anterior
                $(".list-group-item.active").removeClass("active");
                var $target = $(events.target);
                //se obtiene el fid del elemento
                var fid = $target.data("fid");
                //se obtiene el featrue a partir del fid del feature
                var p = this.puntosControl.getFeatureByFid(fid);
                //se centra el mapa
                var lonlat = new OpenLayers.LonLat(p.geometry.x, p.geometry.y);
                this.params.map.setCenter(lonlat, 20);
                //se hace active la fila
                $target.addClass("active");
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
            },
            /**
             * Se encarga de construir la tabla con la lista de puntos de control pertenecientes
             * a la muestra.
             * @function
             *
             * @name #buildTable
             * @param {OpenLayers.Layer.Vector}layer el la referencia al layer de puntos de control
             */
            buildTable: function (layer) {
                this.onCentrarMapa();
                var $target = $("#lista-features");
                for (var i = 0; i < layer.features.length; i++) {
                    var $tmpl = this.putAttributes(layer.features[i].data, $("#tmpl-row a"));
                    $tmpl.data("fid", layer.features[i].fid);
                    $target.append($tmpl);
                }
            }

        });
    }
);