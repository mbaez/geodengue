
/**
 * Handler base de los
 * <a href="http://backbonejs.org/#Collection-fetch">collection</a> y
 * <a href ="http://backbonejs.org/#Model-fetch">models de backbone</a>,
 * se utiliza para implementar el patron ready de backbone.
 *
 *
 * @author <a href="mailto:mxbg.py@gmail.com">Maximiliano Báez</a>
 */
GeoDengue.callback= {
    /**
     * Handler del success de una petición, dispara el evento `ready` para
     * que sea manejado por el objeto de origen.
     *
     * @author <a href="mailto:mxbg.py@gmail.com">Maximiliano Báez</a>
     */
    success : function(data,response,options){
        var params ={};
        params.data =  data;
        params.response = response;
        params.options = options;
        data.trigger('ready',params);
    },

    /**
     * Handler del error de una petición, dispara el evento `error` para
     * que sea manejado por el objeto de origen.
     *
     * @author <a href="mailto:mxbg.py@gmail.com">Maximiliano Báez</a>
     */
    error : function(data, xhr, options){
        var resp = {}
        resp.data = data;
        resp.xhr = xhr;
        resp.options = options
        data.trigger('error', resp);
    }
}


/**
 * Define el módulo Page que extiende de Backbone.View. Un Page
 * es un contenedor de alto nivel que contiene multiples views.
 * <br/>
 * Un page cuenta básicamente con 2 estados : <br/>
 * <ul><li>
 *  <b>Open<b> : Cuando el page esta activo y siendo utilizado
 *  todos los eventos se ecuentran asociados al page en este estado.
 * </li>
 * <li>
 *  <b>Close</b> : El page en este estado no cuenta con eventos
 *  asociados.
 * </li> </ul>
 * @author <a href="mailto:mxbg.py@gmail.com.py">Maximiliano Báez</a>
 */
Backbone.Page = Backbone.View.extend({});
_.extend(Backbone.Page.prototype, {

    /**
     * Este método se encarga de desasociar todos los eventos del
     * page actual.
     * @author <a href="mailto:mxbg.py@gmail.com.py">Maximiliano Báez</a>
     */
    close : function(){
        this.undelegateEvents();
        this.$el.removeData().unbind();
        this.$el.html("");
    }
});

/**
 * Namespace que contiene los métodos para configurar la aplicación.
 * @namespace
 */
Setup = {
    /**
     *Método utilizado para obtener el valor de un objeto de Backbone como
     * una función o una propiedad.
     * @function
     * @private
     */
    getValue : function(object, prop) {
      if (!(object && object[prop])) return null;
      return _.isFunction(object[prop]) ? object[prop]() : object[prop];
    },

    /**
     * Dispara una excepción cuando se requiere la URL y no fue establecida.
     * Es aplicable a los models y collections de backbone.
     * @function
     * @private
     */
    urlError : function() {
        throw new Error('A "url" property or function must be specified');
    },

    /**
     * Sobre-escribir el método de comunicación al servidor de manera a introducir
     * en la cabecera datos de la sesión.
     * @function
     * @public
     *
     * @author <a href="mailto:mbaez@konecta.com.py">Maximiliano Báez</a>
     */
    sync : function(){
        Backbone.sync = function(method, model, options) {
            // Map from CRUD to HTTP for our default `Backbone.sync` implementation.
            var methodMap = {
                'create': 'POST',
                'update': 'PUT',
                'delete': 'DELETE',
                'read':   'GET'
            };
            //se obtiene el tipo de petición a realizar
            var type = methodMap[method];

            // Default options, unless specified.
            options || (options = {});

            // Default JSON-request options.
            var params = {type: type, dataType: 'json'};

            // Ensure that we have a URL.
            if (!options.url) {
              params.url = Setup.getValue(model, 'url') || Setup.urlError();
            }

            // Ensure that we have the appropriate request data.
            if (!options.data && model && (method == 'create' || method == 'update')) {
              params.contentType = 'application/json';
              params.data = JSON.stringify(model.toJSON());
            }

            // For older servers, emulate JSON by encoding the request into an HTML-form.
            if (Backbone.emulateJSON) {
              params.contentType = 'application/x-www-form-urlencoded';
              params.data = params.data ? {model: params.data} : {};
            }

            // For older servers, emulate HTTP by mimicking the HTTP method with `_method`
            // And an `X-HTTP-Method-Override` header.
            if (Backbone.emulateHTTP) {
              if (type === 'PUT' || type === 'DELETE') {
                if (Backbone.emulateJSON) {
                    params.data._method = type;
                }

                params.type = 'POST';
                params.beforeSend = function(xhr) {
                    xhr.setRequestHeader('X-HTTP-Method-Override', type);
                };
              }
            }

            // Don't process data on a non-GET request.
            if (params.type !== 'GET' && !Backbone.emulateJSON) {
              params.processData = false;
            }
            params.headers = {
                "Content-type" : "application/json"
            }
            /*
             * Se añade el parametro para que no se cacheen las peticiones
             * ajax.
             */
            params.cache = false;
            // Make the request, allowing the user to override any Ajax options.
            return $.ajax(_.extend(params, options));
        };
    }
}

/**
 * Define el mecanismo para manejar las multiples páginas.
 */
Backbone.AppRouter = Backbone.Router.extend({
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
        require(['scripts/pages' + params['#'] ],
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
