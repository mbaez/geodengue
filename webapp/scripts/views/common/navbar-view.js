/**
 * Navbar principal de la aplicación, el navbar que se inicializa
 * corresponde al de <a href="http://twitter.github.io/bootstrap/components.html#navbar">
 * Bootstrap</a>.
 *
 * @class
 * @author <a href="mailto:mxbg.py@gmail.com">Maximiliano Báez</a>
 * @name views.common.NavbarView
 */
define(["text!templates/common/navbar-tmpl.html"],
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
             * @name #render
             */
            render: function () {
                var compTmpl = _.template(tmpl, {});
                this.$el.html(compTmpl);
                return this;
            }
        });
    }
);