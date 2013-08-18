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
        'text!pages/Procesos.html',
        //se incluyen los modulos gis necesarios
        "scripts/common/Layer",
        //se incluyen los models necesarios,
        "scripts/models/MuestraModel",
        //se incluyen los views necesarios,
        "scripts/views/common/NavbarView",
        "scripts/views/common/SidebarView",
        "scripts/views/common/ProcesosFormView",
        "scripts/views/map/MapView",
        ],
    function ($,_,Backbone,template,
        Layer,
        // models
        MuestraModel,
        //Se incluyen los Views
        NavbarView,SidebarView,
        ProcesosFormView, MapView
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
            var view = new NavbarView ({el:$("#appHeader")});
            var sideView = new SidebarView ({el:$("#puntosControlSide")});
            this.mapPanel = new MapView({el:$("#incioContent")});
            var form = new ProcesosFormView({el:$("#form")});

            this.initLayers();

            //se añade el handler del view
            form.on("on-execute", this.onEjecutarProceso, this);

            //se retorna la referencia al view.
            return this;
        },

        onEjecutarProceso : function(){
            this.model = new MuestraModel();
            this.model.set({idMuestra : 1});
            // se añade el handler del model
            this.model.on('ready', this.onProcesoReady, this);
            this.model.on('error', this.error, this);
            // se hace el post
            this.model.save(null ,GeoDengue.callback);
        },

        onProcesoReady : function(){
            $(".btn").button("reset");
            var conf = $.extend({}, DataSource.rasterLayerConf);
            conf.name = this.model.get("layer");
            var raster = new Layer.WMS(conf);
            this.map.addLayers(raster);
        },

        error : function(){
            console.log("Error");
        },

         /**
         * Inicializa los layers
         * @function
         *
         * @name #initLayers
         */
        initLayers : function(){
            this.puntosControl = new Layer.Vector(DataSource.puntosControlLayerConf);
            this.mapPanel.map.addLayer(this.puntosControl);
        }
    });
});
