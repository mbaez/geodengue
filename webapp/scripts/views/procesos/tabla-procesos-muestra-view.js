/**
 * Descripción del view
 * @class
 * @author <a href="mailto:correo@autor">Nombre del autor</a>
 * @name nombre del view
 */
define(["text!templates/procesos/tabla-procesos-muestra-tmpl.html",
        "scripts/models/muestra-model",
        "scripts/models/muestra-collection"],
    function (tmpl, MuestraModel, MuestraCollection) {
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
                "change select#list-procesos-muestra": "onChange",
                "click #calcular-foco": "getInterpolationLayer"
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
                this.data = options;
                this.loading();
                this.collection = new MuestraCollection();
                this.collection.on('ready', this.render, this);
                this.collection.on('error', this.error, this);
                this.collection.getProcesosByMuestra(options.muestra);
            },

            /**
             * Este metodo se encarga de contruir el view en el estado de loading
             * @function
             *
             * @public
             * @name #loading
             */
            loading: function () {
                var compTmpl = _.template(tmpl, {});
                this.$el.html(compTmpl);
                return this;
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
                var data = {};
                data.collection = this.collection.toJSON();
                var compTmpl = _.template(tmpl, {
                    data: data
                });
                this.$el.html(compTmpl);
                //se dispara el evento
                $('#list-procesos-muestra').trigger('change');
                return this;
            },

            /**
             * Se encarga de centrar el mapa cuando se hace click en la tabla de puntos de
             * control.
             * @function
             *
             * @name #onChange
             */
            onChange: function (events) {
                //se desactiva el item anterior
                var codigo = $("#list-procesos-muestra").val();
                var $select = $("#select-dias");
                $select.removeAttr("disabled");
                $select.html("");
                codigo = codigo.trim();
                //se hace active la fila
                var proceso = this.collection.where({
                    "codigo": codigo
                });

                //se valida el resultado
                if (proceso.length == 0) {
                    var $el = $("<option></option>");
                    $el.text("No existen datos!!");
                    $select.attr("disabled", true);
                    $select.append($el);
                    return;
                }
                this.proceso = proceso[0].toJSON();
                for (var i = this.proceso.min; i <= this.proceso.max; i++) {
                    var $el = $("<option></option>");
                    $el.text(i);
                    $select.append($el);
                }
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
                $("#calcular-foco").button("loading");
                var data = {};
                data.dia = dia.trim();
                data.id_muestra = this.proceso.id_muestra;
                data.codigo = this.proceso.codigo;

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
                $("#calcular-foco").button("reset");
                this.trigger('on-ready-layer', this.model.toJSON());
            }
        });
    });