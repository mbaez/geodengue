
/**
 * Descripción del view
 * @class
 * @author <a href="mailto:correo@autor">Nombre del autor</a>
 * @name nombre del view
 */
define(["libs/backbone",
        //se incluye el template
        "text!templates/Tmpl.html"],
    function($,_,Backbone,tmpl) {
        return Backbone.View.extend({
            /**
             * Constructor de la clase
             * @function
             *
             * @name #inicialize
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
             * @name #render
             */
            render: function () {
                var compTmpl = _.template(tmpl,{});
                this.$el.html(compTmpl);
                return this;
            }
        });
    }
);
