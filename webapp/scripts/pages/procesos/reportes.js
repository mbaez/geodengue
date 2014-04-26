/**
 * Inicializador de la página de inicio
 * @class
 * @author <a href="mxbg.py@gmail.com">Maximiliano Báez</a>
 */
define(['text!pages/procesos/reportes.html',
        //se incluyen los views necesarios,
        "scripts/views/common/navbar-view",
        "scripts/views/procesos/poblacion-chart-view"
        ],
    function (template,
        //Se incluyen los Views
        NavbarView, PoblacionChartView) {
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
                var chart = new PoblacionChartView({
                    el: $("#incioContent")
                });
                //se retorna la referencia al view.
                return this;
            }
        });
    });