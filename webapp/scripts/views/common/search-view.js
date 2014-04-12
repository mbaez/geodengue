/**
 * View generico para busqueda.
 * @class
 * @author <a href="mailto:mbaez@konecta.com.py">Maximiliano Báez</a>
 * @name views.common.ViewSearch
 */
define(["jquery-ui", 'selectize', "text!templates/common/search-tmpl.html"],
    function (jqui, Selectize, tmpl) {

        return Backbone.View.extend({
            /**
             * Constructor de la clase
             * @function
             * @constructor
             *
             * @name views.common.ViewSearch#initialize
             * @param {Object}options
             * @config {Backbone.Collection}collection el collection con
             *         utilizado para cargar los datos.
             * @config {String}attr el nombre del model el cual se va
             *          visualizar.
             * @config {String}[placeholder] El placeholder para el input.
             * @config {String}[cambiarLabel] El label del boton de cambiar.
             * @config {boolean}[setDefault] Indica si se cargará un valor
             *          por defecto en el input. Por defecto es true.
             * @config {boolean}[validate] Flag utilizado para habilitar
             *          o desabilitar la validación de los datos. Por
             *          defecto es `true`
             * @config {String}[prefijo] texto que se antepono al input
             *          editable. Por defecto su valor es "0".
             * @config {String}[defaultValue] el valor por defecto de la
             *          lista. Si el valor no existe se establece el primer
             *          elemento de la lista.
             */
            initialize: function (options) {
                //si tiene permitido cargar este view
                this.on('allowed', this.allowed, this);
                this.setup(options);
            },

            /**
             * Si posee los permisos para cargar el view, se configuran
             * los eventos y se realizan las peticiones para obtener los
             * datos.
             * @function
             *
             * @name views.common.ViewSearch#allowed
             * @author <a href="mailto:mbaez@konecta.com.py">Maximiliano Báez</a>
             * @param {Object}options
             * @config {Backbone.Collection}collection el collection con
             *         utilizado para cargar los datos.
             * @config {String}attr el nombre del model el cual se va
             *          visualizar.
             * @config {String}[placeholder] El placeholder para el input.
             * @config {String}[cambiarLabel] El label del boton de cambiar.
             * @config {boolean}[setDefault] Indica si se cargará un valor
             *          por defecto en el input. Por defecto es true.
             * @config {boolean}[validate] Flag utilizado para habilitar
             *          o desabilitar la validación de los datos. Por
             *          defecto es `true`
             * @config {String}[prefijo] texto que se antepono al input
             *          editable. Por defecto su valor es "0".
             * @config {String}[defaultValue] el valor por defecto de la
             *          lista. Si el valor no existe se establece el primer
             *          elemento de la lista.
             */
            allowed: function (options) {
                this.data = options;
                //se valida el scope del view
                if (typeof this.data.scope == 'undefined') {
                    this.data.scope = options.el.attr("id");
                }
                if (typeof this.data.prefijo == "undefined") {
                    this.data.prefijo = "";
                }

                //Se inicializa el idMap
                this.idMap = {};
                //mascara de los eventos
                var mask = "#" + this.data.scope + "$value;" + this.data.attr;
                //se definen los ids de los elemntos del view
                this.idMap.input = mask.replace("$value;", "searchInput");
                this.idMap.cambiar = mask.replace("$value;", "cambiarButton");
                this.idMap.aceptar = mask.replace("$value;", "searchButton");
                //~ inicializar en loading state
                if (typeof this.collection == "undefined") {
                    this.loading();
                    return;
                }
                //se añaden los eventos
                this.collection.on('ready', this.render, this);
                this.collection.on('error', this.error, this);
                this.collection.on('error', this.render, this);
                this.loading();
                this.collection.fetch(GeoDengue.callback);
            },

            /**
             * Este metodo se encarga de renderizar el loading del view
             * @function
             *
             * @public
             * @name views.common.ViewSearch#loading
             * @author <a href="mailto:mbaez@konecta.com.py">Maximiliano Báez</a>
             */
            loading: function () {
                var data = $.extend({}, this.data);
                data.loading = true;
                //se construye el template
                var compTmpl = _.template(tmpl, {
                    data: data
                });
                this.$el.html(compTmpl);
                return true;
            },

            /**
             * Se establece el valor por defecto del input de busqueda.
             * @function
             *
             * @name views.common.ViewSearch#setDefault
             * @author <a href="mailto:mbaez@konecta.com.py">Maximiliano Báez</a>
             */
            setDefault: function () {
                if (this.collection.length > 0) {
                    var model;
                    var models = [];
                    //si se especifica el elemento por defecto, se
                    //realiza la busqueda en la lista.
                    if (typeof this.data.defaultValue != "undefined") {
                        var filter = {};
                        filter[this.data.attr] = this.data.defaultValue;
                        // se busca el elemento en la lista
                        models = this.collection.where(filter);
                    }
                    // se obtiene el model del elemento por defecto
                    if (models.length > 0) {
                        model = models[0];
                    } else {
                        //se obtiene el primer elemento del collection
                        model = this.collection.at(0);
                    }
                    //se selecciona el primer elemento
                    this.setSelected(model.get(this.data.attr));
                    //se dispara el evetno
                }
            },

            /**
             * Este metodo se encarga de renderizar el view
             * @function
             *
             * @public
             * @name views.common.ViewSearch#render
             * @author <a href="mailto:rquintana@konecta.com.py">Ramón Quintana</a>
             */
            render: function () {
                var data = {
                    data: this.data
                };
                data.data.items = this.collection.toJSON();
                var compTmpl = _.template(tmpl, data);
                this.$el.html(compTmpl);
                //se inicializa el autocompletado
                this.initSelectize();
                //se añaden los eventos de los botones
                this.eventProxy();
                //se establece el valor por defecto
                if (typeof this.data.setDefault == "undefined") {
                    this.setDefault();
                } else if (this.data.setDefault !== false && this.collection.length == 1) {
                    this.setDefault();
                }
                //se dispara un evento que indica que el view ya fue
                //renderizado.
                this.trigger("render");
                return this;
            },

            /**
             * Este metodo se encarga de añadir los handlers para los evento
             * onclik de los botones de view.
             * @function
             *
             * @name views.common.ViewSearch#eventProxy
             * @author <a href="mailto:mbaez@konecta.com.py">Maximiliano Báez</a>
             */
            eventProxy: function () {
                var thiz = this;
                this.$selectize.on('change', function () {
                    thiz.onAceptar();
                });
            },

            /**
             * Este metodo se encarga de disparar el evento `on-search`
             * inicidado al hacer click en el botton de busqueda.
             * @function
             *
             * @name views.common.ViewSearch#onAceptar
             * @author <a href="mailto:mbaez@konecta.com.py">Maximiliano Báez</a>
             */
            onAceptar: function (event) {
                var data = {};
                //se obtiene el valor del input
                //var value = $(this.idMap.input).val();
                var value = this.$selectize.getValue();
                //se verifica si esta habilitada la validación
                if (typeof this.data["validate"] == "undefined" ||
                    this.data.validate == true) {
                    data = this.validate(value);
                } else {
                    value = value.length > 0 && value[0] == "0" ? value.substring(1) : value;
                    data[this.data.attr] = value;
                }

                //si el data es null es porque ocurrio un error
                if (data != null) {
                    this.trigger('on-search', data);
                }
            },

            /**
             * Este metodo se encarga de validar que el `value` corresponda
             * a un elemento del collection.
             *
             * @function
             *
             * @name views.common.ViewSearch#onAceptar
             * @author <a href="mailto:mbaez@konecta.com.py">Maximiliano Báez</a>
             * @param value{String} el valor del attr del model
             */
            validate: function (value) {
                var data = null;
                var attributes = {};
                value = $(this.idMap.input).val();
                attributes[this.data.attr] = value
                data = this.collection.where(attributes);
                //si no exite en el collection retorna null
                if (data.length == 0) {
                    $(this.idMap.input).addClass("error");
                    $(this.idMap.input).focus();
                    return null;
                }
                return data[0].toJSON();
            },

            /**
             * Este metodo se encarga de establecer `value` como seleccionada
             * en el input.
             * @function
             *
             * @name views.common.ViewSearch#setSelected
             * @author <a href="mailto:mbaez@konecta.com.py">Maximiliano Báez</a>
             * @param {String}value el valor del attr del model
             */
            setSelected: function (value) {
                this.$selectize.setValue(value);
            },

            /**
             * Se ecarga de inicializar el plugin <a href="http://brianreavis.github.io/selectize.js/">selectize</a>
             * para implementar el selector.
             * @function
             *
             * @name views.common.ViewSearch#initSelectize
             * @author <a href="mailto:mbaez@konecta.com.py">Maximiliano Báez</a>
             */
            initSelectize: function () {
                /*se inicializa el config*/
                var config = {};
                var thiz = this;
                config.sortField = 'text';

                /*se construye el render */
                config.render = {
                    /**
                     * Se encarga de constuir el html para el elemento que se encuentra
                     * seleccionado.
                     */
                    item: function (item, escape) {
                        var $item = $(thiz.scope).find("#item-template").clone();
                        if (item.value.length > 0 && item.value[0] == thiz.data.prefijo) {
                            item.value = item.value.substring(1);
                        }

                        $item.find('[data-value]').attr('data-value', item.value);
                        $item.find('[data-value]').append(item.value);
                        return $item.html();
                    }
                }
                if (typeof this.data["validate"] != "undefined" && this.data.validate == false) {
                    config.create = true;
                    /**
                     * Se encarga de constuir el html para el elemento que es añadido
                     * a la lista.
                     */
                    config.render.option_create = function (item) {
                        var $item = $(thiz.scope).find("#create-template").clone();
                        $item.find('strong').text(item.input);
                        return $item.html();
                    }

                }
                /*se obtiene el target a inicializar*/
                var $select = $('#' + this.data.scope + 'searchInput' + this.data.attr);
                /*se inicializa el plugin*/
                var $select = $select.selectize(config);
                /*se extrae el objeto selectize para poder operar con el.*/
                this.$selectize = $select[0].selectize;
            }
        });
    }
);