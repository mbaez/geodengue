
/**
 * Descripción del view
 * @class
 * @author <a href="mailto:mxbg.py@gmail.com">Maximiliano Báez</a>
 * @name nombre del view
 */
define(["libs/JQuery/js/jquery",
        "libs/underscore",
        "libs/backbone",
        //se incluye el template
        "text!templates/map/ToolbarTmpl.html"],
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
             * Conjunto de eventos y handlers asociados.
             */
            events : {
                'click #guardar' : 'onGuardar',
                'click #anadir' : 'onAnadir',
                'click #mover' : 'onMover',
                'click #eliminar' : 'onEliminar'
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
             * Este metodo se encarga disparar el evento <code>on-guardar<code>
             * iniciado desde el boton del toolbar
             * @function
             *
             * @public
             * @name #onGuardar
             */
            onGuardar : function(){
                this.trigger('on-guardar');
            },
            /**
             * Este metodo se encarga disparar el evento <code>on-anadir<code>
             * iniciado desde el boton del toolbar
             * @function
             *
             * @public
             * @name #onAnadir
             */
            onAnadir : function(){
                this.trigger('on-anadir');
            },
            /**
             * Este metodo se encarga disparar el evento <code>on-mover<code>
             * iniciado desde el boton del toolbar
             * @function
             *
             * @public
             * @name #onMover
             */
            onMover : function(){
                this.trigger('on-mover');
            },
            /**
             * Este metodo se encarga disparar el evento <code>on-eliminar<code>
             * iniciado desde el boton del toolbar
             * @function
             *
             * @public
             * @name #onEliminar
             */
            onEliminar : function(){
                this.trigger('on-eliminar');
            },
        });
    }
);
