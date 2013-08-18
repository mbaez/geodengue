/**
 * Sidebar de la pagina puntos de control
 * @clss
 * @author <a href="mailto:mxbg.py@gmail.com">Maximiliano Báez</a>
 * @name views.common.SideBarView
 */
define(["libs/jquery",
        "libs/underscore",
        "libs/backbone",
        //se incluye el template
        "text!templates/common/SidebarTmpl.html"],
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

            events : {
                "click #instalar" : "onInstalar",
                "click #recolectar" : "onRecolectar",
                "click #guardar" : "onGuardar"
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

            onInstalar : function(){
                this.trigger("on-instalar");
            },

            onRecolectar : function(){
                this.trigger("on-recolectar");
            },

            onGuardar : function(){
                this.trigger("on-guardar");
            }
        });
    }
);
