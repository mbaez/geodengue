/**
 * Handler base de los
 * <a href="http://backbonejs.org/#Collection-fetch">collection</a> y
 * <a href ="http://backbonejs.org/#Model-fetch">models de backbone</a>,
 * se utiliza para implementar el patron ready de backbone.
 *
 *
 * @author <a href="mailto:mxbg.py@gmail.com">Maximiliano Báez</a>
 */
GeoDengue.callback = {
    /**
     * Handler del success de una petición, dispara el evento `ready` para
     * que sea manejado por el objeto de origen.
     *
     * @author <a href="mailto:mxbg.py@gmail.com">Maximiliano Báez</a>
     */
    success: function (data, response, options) {
        var params = {};
        params.data = data;
        params.response = response;
        params.options = options;
        data.trigger('ready', params);
    },

    /**
     * Handler del error de una petición, dispara el evento `error` para
     * que sea manejado por el objeto de origen.
     *
     * @author <a href="mailto:mxbg.py@gmail.com">Maximiliano Báez</a>
     */
    error: function (data, xhr, options) {
        var resp = {}
        resp.data = data;
        resp.xhr = xhr;
        resp.options = options
        data.trigger('error', resp);
    }
}


/**
 * Se encarga de setear los atributos de un model en el view. Reemplaza
 * el text de todos los elmentos que cuenten con el atributo
 * data-attr={nombreDelAtributo}. Si se especifica un name al model, collection
 * o json, se añadirá el nombre como prefijo data-attr=name.{nombreDelAtributo}
 * @function
 * @public
 *
 * @author <a href="mailto:mxbg.py@gmail.com">Maximiliano Báez</a>
 * @params {Object}options el json que contiene los datos.
 * @params {String}[name] solo para json planos. Los models y collection
 *          deben contar con un atributo name. En caso de que no se epecifique
 *          el name, se ignorará.
 */
Backbone.View.prototype.putAttributes = function (options, name) {
    var data;
    var attrName = "";
    //se define el target, el target o scope es todo el contenedor del view.
    var $target = $(this.$el);
    //si el name es un object es un dom que será utilizado como target
    if (typeof name == "object") {
        var $target = $(name).clone();
        name = undefined;
    }
    //~ se verifica si el options corresponde a response de un model o
    //~ collections.
    if (options == null) {
        return;
    } else if (typeof options.data == "undefined") {
        //~ es un json plano.
        data = options;
        attrName = typeof name == "undefined" ? "" : name + ".";
    } else {
        //~ si es un model o collection se realiza el tojson.
        data = options.data.toJSON();
        attrName = typeof options.data.name == "undefined" ? "" : options.data.name + ".";
    }


    //se conigura el collapse
    for (var attr in data) {
        var value = data[attr];
        attr = attrName + attr;
        var targetDom = $target.find("[data-attr='" + attr + "']");
        value = value == null ? "" : value;

        if ($(targetDom).is("input") || $(targetDom).is("select")) {
            $(targetDom).val(value);
        } else {
            $(targetDom).text(value);
        }
    }
    return $target;
};

/**
 * Se encarga de setear los atributos de un model en el view. Reemplaza
 * el text de todos los elmentos que cuenten con el atributo
 * data-attr={nombreDelAtributo}. Si se especifica un name al model, collection
 * o json, se añadirá el nombre como prefijo data-attr=name.{nombreDelAtributo}
 * @function
 * @public
 *
 * @author <a href="mailto:mxbg.py@gmail.com">Maximiliano Báez</a>
 * @params {Object}options el json que contiene los datos.
 * @params {String}[name] solo para json planos. Los models y collection
 *          deben contar con un atributo name. En caso de que no se epecifique
 *          el name, se ignorará.
 * @params {Boolean}[vacio] True incluye los vacios, en caso contrario solo incluirá los strings
 *            no vacios.
 */
