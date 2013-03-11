/**
 * Inicializador de la página de inicio
 * @class
 * @author <a href="mailto:mbaez@konecta.com.py">Maximiliano Báez</a>
 * @name controllers.Inicio
 */
define([    'libs/JQuery/js/jquery',
            'libs/underscore',
            'libs/backbone',
            "scripts/views/map/MapView",
            "text!templates/map/MapTmpl.html"
        ], function ($,_,Backbone,
            MapView, MapTmpl
        ) {
    "use strict";
    var thiz ={};
    var mapPanel = new MapView ({el : $("#incioContent")});
    // se retorna el json que contiene los metodos de los eventos
    return thiz;
});
