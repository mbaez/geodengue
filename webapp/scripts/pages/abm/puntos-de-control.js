/**
 * Inicializador de la página de inicio
 * @class
 * @author <a href="mailto:mbaez@konecta.com.py">Maximiliano Báez</a>
 * @name controllers.Inicio
 */
define(['text!pages/abm/puntos-de-control.html',
        //se incluyen los modulos gis necesarios
        "openlayers-layer",
        "openlayers-control",
        //se incluyen los views necesarios,
        "scripts/views/common/navbar-view",
        "scripts/views/common/sidebar-view",
        "scripts/views/map/popup-view",
        "scripts/views/map/map-view",
        "scripts/views/map/toolbar-view"
        ],
    function (template,
        Layer, Control,
        //Se incluyen los Views
        NavbarView, SidebarView, PopupView,
        MapView, ToolbarView
    ) {
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
                var view = new NavbarView({
                    el: $("#appHeader")
                });
                var sideView = new SidebarView({
                    el: $("#puntosControlSide")
                });
                this.mapPanel = new MapView({
                    el: $("#incioContent")
                });

                //se añaden los handlers de los eventos del sidebar
                sideView.on('on-guardar', this.onGuardar, this);
                sideView.on('on-instalar', this.onInstalar, this);
                sideView.on('on-recolectar', this.onRecolectar, this);
                //se retorna la referencia al view.
                this.initLayers();
                this.initControls();
                return this;
            },

            /**
             * Inicializa los layers
             * @function
             *
             * @name #initLayers
             */
            initLayers: function () {
                this.puntosControl = new Layer.Vector(DataSource.puntosControlLayerConf);
                this.mapPanel.map.addLayer(this.puntosControl);
            },

            /**
             * Inicializa los controladores para la pagina de puntos de
             * control
             * @function
             *
             * @name #initControls
             */
            initControls: function () {
                var thiz = this;
                //se crea el controlador para poder modificar features
                this.selectControl = new Control.SelectFeature(this.puntosControl);
                //se anhade un popup para editar datos
                this.selectControl.onSelect = function (feature) {
                    console.log(feature);
                    var view = thiz.initSelectPopup(feature);
                }

                //se crea el controlador para crear un nuevo feature sobre el layer
                this.addControl = new Control.DrawPointFeature(this.puntosControl);
                //se anhade el popup para cargar los datos del feature
                this.addControl.featureAdded = function (feature) {
                    console.log(feature);
                    var view = thiz.initAddPopup(feature);
                }
                //se anhaden los controles al map
                this.mapPanel.map.addControl(this.selectControl);
                this.mapPanel.map.addControl(this.addControl);
                //se desactivan los controles
                this.selectControl.deactivate();
                this.addControl.deactivate();
            },

            /**
             * Metodo para crear el popup de modificacion de feature
             * @function
             *
             * @name #initSelectPopup
             *
             * @param {OpenLayers.Feature} feature El feature seleccionado
             * en el layer
             *
             */
            initSelectPopup: function (feature) {
                var popup = new PopupView({
                    el: $("#none"),
                    feature: feature,
                    mapPanel: this.mapPanel,
                    //el estado de un feature modificado debe ser 'UPDATE'
                    state: OpenLayers.State.UPDATE,
                    fields: [
                        {
                            label: "Id Muestra",
                            id: "id_muestras",
                            placeholder: "Ingrese el id de muestra"
                        },
                        {
                            label: "Cantidad",
                            id: "cantidad",
                            placeholder: "Ingrese la cantidad"
                        },
                        {
                            label: "Fecha",
                            id: "fecha_recoleccion",
                            placeholder: "",
                            type: "date"
                        }
                ]
                });
                return popup;
            },

            /**
             * Metodo para crear el popup de anhadir de feature
             * @function
             *
             * @name #initAddPopup
             *
             * @param {OpenLayers.Feature} feature El feature agregado
             * en el layer
             *
             */
            initAddPopup: function (feature) {
                var popup = new PopupView({
                    el: $("#none"),
                    feature: feature,
                    mapPanel: this.mapPanel,
                    //el estado de un feature modificado debe ser 'INSERT'
                    state: OpenLayers.State.INSERT,
                    fields: [
                        {
                            label: "Codigo",
                            id: "codigo",
                            placeholder: "Ingrese el nombre"
                        },
                        {
                            label: "Id Muestra",
                            id: "id_muestras",
                            placeholder: "Ingrese el id de muestra"
                        },
                        {
                            label: "Descripcion",
                            id: "descripcion",
                            placeholder: "Ingrese la descripcion"
                        },
                        {
                            label: "Fecha",
                            id: "fecha_instalacion",
                            placeholder: "",
                            type: "date"
                        }
                    ]
                });
                return popup;
            },

            /**
             * Metodo handler para el evento 'on-guardar' disparado desde el
             * boton guardar
             * @function
             *
             * @name #onGuardar
             *
             */
            onGuardar: function () {
                console.log("commit");
                this.puntosControl.commit();
            },

            /**
             * Metodo handler para el evento 'on-instalar' disparado desde el
             * boton instalar
             * @function
             *
             * @name #onInstalar
             *
             */
            onInstalar: function () {
                this.selectControl.deactivate();
                this.addControl.activate();
            },

            /**
             * Metodo handler para el evento 'on-recolectar' disparado desde el
             * boton recolectar
             * @function
             *
             * @name #onRecolectar
             *
             */
            onRecolectar: function () {
                this.addControl.deactivate();
                this.selectControl.activate();
            }

        });
    });