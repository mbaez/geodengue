var GeoDengue = {};
GeoDengue.baseURL = "/geodengue/";
GeoDengue.RESTBaseUrl = '/geodengue/rest';

/**
 * Este método se encarga de obtener todos los parametros de la url y
 * los carga en un json.
 *
 * @author <a href="mailto:mxbg.py@gmail.com">Maximiliano Báez</a>
 */
GeoDengue.getUrlParams = function (url) {
    var urlString = "";
    if (!url) {
        document.location.search.replace("?", "");
    } else {
        var index = url.indexOf("?");
        if (index == -1) {
            index = url.length;
        }
        var action = url.substring(1, index - 1);
        var query = url.substring(index + 1, url.length);
        urlString = '#=' + action + '&' + query;
    }
    // se elimina el # del final
    if (urlString[urlString.length - 1] == "#") {
        urlString = urlString.substr(0, urlString.length - 1);
    }
    var params = urlString.split("&");
    var urlParams = {};

    // se agrega el trim para ie
    if (typeof String.prototype.trim !== 'function') {
        String.prototype.trim = function () {
            return this.replace(/^\s+|\s+$/g, '');
        };
    }
    // se obtiene los parametros de la url
    for (var i = 0; i < params.length; i++) {
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
GeoDengue.getHashParams = function () {
    return GeoDengue.getUrlParams(document.location.hash)
};
/**
 * Sobre-escribe el metodo parse de los Collections de manera a sacar
 * la respuesta del atributo "lista".
 * @author <a href="mailto:mxbg.py@gmail.com">Maximiliano Báez</a>
 */
GeoDengue.responseParser = function (response) {
    return response.lista;
};