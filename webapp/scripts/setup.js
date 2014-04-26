/**
 * Se configuran las dependencias de los módulo con requierejs
 */
requirejs.config({
    baseUrl: '/geodengue/',
    paths: {
        "text": "libs/text",
        "underscore": "libs/underscore",
        "backbone": "libs/backbone",
        "highcharts": "libs/highcharts-custom",
        /*bootstrap*/
        "bootstrap": "libs/bootstrap",
        /*Jquery y plugins*/
        "jquery": "libs/jquery/jquery",
        "jquery-ui": "libs/jquery/jquery-ui",
        "selectize": "libs/jquery/selectize",
        "jquery-impromptu": "libs/jquery/jquery-impromptu",
        /*openlayer*/
        'OpenLayers': 'libs/OpenLayers/OpenLayers',
        'openlayers-layer': 'scripts/common/openlayers-layer',
        'openlayers-control': 'scripts/common/openlayers-control',
        'openlayers-style': 'scripts/common/openlayers-style',

        /*Plugins utilitarios*/
        "backbone-page": "scripts/common/backbone-page",
        "backbone-extend": "scripts/common/backbone-extend",
        "router": "scripts/common/router"
    },
    waitSeconds: 60,
    shim: {
        'underscore': {
            exports: '_'
        },
        'jquery': {
            exports: '$'
        },
        'backbone': {
            deps: ['underscore', 'jquery'],
            exports: 'Backbone'
        },
        'jquery-ui': {
            exports: 'jqui',
            deps: ['jquery']
        },
        'bootstrap': {
            exports: 'Bootstrap',
            deps: ['jquery', 'jquery-ui']
        },
        'jquery-impromptu': {
            deps: ['jquery'],
            exports: 'Impromptu'
        },
        'selectize': {
            deps: ['jquery'],
            exports: 'Selectize'
        },
        'backbone-page': {
            deps: ['backbone', 'bootstrap', 'jquery-impromptu'],
            exports: 'BackbonePage'
        },
        'backbone-extend': {
            deps: ['backbone-page'],
            exports: 'BackboneExtend'
        },

        'libs/validation': {
            deps: [],
            exports: 'Validation'
        },

        'openlayers-layer': {
            deps: ['OpenLayers','jquery'],
            exports: 'Layer'
        },
        'openlayers-control': {
            deps: ['OpenLayers'],
            exports: 'Control'
        },
        'openlayers-style': {
            deps: ['OpenLayers'],
            exports: 'Style'
        },
        'OpenLayers': {
            exports: 'OpenLayers'
        }
    }
});

/**
 * Se añade el handler de error de requierejs. Se ivoca a este método
 * cuando no se pudo cargar una dependencia.
 *
 * @author <a href="mailto:mbaez@konecta.com.py">Maximiliano Báez</a>
 */
requirejs.onError = function (err) {
    console.error(err.requireModules);
};

require(["underscore", 'backbone', 'router'],
    function (_, Backbone, Router) {
        var router = new Router();
        // se inicializa el historial
        Backbone.history.start();
        Setup.sync();
    }
);