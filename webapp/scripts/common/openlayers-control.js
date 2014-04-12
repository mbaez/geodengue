/**
 * Este workspace abarca las clases que manejan los controles a utilizace
 * en los layers.
 * @namespace
 *
 * @author <a href="mailto:mxbg.py@gmail.com">Maximiliano Báez</a>
 * @name common.Control
 */
Control = {
    /**
     * Construye el control que permite modificar las capas.
     *
     * @author <a href="mailto:mxbg.py@gmail.com">Maximiliano Báez</a>
     * @param vectorLayer : la capa del tipo vector sobre la cual es
     *                      editable.
     */
    ModifyFeature : function(vectorLayer){
        return new OpenLayers.Control.ModifyFeature(
            vectorLayer
        );
    },

    /**
     * Construye el control que permite dibujar un punto.
     *
     * @author <a href="mailto:mxbg.py@gmail.com">Maximiliano Báez</a>
     * @param vectorLayer : la capa del tipo vector sobre la cual es
     * editable.
     * @param {function}handler:  La funcion a la cual se llamara cuando
     * se agregue un feature a la capa
     */
    DrawPointFeature : function (vectorLayer,handler){
        var params = {
            handlerOptions: {multi: false}
        }
        //si cuenta con un handler
        if(typeof handler == "function"){
            params.funcionHandler = handler;
        }
        //se retorna el control de openlayers ya inicializado.
        return new OpenLayers.Control.DrawFeature(
            vectorLayer, OpenLayers.Handler.Point, params
        );
    },

    /**
     * Construye el control que permite seleccionar los objetos de una capa.
     *
     * @author <a href="mailto:mxbg.py@gmail.com">Maximiliano Báez</a>
     * @param vectorLayer : la capa del tipo vector la cual se desea
     * seleccionar.
     */
    SelectFeature : function(vectorLayer){
        //se construye el control
        var selectCtrl = new OpenLayers.Control.SelectFeature(vectorLayer,
            {
                clickout: true,
                onSelect : function(e){}
            }
        );
        return selectCtrl;
    },
    /**
     * Construye el control que permite eliminar los objetos de una capa.
     *
     * @author <a href="mailto:mxbg.py@gmail.com">Maximiliano Báez</a>
     * @param vectorLayer : la capa del tipo vector con la cual se va a
     * trabajar.
     */
    DeleteFeature :function(vectorLayer) {
        return new OpenLayers.Control.SelectFeature(vectorLayer);
    }
};
