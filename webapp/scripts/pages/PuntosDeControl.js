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
        'text!pages/PuntosDeControl.html',
        //se incluyen los modulos gis necesarios
        "scripts/common/Layer",
        "scripts/common/Control",
        //se incluyen los views necesarios,
        "scripts/views/common/NavbarView",
        "scripts/views/map/PopupView",
        "scripts/views/map/MapView",
        "scripts/views/map/ToolbarView"
        ],
    function ($,_,Backbone,template,
        Layer, Control,
        //Se incluyen los Views
        NavbarView,PopupView,
        MapView, ToolbarView
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
            this.mapPanel = new MapView({el:$("#incioContent")});
            //se inicializa el toolbar de edición
            var toolbar = new ToolbarView ({el : $("#gisToolbar")});
            //se añaden los handlers de los eventos del toolbar
            toolbar.on('on-guardar', this.onGuardar, this);
            //se retorna la referencia al view.
            this.initLayers();
            this.initControls();
            return this;
        },

        initLayers : function(){
            this.puntosControl = new Layer.Vector(DataSource.puntosControlLayerConf);
            this.mapPanel.map.addLayer(this.puntosControl);
        },

        initControls : function(){
            var thiz = this;
            this.selectControl = new Control.SelectFeature(this.puntosControl);
            this.selectControl.onSelect = function(feature){
                console.log(feature);
                var view = new PopupView({
                    el: $("#none"),
                    feature : feature,
                    mapPanel :thiz.mapPanel,
                    fields : [
                     { label : "Codigo", id:"codigo", placeholder:"Ingrese el nombre"},
                     { label : "Id Muestra", id:"id_muestra", placeholder:"Ingrese el nombre"},
                     { label : "Descripcion", id:"descripcion", placeholder:"Ingrese el nombre"}
                     //~ { label : "Fecha", id:"fecha_instalacion", placeholder:"" , type : "date"}
                    ]
                });
            }
            this.mapPanel.map.addControl(this.selectControl);
            this.selectControl.activate();
        },

        onGuardar : function(){
            console.log("commit");
            this.puntosControl.commit();
        }
    });
});
