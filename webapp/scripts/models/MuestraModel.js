/**
 * Definición del modelo de un proceso
 * Retorna la clase, no una instancia.
 *
 * @class
 * @author <a href="mailto:mxbg.py@gmail.com">Maximiliano Báez</a>
 * @name models.MuestraModel
 */
define(["libs/underscore","libs/backbone"], function (_,Backbone) {
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
        url : function () {
            return GeoDengue.RESTBaseUrl + "/muestras/" +
                this.get("idMuestra") + "/evolucionar";
        }
    });
});
