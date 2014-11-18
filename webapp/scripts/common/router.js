/**
 * Define el router genérico de la aplicación.
 * @class
 * @name common.Router
 * @author <a href="mailto:mxbg.py@gmail.com">Maximiliano Báez</a>
 */
define(['backbone', 'backbone-extend'], function (Backbone, BackboneExtend) {
    /**
     * Define el mecanismo para manejar las multiples páginas.
     */
    return Backbone.Router.extend({
        routes: {
            "*actions": "interceptor"
        },
        /**
         * Este atributo hace referencia al Page actual, su valor
         * inicial es null.
         */
        current: null,
        /**
         * Handler genérico de los paths de la url. Se encarga de
         * cargar el page correspondiente.
         * @param {Object}action el path de la url que se encuentra
         *          luego del #
         */
        handler: function (params) {
            // referencia a si mismo
            var thiz = this;
            // Se cargar el page correspondiente
            require(['scripts/pages' + params['#']],
                function (Page) {
                    if (thiz.current != null) {
                        //se cierra el page para desasociar los eventos
                        //del viejo page para evitar conflictos con el
                        //nuevo page.
                        thiz.current.close();
                    }
                    //se instancia el nuevo page
                    thiz.current = new Page({
                        el: $('#appContent')
                    });
                }
            );
        },

        /**
         * Interceptor de las urls, se encarga de verificar la url, extraer
         * los parametros de la misma e invocar al hadler.
         *
         * @param {String}action el path de la url que se encuentra
         *          luego del #
         */
        interceptor: function (action) {
            //Se obtienen los parametros de la url para verificar los parametros
            //de la url
            var urlParams = GeoDengue.getHashParams();
            if (typeof urlParams["#"] == "undefined" || urlParams["#"].length == 0) {
                window.location = "#/inicio/";
            } else {
                this.handler(urlParams);
            }
        }
    });
});
