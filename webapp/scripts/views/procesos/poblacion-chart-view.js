/**
 * Descripción del view
 * @class
 * @author <a href="mailto:correo@autor">Nombre del autor</a>
 * @name nombre del view
 */
define(["text!templates/procesos/poblacion-chart-tmpl.html", 'highcharts',
        //se incluyen los models necesarios,
        "scripts/models/muestra-collection"],
    function (tmpl, Highcharts, MuestraCollection) {
        return Backbone.View.extend({
            /**
             * Constructor de la clase
             * @function
             *
             * @name #initialize
             * @param options {Object}
             */
            initialize: function (options) {
                //si tiene permitido cargar este view
                this.on('allowed', this.allowed, this);
                this.setup(options);
            },
            /**
             * Json que mapea los eventos a los handlers
             * @field
             * @type Object
             * @name #events
             */
            events: {},
            /**
             * Si posee los permisos para cargar el view, se configuran
             * los eventos y se realizan las peticiones para obtener los
             * datos.
             * @function
             *
             * @name #allowed
             * @param {Object}options
             * @config {String}el la referencia al dom donde se renderiza
             *          el view.
             */
            allowed: function (options) {
                this.data = options;
                this.collection = new MuestraCollection();
                this.collection.on('ready', this.render, this);
                this.collection.on('error', this.error, this);
                this.collection.getReportePoblacion();

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
                var compTmpl = _.template(tmpl, {});
                this.$el.html(compTmpl);
                this.initChart();
                return this;
            },

            initChart: function () {
                var config = {};
                config.title = {
                    text: '',
                    x: -20 //center
                };
                config.subtitle = {
                    text: 'Source: geodengue',
                    x: -20
                };
                config.xAxis = {
                    categories: this.collection.pluck('dia'),
                };
                config.yAxis = {
                    title: {
                        text: 'Individuos'
                    },
                    plotLines: [{
                        value: 0,
                        width: 1,
                        color: '#808080'
                        }]
                };
                config.yAxis = {
                    min: 0
                };
                config.tooltip = {
                    valueSuffix: ' Individuos'
                };
                config.legend = {
                    layout: 'vertical',
                    align: 'right',
                    verticalAlign: 'middle',
                    borderWidth: 0
                };

                config.series = [{
                    name: 'Poblacion',
                    data: this.collection.pluck('count')
                }, {
                    name: 'Población inicial',
                    data: this.collection.pluck('inicial')
                }, {
                    name: 'Poblacion Nueva',
                    data: this.collection.pluck('nueva')
                }];

                $('#poblacion-chart').highcharts(config);
            }
        });
    }
);