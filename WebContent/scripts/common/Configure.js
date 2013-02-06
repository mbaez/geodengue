
//se configura el requierejs
requirejs.config({
    baseUrl: '/geodengue/',
    paths: {
        'text' : 'libs/text'
    },
    shim: {
        'libs/underscore': {
            exports: '_'
        },
        'libs/JQuery/js/jquery': {
            exports: '$'
        },
        'libs/backbone': {
            deps: ['libs/underscore', 'libs/JQuery/js/jquery'],
            exports: 'Backbone'
        },
        'libs/Bootstrap/js/bootstrap.min' : {
            deps : ['libs/JQuery/js/jquery'],
            exports: 'Bootstrap'
        }
    }
});

/**
 *
 * @author <a href="mailto:mbaez@konecta.com.py">Maximiliano Báez</a>
 */
var urlMapper = {
    "inicio" : "Inicio"
}

/**
 *
 * @author <a href="mailto:mbaez@konecta.com.py">Maximiliano Báez</a>
 */
require(['libs/backbone'],function(Backbone) {

    var Router = Backbone.Router.extend({
        routes: {
            "*actions": "defaultRoute"
        }
    });

    var router = new Router();
    router.on('route:defaultRoute', function (actions) {
        if(!urlMapper[actions]){
            actions = "inicio";
            window.location ="#"+actions;
            return;
        }
        $.ajax('pages/' + urlMapper[actions] + ".html").done(
            function(data) {
              $('#appContent').html(data);
                //Una vez cargada la pagina, cargar su controlador
                require(['scripts/controllers/' + urlMapper[actions] ],
                    function(elScript) {
                        //nada que hacer
                    }
                );
            }
        );
    });

    Backbone.history.start();
});

