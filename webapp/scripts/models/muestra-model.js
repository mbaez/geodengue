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
                this.get("idMuestra");
        },
        /**
         * Se encarga de realizar un post a /muestras/{id_muestra}/{proceso}
         * @function
         * @name models.MuestraModel#executeProcess
         * @retruns {String} Un cadena que representa la url del recurso
         */
        executeProcess: function (data) {
            this.set({
                idMuestra: 1
            });
            // se obtiene la url base del model
            var urlBase = this.url();
            //se sobreescribe la url para invocar al proceso correspondiente
            this.url = function () {
                return urlBase + "/" + data.proceso;
            }
            this.save(null, GeoDengue.callback);
        }
    });
});