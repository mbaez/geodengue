/**
 * Navbar principal de la aplicación, el navbar que se inicializa
 * corresponde al de <a href="http://twitter.github.io/bootstrap/components.html#navbar">
 * Bootstrap</a>.
 *
 * @class
 * @author <a href="mailto:mxbg.py@gmail.com">Maximiliano Báez</a>
 * @name views.common.NavbarView
 */
define(["libs/jquery",
        "libs/underscore",
        "libs/backbone",
        //se incluye el template
        "text!templates/common/NavbarTmpl.html"],
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
