
/**
 * Este workspace abarca las clases que manejan las capas pertenecientes
 * al mapa.
 *
 * @autor Maximiliano Báez <mbaez@konecta.com.py>
 */
Layer = {
    /**
     * Construye el Stratergy tipo Save que es aplicado a las capas
     * del tipo vector.
     *
     * @autor Maximiliano Báez <mbaez@konecta.com.py>
     */
    StrategySave : function(){
        return  new OpenLayers.Strategy.Save({
            onCommit: function(response) {

                if(!response.success() && this.onFailure){
                    this.onFailure();
                    return;
                }else if(this.onSuccess){
                    this.onSuccess(response);
                }

                this.layer.refresh();
            }
        });
    },

    /**
     * Construye el protocolo WFS para obtener una capa.
     *
     * @autor Maximiliano Báez <mbaez@konecta.com.py>
     *
     * @param layerName el nombre de la capa que se debe obtener
     * @return el protocolo WFS construido
     * @see Gis.Map.Config()
     */
    Protocol : function(layerName, service, geometryName, filter,featureNS){
        //var config =  new DataSource();
        var options = {
            url:  DataSource.host + service,
            version: "1.1.0",
            //featureNS : DataSource.workspace,
            featureType: layerName,
            geometryName: geometryName,
            srsName: DataSource.projectionCode
        };
        if(featureNS){
            options['featureNS'] = featureNS;
        }

        if(filter){
            options['filter'] = filter;
        }
        return new  OpenLayers.Protocol.WFS(options);
    },

    /**
     * Crea una capa del tipo vector, del servidor y del workspace
     * definidos en las vairables host y workspace.
     *
     * @autor Maximiliano Báez <mbaez@konecta.com.py>
     *
     * @param layerName {String} el nombre de la capa que se debe obtener
     * @param geometryName {String} el nombre de la columna que contiene la geometria
     * @param filter {Gis.Filter} el filtro para acotar los features que se retornan
     * @return {OpenLayers.Layer.Vector} La capa del tipo vector construida
     * @see Protocol(String, String, String)
     * @see StrategySave()
     */
    Vector : function(layerName, geometryName,featureNS, options){
        if(!geometryName && !featureNS){
            return new OpenLayers.Layer.Vector(layerName,
                    {displayInLayerSwitcher: false});
        }

        //se construye el strategy
        var params = {};
        if(options){
            params = options;
        }
        //var config = new DataSource();
        var fixed = new OpenLayers.Strategy.Fixed();
        var strategySave =  new Gis.Map.Layer.StrategySave();
        //se establece el servicio
        var service = "ows";
        //se construye el protocolo
        var protocol = null;
        protocol = new Layer.Protocol(layerName,
                          service, geometryName,params['filter'],featureNS);
        if(params['callback']){
            protocol.read({
                callback: params['callback']
            });
        }

        //Se construye la capa del tipo vector
        return new OpenLayers.Layer.Vector(layerName,
            {
                strategies : [fixed, strategySave],
                protocol: protocol,
                /**
                 * Se encarga de confirmar los cambios realizados en las capas.
                 *
                 * @param options{Object}
                 *            un json con que cuenta con los siguientes parametros
                 *            válidos :
                 *            -onSuccess {function}: Cuando la operacion se realizó
                 *              correctamente
                 *            -onFailure {function}: cuando ocurrio un error al
                 *              realizar la operación.
                 *
                 * @autor Maximiliano Báez<mbaez@konecta.com.py>
                 */
                commit : function(options){
                    if(options){
                        this.strategies[1]["onSuccess"] = options.onSuccess;
                        this.strategies[1]["onFailure"] = options.onFailure;
                    }
                    this.strategies[1].save();
                },
                displayInLayerSwitcher: false
            }
        );
    },

    /**
     * Construye una capa satelital de google.
     *
     * @autor Maximiliano Báez <mbaez@konecta.com.py>
     *
     * @return la capa satelital de google.
     */
    Google : function(options){
        var zoomLevels =  20;
        if(options.zoomLevels){
            zoomLevels = options.zoomLevels;
        }
        return new OpenLayers.Layer.Google(
            options.type, {
                type: options.type,
                numZoomLevels: zoomLevels,
                sphericalMercator: false,
                animationEnabled: false
            }
        );
    },

    /**
     * Obtiene las capas del servidor mediante el protocolo WMS.
     *
     * @autor Maximiliano Báez <mbaez@konecta.com.py>
     *
     * @params names: {String}un array con los nombres de las capas a construir
     * @params filter: {OpenLayers.Filter} un filtro para acotar la capa
     * @params base: {Boolean} establece si es o no una capa base
     * @return La lista de capas WMS obtenidas.
     * @see Gis.Map.Config
     */
    WMS : function(names,filter,base,geometryName){
        //direccion del servidor al cual se le realizan las peticiones de las
        //capas via WMS
        var filter_1_1 = new OpenLayers.Format.Filter({version: "1.1.0"});
        var xml = new OpenLayers.Format.XML();
        //var config = new DataSource();
        var server = DataSource.host + "wms";
        //var server = DataSource.host + "gwc/service/wms";
        //formato en el que el servidor retorna el mapa
        var format = 'image/png';
        // nombre de las capas que se solicitan al servidor
        var layers = [];
        var options = {
            transparent: true,
            format: format,
            geometryName: geometryName
        };

        if(filter){
            options['filter'] = xml.write(filter_1_1.write(filter));
        }
        // se construyen las capas
        for(var i=0; i<names.length; i++){
            var name= names[i].workspace + ":" + names[i].name;
            options['layers'] = name;
            layers[i] = new OpenLayers.Layer.WMS(
                name, server, options, {attribution:""});

            layers[i].transitionEffect = 'resize';
            layers[i].isBaseLayer = base;
        }
        //se retorna las capas
        return layers;
    }

};
