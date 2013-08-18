/**
 * Sidebar de la pagina puntos de control
 * @clss
 * @author <a href="mailto:mxbg.py@gmail.com">Maximiliano Báez</a>
 */
define(["libs/jquery",
        "libs/underscore",
        "libs/backbone",
        //se incluye el template
        "text!templates/common/ProcesosFormTmpl.html"],
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
             * Json que mapea los eventos a los handlers
             * @field
             * @type Object
             * @name #events
             */
            events : {
                "click #procesosForm .btn" : "onClick",
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
            },

            /**
             * @function
             *
             * @author <a href="mailto:mxbg.py@gmail.com">Maximiliano Báez</a>
             * @name #onClick
             */
            onClick : function(){
                $(".btn").button("loading");
                this.trigger("on-execute");
            }
        });
    }
);
