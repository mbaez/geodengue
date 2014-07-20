/**
 * Definición del modelo de un proceso
 * Retorna la clase, no una instancia.
 *
 * @class
 * @author <a href="mailto:mxbg.py@gmail.com">Maximiliano Báez</a>
 * @name models.MuestraModel
 */
define(["backbone"], function (Backbone) {
    /**
     * Constructor de la clase
     * @function
     *
     * @name models.MuestraModel#inicialize
     */
    return Backbone.Model.extend({
        /**
         * Url de la cual se obtiene el recurso.
         * @function
         * @name models.MuestraModel#url
         * @retruns {String} Un cadena que representa la url del recurso
         */
        url: function () {
            return GeoDengue.RESTBaseUrl + "/muestras/" +
                this.get("id_muestra");
        },
        /**
         * Se encarga de realizar un post a /muestras/<id_muestra>/procesos/<codigo>
         * @function
         * @name models.MuestraModel#executeProcess
         */
        crearProceso: function (data) {
            this.set(data);
            // se obtiene la url base del model
            var urlBase = this.url();
            //se sobreescribe la url para invocar al proceso correspondiente
            this.url = function () {
                return urlBase + "/procesos/" + this.get("nombre");
            }
            this.save(null, GeoDengue.callback);
        },
        /**
         * Se encarga de realizar
         * POST /muestras/<id_muestra>/procesos/<codigo>/dias/<dia>/foco
         * @function
         * @params {Object}data
         * @config {Sting}codigo el codigo del proceso
         * @config {Number}dia el dia de evaluacion
         * @config {Number}id_muestra el identificador de la muestra
         * @name models.MuestraModel#executeProcess
         */
        getLayerFoco: function (data) {
            this.set(data);
            var urlBase = this.url();

            //se sobreescribe la url para invocar al proceso correspondiente
            this.url = function () {
                return urlBase + "/procesos/" + this.get("codigo") + "/dias/" +
                    this.get("dia") + "/foco";
            }
            this.save(null, GeoDengue.callback);
        }
    });
});