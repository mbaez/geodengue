/**
 * Este workspace abarca las clases que manejan las capas pertenecientes
 * al mapa.
 * @namespace
 *
 * @author <a href="mailto:mxbg.py@gmail.com">Maximiliano Báez</a>
 * @name common.Layer
 */
Layer = {
    /**
     * Construye el Stratergy tipo Save que es aplicado a las capas
     * del tipo vector.
     * @class
     *
     * @name common.Layer.StrategySave
     * @author <a href="mailto:mxbg.py@gmail.com">Maximiliano Báez</a>
     * @return {OpenLayers.Strategy.Save}
     */
    StrategySave: function () {
        return new OpenLayers.Strategy.Save({
            onCommit: function (response) {
                if (!response.success() && this.failure) {
                    this.failure();
                    return;
                } else if (this.success) {
                    this.success(response);
                }

                this.layer.refresh();
            }
        });
    },

    /**
     * Construye el protocolo WFS para obtener una capa.
     * @class
     *
     * @name common.Layer.Protocol
     * @author <a href="mailto:mxbg.py@gmail.com">Maximiliano Báez</a>
     * @param options {Object}
     * @config {String} layerName El nombre de la capa
     * @config {String} service El nombre del servicio (wfs o ows).
     * @config {String} geometyName El nombre de la columna que contiene
     *              el geometry del layer.
     * @config {OpenLayers.Layer.Filter} [filter] el filtro utilizado para acotar
     *              los datos.
     * @config {String} [featureNS] la url del workspace en el que se
     *              encuentra el layer.
     * @return {OpenLayers.Protocol.WFS}
     */
    Protocol: function (options) {
        var params = {
            url: DataSource.host + options.service,
            featureType: options.name,
            version: "1.1.0",
            featureNS: options.featureNS,
            geometryName: options.geometryName,
            srsName: DataSource.projectionCode
        };

        if (typeof options.filter != "undefined") {
            params['filter'] = options.filter;
        }
        return new OpenLayers.Protocol.WFS(params);
    },

    /**
     * Crea una capa del tipo vector, del servidor y del workspace
     * definidos en las vairables host y workspace.
     * @class
     *
     * @author <a href="mailto:mxbg.py@gmail.com">Maximiliano Báez</a>
     * @name common.Layer.Vector
     * @param options {Object}
     * @config {String} layerName El nombre de la capa
     * @config {String} [geometyName] El nombre de la columna que contiene
     *              el geometry del layer.
     * @config {OpenLayers.Filter} [filter] el filtro utilizado para acotar
     *              los datos.
     * @config {String} [featureNS] La url del workspace en el que se
     *              encuentra el layer.
     * @config {Function} [callback] Función que es invocada cuando se
     *               obtiene los datos del layer.
     * @return {OpenLayers.Layer.Vector} La capa del tipo vector construida.
     */
    Vector: function (options) {
        if (!options["geometryName"] && !options["featureNS"]) {
            return new OpenLayers.Layer.Vector(options.name, {
                displayInLayerSwitcher: false
            });
        }
        //se construye el strategy
        var params = {};
        //se copian los atributos
        $.extend(params, options);
        params.callback = function (data) {
            //se dispara el evento para notificar que el view fue
            //renderizado
            $("body").trigger({
                type: 'on-layer-ready',
                layer: data
            });
        }
        //se establece el servicio
        params.service = "ows";
        var fixed = new OpenLayers.Strategy.Fixed();
        var strategySave = new Layer.StrategySave();
        //se construye el protocolo
        var protocol = new Layer.Protocol(params);
        protocol.read({
            callback: params['callback']
        });


        //Se construye la capa del tipo vector
        return new OpenLayers.Layer.Vector(options.name, {
            strategies: [fixed, strategySave],
            protocol: protocol,
            /**
             * Se encarga de confirmar los cambios realizados en las capas.
             * @function
             * @name common.Layer.Vector#commit
             * @author <a href="mailto:mxbg.py@gmail.com">Maximiliano Báez</a>
             * @param options {Object}
             * @config {Function} [success] Función que se invoca cuando
             *              la operacion se realizó correctamente
             * @config {Function} [failure] Función que es invocada
             *              cuando ocurrio un error al realizar la operación.
             */
            commit: function (options) {
                if (options) {
                    this.strategies[1]["success"] = options.success;
                    this.strategies[1]["failure"] = options.failure;
                }
                this.strategies[1].save();
            },
            displayInLayerSwitcher: true
        });
    },

    /**
     * Construye los layers para obtener los datos del servidor mediante
     * el potocolo WMS.
     * @function
     *
     * @author <a href="mailto:mxbg.py@gmail.com">Maximiliano Báez</a>
     * @params options {Object}
     * @config {Array}[names] Un array con los nombres de las capas a construir
     * @config {String}[name] Un string con el nombre de la capa a construir
     * @config {Boolean} [base] Establece si es o no una capa base
     *
     * @return {Array} La lista de capas WMS obtenidas.
     */
    WMS: function (options) {
        //direccion del servidor al cual se le realizan las peticiones de las
        //capas via WMS
        var server = DataSource.host;
        //var server = DataSource.host + "gwc/service/wms";
        //formato en el que el servidor retorna el mapa
        var format = 'image/png';
        // nombre de las capas que se solicitan al servidor
        var layers = [];
        var names = []
        //se validan los parametros del constructor
        if (typeof options.base == "undefined") {
            options.base = false;
        }
        if (typeof options.length != "undefined") {
            names = options;
        } else if (typeof options.name != "undefined") {
            names = [options];
        }
        //se preparan los parametros
        var config = {
            format: "image/png",
            transparent: true
        };
        // se construyen las capas
        for (var i = 0; i < names.length; i++) {
            //se establece el nombre del layer
            config.LAYERS = names[i].name;
            //se construye el layer wms
            layers[i] = new OpenLayers.Layer.WMS(
                config.LAYERS,
                server + names[i].workspace + "/wms",
                config
            );
            layers[i].transitionEffect = 'resize';
            layers[i].isBaseLayer = options.base;
        }
        //se retorna las capas
        return layers;
    }

};