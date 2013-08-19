/**
 * Inicializador de la página de inicio
 * @class
 * @author <a href="mxbg.py@gmail.com">Maximiliano Báez</a>
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
        "scripts/views/common/ProcesosFormView",
        "scripts/views/map/MapView",
        ],
    function ($,_,Backbone,template,
        Layer,
        // models
        MuestraModel,
        //Se incluyen los Views
        NavbarView, ProcesosFormView, MapView
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
            this.mapPanel = new MapView({el:$("#incioContent")});
            var form = new ProcesosFormView({el:$("#form")});
            //se añade el handler del view
            form.on("on-execute", this.onEjecutarProceso, this);
            //se inicializa los layers
            this.initLayers();
            //se retorna la referencia al view.
            return this;
        },
         /**
         * Este método se encarga de manejar el evento 'on-execute' disparado
         * desde el from view.
         * @function
         *
         * @name #onEjecutarProceso
         * @author <a href="mxbg.py@gmail.com">Maximiliano Báez</a>
         * @params {Object}data
         * @config {String}proceso El nombre del proceso a iniciar
         */
        onEjecutarProceso : function(data){
            this.model = new MuestraModel();
            this.model.set({idMuestra : 1});
            // se obtiene la url base del model
            var urlBase = this.model.url();
            //se sobreescribe la url para invocar al proceso correspondiente
            this.model.url = function (){
                return urlBase +"/" + data.proceso;
            }
            // se añade el handler del model
            this.model.on('ready', this.onProcesoReady, this);
            this.model.on('error', this.error, this);
            // se hace el post
            this.model.save(null, GeoDengue.callback);
        },

         /**
         * Este método se encarga de manejar el evento 'ready' de la
         * petición realizada con el model.
         *
         * @function
         *
         * @name #onProcesoReady
         * @author <a href="mxbg.py@gmail.com">Maximiliano Báez</a>
         */
        onProcesoReady : function(){
            //se reinicia los botones
            $(".btn").button("reset");
            var conf = $.extend({}, DataSource.rasterLayerConf);
            conf.name = this.model.get("layer");
            //se construye el raster layer
            var raster = new Layer.WMS([conf]);
            // se añade el layer al mapa
            this.mapPanel.map.addLayers(raster);
        },

         /**
         * Este método se encarga de manejar el evento 'error' de la
         * petición realizada con el model.
         *
         * @function
         *
         * @name #error
         * @author <a href="mxbg.py@gmail.com">Maximiliano Báez</a>
         */
        error : function(){
            $(".btn").button("reset");
            console.error("Error");
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
