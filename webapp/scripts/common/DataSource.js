
/**
 * Esta clase contiene varialbles estaticas que contiene información
 * las configuraciones necesarias.
 *
 * @author <a href="mailto:mxbg.py@gmail.com">Maximiliano Báez</a>
 */
DataSource = {
    /**
     * Sistema de proyecciones del mapa
     */
    //projectionCode : "EPSG:4326",
    projectionCode : "EPSG:900913",

    /**
     * Las configuraciones de la capa
     */
    larvitrampasLayerConf : {
        name: 'larvitrampas',
        //filterColumn : "",
        geometryName: 'the_geom',
        featureNS : "py.com.tesis.dengue" ,
        workspace : "tesis",
        styleMap : null
    },
    baseLayerConf : {
        name: 'MapaColombia',
        workspace : "tesis"
    }
};


/**
 * La direcion del geoserver de konecta, acceso atravez de internet
 */
DataSource.server = "http://octavius.konecta.com.py:8080";
//DataSource.server = "http://localhost:8080";
/**
 * La url del servidor con el proxy del servidor, todas las peticiones
 * http, excepto el login y logout, pasan atravez del proxy para
 * evitar el problema de cross domain.
 */
DataSource.url = DataSource.server;
/**
 * El path completo del geoservrer
 */
DataSource.host = DataSource.url+"/geoserver/";
