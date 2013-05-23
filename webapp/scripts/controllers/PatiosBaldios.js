/**
 * Inicializador de la página de inicio
 * @class
 * @author <a href="mailto:mbaez@konecta.com.py">Maximiliano Báez</a>
 * @name controllers.Inicio
 */
define(['libs/JQuery/js/jquery',
        'libs/underscore',
        'libs/backbone',
        //se importa el template html del page
        'text!pages/PatiosBaldios.html',
        //se incluyen los modulos gis necesarios
        "scripts/common/Layer",
        "scripts/common/Control",
        //Se incluyen los Views
        "scripts/views/map/MapView",
        "scripts/views/common/NavbarView"
        ],
    function ($,_,Backbone,template,
        //se incluyen los modulos gis necesarios
        Layer, Control,
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
            this.mapPanel = new MapView ({el : $("#incioContent")});
            var view = new NavbarView ({el : $("#appHeader")});
            this.initLayerPuntosControl();
            //se retorna la referencia al view.
            return this;
        },
        events : {
            "click .btn" : 'save'
        },

        initLayerPuntosControl : function(){
            this.puntosControl = new Layer.Vector(DataSource.puntosControlLayerConf);
            var drawControl = new Control.DrawPointFeature(this.puntosControl);
            this.mapPanel.map.addControl(drawControl);
            this.mapPanel.map.addLayer(this.puntosControl);
            drawControl.activate();
        },

        save : function(){
            console.log("commit");
            this.puntosControl.commit();
        }
    });
});

