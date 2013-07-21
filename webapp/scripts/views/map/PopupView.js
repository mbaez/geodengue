
/**
 * Descripción del view
 * @class
 * @author <a href="mailto:correo@autor">Nombre del autor</a>
 * @name nombre del view
 */
define(["libs/backbone",
        "libs/OpenLayers/OpenLayers",
        //se incluye el template
        "text!templates/map/PopupTmpl.html"],
    function(Backbone, OpenLayers,tmpl) {
        return Backbone.View.extend({
            /**
             * Constructor de la clase
             * @function
             *
             * @name #inicialize
             * @params {Object} options
             * @config {Array} fields
             */
            initialize: function(options) {
                this.data = options;
                this.render();
            },


            onAceptar : function(events){
                this.putAttributes();
                this.onClose();
            },

            /**
             * Añade los valores de los atributos del feature al popup
             * @autor Maximiliano Báez <mbaez@konecta.com.py>
             */
            showAttributes : function(){
                var attributes = {};
                var feature = this.data.feature;
                for(var i=0; i< this.data.fields.length; i++){
                    var id = this.data.fields[i].id;
                    var value = feature.attributes[id];
                    if(this.data.fields[i].type == "date"){
                        value = new Date(value);
                        document.getElementById(id).valueAsDate = value;
                    }else{
                        $("#"+id ).val(value);
                    }
                }
            },

            /**
             * Añade los valores del form del popup al feature.
             * @autor Maximiliano Báez <mbaez@konecta.com.py>
             */
            putAttributes : function(){
                var attributes = {};
                var feature = this.data.feature;
                for(var i=0; i< this.data.fields.length; i++){
                    var id = this.data.fields[i].id;
                    var value = $("#"+id ).val();
                    feature.attributes[id] = value;
                }
                feature.state = this.data.state;
            },

            onClose : function() {
                this.data.mapPanel.map.removePopup(this.popup);
                this.popup.destroy();
                $("#mapPopup").remove();
            },
            /**
             * Este metodo se encarga de contruir el view a partir del
             * template.
             * @function
             *
             * @public
             * @name #render
             */
            render: function () {
                var thiz = this;
                var compTmpl = _.template(tmpl,{data:this.data});
                this.popup = new OpenLayers.Popup.FramedCloud(
                    "chicken",
                    this.data.feature.geometry.getBounds().getCenterLonLat(),
                    null, compTmpl,
                    null, true, function(){
                       thiz.onClose();
                    });
                this.data.mapPanel.map.addPopup(this.popup);
                var thiz = this;
                $("#aceptar").click(function(){
                    thiz.onAceptar();
                });
                this.showAttributes();
                return this;
            }

        });
    }
);
