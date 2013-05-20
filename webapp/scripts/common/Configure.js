
//se configura el requierejs
requirejs.config({
    baseUrl: '/geodengue/',
    paths: {
        'text' : 'libs/text'
    },
    shim: {
        'libs/underscore': {
            exports: '_'
        },
        'libs/JQuery/js/jquery': {
            exports: '$'
        },
        'libs/backbone': {
            deps: ['libs/underscore', 'libs/JQuery/js/jquery'],
            exports: 'Backbone'
        },
        'libs/backbone.page': {
            deps: ['libs/backbone'],
            exports: 'BPage'
        },
        'libs/Bootstrap/js/bootstrap.min' : {
            deps : ['libs/JQuery/js/jquery'],
            exports: 'Bootstrap'
        },
        'scripts/common/Layer' : {
            deps : ['libs/OpenLayers/OpenLayers'],
            exports: 'Layer'
        },
        'scripts/common/Style' : {
            deps : ['libs/OpenLayers/OpenLayers'],
            exports: 'Style'
        },
        'libs/OpenLayers/OpenLayers' : {
            exports: 'OpenLayers'
        }
    }
});

var GeoDengue = {};
GeoDengue.baseURL = "/geodengue/";
GeoDengue.RESTBaseUrl = '/geodengue/rest';

/**
 * Este método se encarga de obtener todos los parametros de la url y
 * los carga en un json.
 *
 * @author <a href="mailto:mxbg.py@gmail.com">Maximiliano Báez</a>
 */
GeoDengue.getUrlParams = function(url) {
    var urlString = "";
    if(!url){
        document.location.search.replace("?", "");
    }else{
        var index = url.indexOf("?");
        if(index == -1){
            index = url.length;
        }
        var action = url.substring(1 , index - 1);
        var query = url.substring(index+1, url.length);
        urlString = '#='+action +'&'+ query;
    }
    // se elimina el # del final
    if (urlString[urlString.length - 1] == "#") {
        urlString = urlString.substr(0, urlString.length - 1);
    }
    var params = urlString.split("&");
    var urlParams = {};

    // se agrega el trim para ie
    if (typeof String.prototype.trim !== 'function') {
        String.prototype.trim = function() {
            return this.replace(/^\s+|\s+$/g, '');
        };
    }
    // se obtiene los parametros de la url
    for ( var i = 0; i < params.length; i++) {
        var tokens = params[i].split("=");
        urlParams[tokens[0].trim()] = tokens[1];
    }
    return urlParams;
};

/**
 * Este método se encarga de obtener todos los parametros de la url que
 * se encuentran el el hash y los carga en un json.
 *
 * @author <a href="mailto:mbaez@konecta.com.py">Maximiliano Báez</a>
 */
GeoDengue.getHashParams = function(){
    return GeoDengue.getUrlParams(document.location.hash)
};


/**
 *
 * @author <a href="mailto:mbaez@konecta.com.py">Maximiliano Báez</a>
 */
require(['libs/backbone',
        'libs/backbone.page',
        "libs/Bootstrap/js/bootstrap.min"],
    function(Backbone,BPage,Bootstrap) {

    var Router = Backbone.Router.extend({
        routes: {
            "*actions": "interceptor"
        },
        /**
         * Este atributo hace referencia al Page actual, su valor
         * inicial es null.
         */
        current : null,
        /**
         * Handler genérico de los paths de la url. Se encarga de
         * cargar el page correspondiente.
         * @param action {String} el path de la url que se encuentra
         *          luego del #
         */
        handler : function(params){
            // referencia a si mismo
            var thiz = this;
            // Se cargar el page correspondiente
            require(['scripts/controllers' + params['#'] ],
                function(Page) {
                    if(thiz.current != null){
                        //se cierra el page para desasociar los eventos
                        //del viejo page para evitar conflictos con el
                        //nuevo page.
                        thiz.current.close();
                    }
                    //se instancia el nuevo page
                    thiz.current = new Page({el : $('#appContent')});
                }
            );
        },
        /**
         * Interseptor de las urls, se encarga de verificar la url, extraer
         * los parametros de la misma e invocar al hadler.
         *
         * @param action {String} el path de la url que se encuentra
         *          luego del #
         */
        interceptor : function(action){
            //Se obtienen los parametros de la url para verificar los parametros
            //de la url
            var urlParams = GeoDengue.getHashParams();
            //si se verifica que se especifique el path del page
            if(typeof urlParams["#"] == "undefined"){
                window.location="#/Inicio/";
            }else{
                //TODO Añadir controles de seguridad
                this.handler(urlParams);
            }
        }
    });
    //se instancia el router
    var router = new Router();
    Backbone.history.start();
});
