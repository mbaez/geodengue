/**
 * Inicializador de la página de inicio
 * @class
 * @author <a href="mailto:mbaez@konecta.com.py">Maximiliano Báez</a>
 * @name controllers.Inicio
 */
define(['libs/jquery',
        'libs/underscore',
        'libs/backbone',
        //se importa el template html del page
        'text!pages/Inicio.html',
        //se incluyen los modulos gis necesarios
        'scripts/common/Style',
        //Se incluyen los Views
        "scripts/views/map/MapView",
        "scripts/views/common/NavbarView"
        ],
    function ($,_,Backbone,template,
        //se incluyen los modulos gis necesarios
        Style,
        //Se incluyen los Views
        MapView,NavbarView
    ) {
    "use strict";
    return Backbone.Page.extend({
        /**
         * Constructor de la clase
         * @function
         *
         * @name #inicialize
         */
        initialize : function(){
            this.render();
        },

         /**
         * Este metodo se encarga de contruir de incializar el page a
         * partir del template y cargar los views correspondientes.
         * @function
         *
         * @public
         * @name #render
         */
        render : function(){
            this.$el.html(template);
            var view = new NavbarView ({el : $("#appHeader")});
            //se retorna la referencia al view.
            return this;
        }
    });
});
