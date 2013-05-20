/**
 * Define el módulo Page que extiende de Backbone.View. Un Page
 * es un contenedor de alto nivel que contiene multiples views.
 * <br/>
 * Un page cuenta básicamente con 2 estados : <br/>
 * <ul><li>
 *  <b>Open<b> : Cuando el page esta activo y siendo utilizado
 *  todos los eventos se ecuentran asociados al page en este estado.
 * </li>
 * <li>
 *  <b>Close</b> : El page en este estado no cuenta con eventos
 *  asociados.
 * </li> </ul>
 * @author <a href="mailto:mxbg.py@gmail.com.py">Maximiliano Báez</a>
 */
Backbone.Page = Backbone.View.extend({});
_.extend(Backbone.Page.prototype, {

    /**
     * Este método se encarga de desasociar todos los eventos del
     * page actual.
     * @author <a href="mailto:mxbg.py@gmail.com.py">Maximiliano Báez</a>
     */
    close : function(){
        this.undelegateEvents();
        this.$el.removeData().unbind();
        this.$el.html("");
    }
});
