/**
 * Descripción del view
 * @class
 * @author <a href="mailto:mxbg.py@gmail.com">Maximiliano Báez</a>
 * @name nombre del view
 */
define(["text!templates/Tmpl.html"],
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
                this.data = options;
                this.collection.on('ready', this.render, this);
                this.collection.on('error', this.error, this);
                this.collection.on('fetch', this.loading, this);
                //si son models
                /**
                this.model.on('ready', this.render, this);
                this.model.on('error', this.error, this);
                this.model.on('fetch', this.loading, this);
                this.model.fetch(BaseCallback.fetch);
                */
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
