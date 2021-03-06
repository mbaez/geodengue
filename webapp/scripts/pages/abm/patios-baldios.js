/**
 * Inicializador de la página de inicio
 * @class
 * @author <a href="mailto:mxbg.py@gmail.com">Maximiliano Báez</a>
 * @name controllers.Inicio
 */
define(['text!pages/abm/patios-baldios.html',
        //se incluyen los modulos gis necesarios
        "openlayers-layer",
        "openlayers-control",
        //Se incluyen los Views
        "scripts/views/map/map-view",
        "scripts/views/common/navbar-view",
        "scripts/views/map/toolbar-view"
        ],
    function (template,
        //se incluyen los modulos gis necesarios
        Layer, Control,
        //Se incluyen los Views
        MapView, NavbarView, ToolbarView) {
        "use strict";
        return Backbone.Page.extend({
            /**
             * Tempalte de la página actual.
             * @type String
             * @field
             * @name template
             */
            template: template,

            /**
             * Constructor de la clase
             * @function
             *
             * @name #inicialize
             */
            initialize: function () {
                this.open();
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
            render: function () {
                //se inicializa el mapa
                this.mapPanel = new MapView({
                    el: $("#incioContent")
                });
                //se carga el navbar
                var view = new NavbarView({
                    el: $("#appHeader")
                });
                //se inicializa el toolbar de edición
                var toolbar = new ToolbarView({
                    el: $("#gisToolbar")
                });
                //se añaden los handlers de los eventos del toolbar
                toolbar.on('on-guardar', this.onGuardar, this);
                toolbar.on('on-anadir', this.onAnadir, this);
                toolbar.on('on-mover', this.onMover, this);
                toolbar.on('on-eliminar', this.onEliminar, this);
                //se cargan los layers
                this.initLayers();
                //se retorna la referencia al view.
                return this;
            },

            initLayers: function () {
                this.puntosControl = new Layer.Vector(DataSource.puntosControlLayerConf);
                //se crean los controles para las operaciones
                this.anadirControl = new Control.DrawPointFeature(this.puntosControl);
                this.moverControl = new Control.ModifyFeature(this.puntosControl);
                this.eliminarControl = new Control.DeleteFeature(this.puntosControl);
                //se añaden los controles al mapa
                this.mapPanel.map.addControl(this.anadirControl);
                this.mapPanel.map.addControl(this.moverControl);
                this.mapPanel.map.addControl(this.eliminarControl);
                //se añade el layer
                this.mapPanel.map.addLayer(this.puntosControl);
                //se desactivan los controles
                this.anadirControl.deactivate();
                this.moverControl.deactivate();
                this.eliminarControl.deactivate();
            },

            onAnadir: function () {
                this.anadirControl.activate();
                this.moverControl.deactivate();
                this.eliminarControl.deactivate();
            },

            onMover: function () {
                this.anadirControl.deactivate();
                this.moverControl.activate();
                this.eliminarControl.deactivate();
            },

            onEliminar: function () {
                this.anadirControl.deactivate();
                this.moverControl.deactivate();
                this.eliminarControl.activate();
            },

            onGuardar: function () {
                console.log("commit");
                this.puntosControl.commit();
            }
        });
    });