Backbone.View.prototype.getAttributes = function (name, vacio) {
    var attrName = "";
    var putEmpty = typeof vacio == 'boolean' ? vacio : true;
    //~ se verifica si el options corresponde a response de un model o
    //~ collections.
    var selector = ""
    //~ es un json plano.
    selector = typeof name == "undefined" ? '[data-attr]' : "[data-attr^=" + name + "]";
    attrName = typeof name == "undefined" ? '' : name + ".";

    //se define el target, el target o scope es todo el contenedor del view.
    var target = "#" + $(this.$el).attr("id");
    //se conigura el collapse
    var data = {};
    $(target).find(selector).each(function (e) {
        var attr = $(this).attr('data-attr').replace(attrName, "");

        var val = $(this).val();
        var text = $(this).text();
        var value = typeof val !== "undefined" && val.length > 0 ? val : text;
        value = typeof value == "undefined" || value == null ? '' : value.trim();
        if (value.length > 0 || putEmpty) {
            data[attr] = value;
        }
    });
    /*se setean los valores*/
    return data;
};


/**
 * Se encarga de constuir un alert configurable para el view.
 * @function
 * @public
 *
 * @author <a href="mailto:mxbg.py@gmail.com">Maximiliano Báez</a>
 *
 * @params {Object}options
 * @config {String}type El tipo de alert.[success|warning|error|info]
 * @config {String}mensaje El mensaje del alert.
 */
Backbone.View.prototype.alert = function (options) {
    var titleType = {
        error: "Error",
        success: "Operaci\u00f3n exitosa",
        warning: "Atenci\u00f3n",
        info: "Aviso"
    };

    /*
     * si actualmente se desplegó un promp no se debe desplegar otro promp debido
     * que genera problemas con css y los eventos causando que la página no responda
     * bloquenado toda operación para el usaurio.
     */
    var $jqi = $(".jqi");
    var $confirm = $(".confirm");
    var isOpen = $('body').attr('data-alert');
    if ($jqi.length > 0 || typeof isOpen != 'undefined') {
        return;
    }
    /*
     *Si es que se puede renderizar el alert, se añade la marca para indicar que el alert ya
     *fue renderidzado.
     */
    $('body').attr('data-alert', true);
    //se configuran los class
    var time = $confirm.length == 0 ? 0 : 1000;
    var alert = 'alert-' + options.type;
    var btn = "btn-" + options.type;
    var config = {
        title: titleType[options.type],
        zIndex: 9999,
        classes: {
            box: '',
            fade: '',
            prompt: alert,
            close: '',
            title: alert,
            message: alert,
            buttons: btn,
            button: '',
            defaultButton: ''
        },
        close: function (events) {
            //cuando se cierra el alert se remueve la marca para habilitar la creación de 
            //nuevos alerts
            $('body').removeAttr('data-alert');
        }
    }
    //se construye el alert
    setTimeout(function () {
        $.prompt(options.mensaje, config);
    }, time);
};

/**
 * Se encarga de desplegar el mensaje de error del view.
 * @function
 * @public
 *
 * @author <a href="mailto:mxbg.py@gmail.com">Maximiliano Báez</a>
 */
Backbone.View.prototype.error = function (data) {
    var response;
    try {
        response = JSON.parse(data.xhr.responseText);
    } catch (e) {
        response = {
            codigo: 500,
            mensaje: data.xhr.responseText
        }
    }
    //se construye el alert
    this.alert({
        mensaje: response.mensaje,
        type: "error"
    });
};


/**
 * Se encarga de implementar los fetch por páginas para los collections
 * de backbone.
 * @function
 * @public
 *
 * @author <a href="mailto:mxbg.py@gmail.com">Maximiliano Báez</a>
 */
