/**
 * Sidebar de la pagina puntos de control
 * @clss
 * @author <a href="mailto:mxbg.py@gmail.com">Maximiliano Báez</a>
 */
define(["text!templates/procesos/procesos-form-tmpl.html"],
    function (tmpl) {
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
                "click #crear-proceso": "onClick",
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
                $("#process-info").hide();
                return this;
            },

            /**
             * Dispara el evento   'on-execute' cuando se hace click en uno de los botones
             * @function
             *
             * @author <a href="mailto:mxbg.py@gmail.com">Maximiliano Báez</a>
             * @name #onClick
             */
            onClick: function (event) {
                var nombre = $("#nombre-proceso").val();
                if (nombre == null || nombre.length == 0) {
                    $("#nombre-proceso").parent().addClass("has-error");
                    return;
                }
                $("#nombre-proceso").parent().removeClass("has-error");
                $("#crear-proceso").button("loading");
                // se dispara el evento
                this.trigger("on-crear-proceso", {
                    nombre: nombre
                });
            },

            /**
             * Este metodo se encarga de contruir el panel adicional con el resumen del proceso
             * @function
             *
             * @public
             * @name #showProcessInfo
             */
            showProcessInfo: function (resumen) {
                $("#process-info").show();
                this.putAttributes(resumen);
                for (var estado in resumen) {
                    this.putAttributes(resumen[estado], estado);
                }
            }
        });
    }
);