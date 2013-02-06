
/**
 * Esta clase contiene varialbles estaticas que contiene información
 * las configuraciones necesarias.
 *
 * @autor Maximiliano Báez <mbaez@konecta.com.py>
 */
DataSource = {

    /**
     * La direcion del geoserver de konecta, acceso atravez de internet
     */
    server : "http://octavius.konecta.com.py:8080",
    /**
     * La url del servidor con el proxy del servidor, todas las peticiones
     * http, excepto el login y logout, pasan atravez del proxy para
     * evitar el problema de cross domain.
     */
    url : "/gis/Proxy?url="+this.server,
    /**
     * El path completo del geoservrer
     */
    host : this.url+"/geoserver/",

    /**
     * Sistema de proyecciones del mapa
     */
    projectionCode : "EPSG:4326",
    projection : new OpenLayers.Projection(this.projectionCode),

    /**
     * Las configuraciones de la capa 
     */
    puntosRiesgoLayerConf : {
        name: 'puntosRiesgo',
        //filterColumn : "",
        geometryName: 'the_geom',       
        featureNS : "DWHMapasGpon" ,
        workspace : "workspace",
        styleMap : null
    }
};