Backbone.Collection.prototype.pagination = function (callback) {

    if (typeof this.pagerBaseUrl == "undefined") {
        this.pagerBaseUrl = this.url();
    }

    if (typeof this.pagina == "undefined") {
        this.pagina = 1;
    }

    if (typeof this.registros == "undefined") {
        this.registros = 10;
    }
    var baseUrl = this.pagerBaseUrl;
    //se sobrescribe la url para obtner la página solicitada
    this.inicio = (this.pagina - 1) * this.registros;
    this.url = function () {
        var and = "?";
        if (baseUrl.indexOf("?") >= 0) {
            and = "&";
        }
        return baseUrl + and + "registros=" + this.registros + "&inicio=" + this.inicio;
    }
    //se realiza el fetch a la url actualizada
    return this.fetch(callback);
};

/**
 * Se encarga de verificar si existe el $el correspondiente al view.
 * Su objetivo es evitar que se los collection/models realicen un
 * fetch si es que no existe el `$el` correspondiente. Si el `$el`
 * existe dispara el evento `allowed`, en caso contrario dispara el
 * evento `forbidden`
 * @function
 * @public
 *
 * @author <a href="mailto:mxbg.py@gmail.com">Maximiliano Báez</a>
 */
Backbone.View.prototype.setup = function (options) {
    var event = 'forbidden';
    //si posee el elemento
    if (this.$el.length > 0) {
        event = 'allowed';
        /*se añade el atributo scope*/
        this.scope = "#" + options.el.attr("id");
    }
    /*
     * Se añade un wrap al metodo render de los views para poder
     * detectar cuando terminó de renderizarce un view. Se dispara
     * un evento 'view-render-done'.
     */
    this.render = _.wrap(this.render, function (render, args) {
        render.call(this, args);
        //se dispara el evento para notificar que el view fue
        //renderizado
        $("body").trigger({
            type: 'on-render-done',
            scope: this.scope
        });
    });
    //se dispara el evento
    this.trigger(event, options);
};

Backbone.View.prototype.close = function (options) {
    this.undelegateEvents();
};

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
    getValue: function (object, prop) {
        if (!(object && object[prop])) return null;
        return _.isFunction(object[prop]) ? object[prop]() : object[prop];
    },

    /**
     * Dispara una excepción cuando se requiere la URL y no fue establecida.
     * Es aplicable a los models y collections de backbone.
     * @function
     * @private
     */
    urlError: function () {
        throw new Error('A "url" property or function must be specified');
    },

    /**
     * Sobre-escribir el método de comunicación al servidor de manera a introducir
     * en la cabecera datos de la sesión.
     * @function
     * @public
     *
     * @author <a href="mailto:mxbg.py@gmail.com">Maximiliano Báez</a>
     */
    sync: function () {
        Backbone.sync = function (method, model, options) {
            // Map from CRUD to HTTP for our default `Backbone.sync` implementation.
            var methodMap = {
                'create': 'POST',
                'update': 'PUT',
                'delete': 'DELETE',
                'read': 'GET'
            };
            //se obtiene el tipo de petición a realizar
            var type = methodMap[method];

            // Default options, unless specified.
            options || (options = {});

            // Default JSON-request options.
            var params = {
                type: type,
                dataType: 'json'
            };

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
                params.data = params.data ? {
                    model: params.data
                } : {};
            }

            // For older servers, emulate HTTP by mimicking the HTTP method with `_method`
            // And an `X-HTTP-Method-Override` header.
            if (Backbone.emulateHTTP) {
                if (type === 'PUT' || type === 'DELETE') {
                    if (Backbone.emulateJSON) {
                        params.data._method = type;
                    }

                    params.type = 'POST';
                    params.beforeSend = function (xhr) {
                        xhr.setRequestHeader('X-HTTP-Method-Override', type);
                    };
                }
            }

            // Don't process data on a non-GET request.
            if (params.type !== 'GET' && !Backbone.emulateJSON) {
                params.processData = false;
            }
            params.headers = {
                "Content-type": "application/json"
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