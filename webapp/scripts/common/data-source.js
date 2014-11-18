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
    projectionCode: "EPSG:4326",
    //~ projectionCode : "EPSG:900913",
    maxExtent: [
        -60.60455146882159, -27.40893277789768,
        -54.2972992541837, -21.032259302736406
    ],

    center: [-57.59405207780335, -25.30465826128996],
    /**
     * Las configuraciones de la capa
     */
    puntosControlLayerConf: {
        name: 'puntos_control',
        geometryName: 'the_geom',
        featureNS: "py.com.geodengue",
        workspace: "geodengue"
    },  
    /**
     * Las configuraciones de la capa que contiene los datos de los adultos
     */
    eventosAdultosLayerConf: {
        name: 'eventos_adultos',
        geometryName: 'the_geom',
        featureNS: "py.com.geodengue",
        workspace: "geodengue"
    },
    /**
     * Las configuraciones de la capa que contiene los datos de los inidividuos
     * de etapas inmaduras.
     */
    eventosInmadurasLayerConf: {
        name: 'eventos_inmaduras',
        geometryName: 'the_geom',
        featureNS: "py.com.geodengue",
        workspace: "geodengue"
    },
    /**
     * Las configuraciones de la capa
     */
    puntosRiesgoLayerConf: {
        name: 'puntos_riesgo',
        geometryName: 'the_geom',
        featureNS: "py.com.geodengue",
        workspace: "geodengue"
    },

    /**
     * Configuraciones de la capa base.
     */
    baseLayerConf: {
        name: 'MapasPy',
        workspace: "geodengue",
        base: true
    },

    /**
     * Las configuraciones de la capa de raster
     */
    rasterLayerConf: {
        name: '',
        featureNS: "py.com.geodengue",
        workspace: "geodengue"
    },
};


/**
 * La direcion del geoserver de konecta, acceso atravez de internet
 */
//~ DataSource.server = "http://octavius.konecta.com.py:8080";
DataSource.server = "http://localhost/geodengue";
/**
 * La url del servidor con el proxy del servidor, todas las peticiones
 * http, excepto el login y logout, pasan atravez del proxy para
 * evitar el problema de cross domain.
 */
DataSource.url = DataSource.server;
/**
 * El path completo del geoservrer
 */
DataSource.host = DataSource.url + "/geoserver/";