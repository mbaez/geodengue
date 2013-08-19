
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
        'libs/jquery': {
            exports: '$'
        },
        'libs/backbone': {
            deps: ['libs/underscore', 'libs/jquery'],
            exports: 'Backbone'
        },
        'scripts/common/Backbone.Extend': {
            deps: ['libs/backbone'],
            exports: 'BExtend'
        },
        'libs/bootstrap' : {
            deps : ['libs/jquery'],
            exports: 'Bootstrap'
        },
        'scripts/common/Layer' : {
            deps : ['libs/OpenLayers/OpenLayers'],
            exports: 'Layer'
        },
        'scripts/common/Control' : {
            deps : ['libs/OpenLayers/OpenLayers'],
            exports: 'Control'
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
 * @author <a href="mailto:mxbg.py@gmail.com">Maximiliano Báez</a>
 */
GeoDengue.getHashParams = function(){
    return GeoDengue.getUrlParams(document.location.hash)
};

/**
 *
 * @author <a href="mailto:mxbg.py@gmail.com">Maximiliano Báez</a>
 */
require(['libs/underscore',
        'libs/backbone',
        'libs/bootstrap',
        'scripts/common/Backbone.Extend'],
    function(_, Backbone,Bootstrap, BExtend) {
    //se configura los models y collection
    Setup.sync();
    //se instancia el router
    var router = new Backbone.AppRouter();
    Backbone.history.start();
});
