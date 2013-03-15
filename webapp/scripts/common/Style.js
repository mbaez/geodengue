Style ={};
/**
 * Clase que se encarga de aplicar el estilo al layer.
 *
 * @author <a href="mailto:mxbg.py@gmail.com">Maximiliano Báez</a>
 */
Style.Apply = function(styleMap) {
    this.complete = function(req) {
        var format = new OpenLayers.Format.SLD();
        var sld = format.read(req.responseXML || req.responseText);
        for ( var l in sld.namedLayers) {
            for ( var index = 0; index < sld.namedLayers[l].userStyles.length; index++) {
                var value = sld.namedLayers[l].userStyles[index];
                var style = value;
                styleMap.styles[value.name] = style;
            }
        }
        for ( var type in styleMap.styles) {
            if (styleMap.styles[type].rules) {
                for(var i=0; i<styleMap.styles[type].rules.length; i++){
                var rule = styleMap.styles[type].rules[i];
                    if (rule && rule.symbolizer["Point"]) {
                        rule.symbolizer.Point["labelOutlineColor"] = "white";
                        rule.symbolizer.Point["labelOutlineWidth"] = "3";
                        rule.symbolizer.Point["fill"] = true;
                    }
                }
            }
        }
    };
};

/**
 * Clase que se encarga de realiza la peticion http para obtener el xml que
 * contiene el sld del estilo y posteriormente aplicar el estilo a la capa.
 *
 * @author <a href="mailto:mxbg.py@gmail.com">Maximiliano Báez</a>
 */
Style.Layer = function(sldUrl) {
    this.styleMap = new OpenLayers.StyleMap();
    this.apply = new Style.Apply(this.styleMap);
    this.get = OpenLayers.Request.GET({
        url : sldUrl,
        success : this.apply.complete
    });
};
