
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
                for(var i=0; i< this.data.fields.length; i++){
                    var id = this.data.fields[i].id;
                    var value = $("#"+id ).val();
                    this.data.feature.attributes[id] = value;
                }
                this.data.feature.state = "Update";
                this.onClose();
            },

            onClose : function() {
                this.data.mapPanel.map.removePopup(this.popup);
                this.popup.destroy();
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
                var compTmpl = _.template(tmpl,{data:this.data});
                this.popup = new OpenLayers.Popup.FramedCloud(
                    "chicken",
                    this.data.feature.geometry.getBounds().getCenterLonLat(),
                    null, compTmpl,
                    null, true, null);
                this.data.mapPanel.map.addPopup(this.popup);
                var thiz = this;
                $("#aceptar" ).click(function(){
                    thiz.onAceptar();
                });
                return this;
            }

        });
    }
);
