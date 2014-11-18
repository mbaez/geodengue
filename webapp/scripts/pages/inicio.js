/**
 * Inicializador de la página de inicio
 * @class
 * @author <a href="mailto:mxbg.py@gmail.com">Maximiliano Báez</a>
 * @name controllers.Inicio
 */
define([ //se importa el template html del page
        'text!pages/inicio.html',
        //se incluyen los modulos gis necesarios
        'openlayers-style',
        //Se incluyen los Views
        "scripts/views/common/navbar-view"
        ],
    function (template,
        //se incluyen los modulos gis necesarios
        Style,
        //Se incluyen los Views
        NavbarView) {
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
                //se retorna la referencia al view.
                return this;
            }
        });
    });
