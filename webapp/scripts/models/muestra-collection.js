/**
 * Collection de lineas asociadas al cliente
 * Retorna la clase, no una instancia.
 *
 * @class
 * @author <a href="mailto:mxbg.py@gmail.com">Maximiliano Báez</a>
 * @name models.MuestraCollection
 * @see models.MuestraModel
 */
define(["backbone", "scripts/models/muestra-model"],
    function (Backbone, Model) {
        return Backbone.Collection.extend({
            model: Model,
            parse: GeoDengue.responseParser,
            /**
             * Url de la cual se obtiene el recurso.
             * @function
             * @name models.MuestraCollection#url
             * @retruns {String} Un cadena que representa la url del recurso
             */
            url: function () {
                return GeoDengue.RESTBaseUrl + '/muestras';
            },

            /**
             * Realiza un GET a /muestras para obtener la lista de todas las muestras
             * @function
             *
             * @name models.MuestraCollection#getAllMuestras
             */
            getAllMuestras: function (fetch) {
                //~ se sobrescribe la url
                var baseUrl = this.url();
                //~ se hace un clean de los atributos
                //se realiza el get
                if (fetch === true || typeof fetch == "undefined") {
                    this.fetch(GeoDengue.callback);
                }
            },

            /**
             * Realiza un GET a /muestras/1/resumen-poblacion
             * @function
             *
             * @name models.MuestraCollection#getReportePoblacion
             */
            getReportePoblacion: function () {
                //~ se sobrescribe la url
                var baseUrl = this.url();
                this.url = function () {
                    return baseUrl + "/1/resumen-poblacion";
                }
                this.fetch(GeoDengue.callback );
            }

        });
    });