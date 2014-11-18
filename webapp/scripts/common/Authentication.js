
/**
 * Esta clase ofrece métodos para la autenticacion de usuarios con el servidor
 * de mapas geoserver mediante los metodos post y get.
 *
 * @autor Maximiliano Báez <mxbg.py@gmail.com>
 */
Authentication = function() {

	var baseUrl = DataSource.server;
	this.url = "/rplaces/Security?url="+baseUrl;
	/**
	 * Realiza un get al servlet de geosercer para cerrar la sesión establecida.
	 *
	 * @autor Maximiliano Báez <mxbg.py@gmail.com>
	 *
	 * @return el codigo del estado de la petición
	 */
	this.logout = function(options) {
		// url del servlet del geoserver
		var theUrl = this.url + "/geoserver/j_spring_security_logout";
		var xmlHttp = new XMLHttpRequest();
		xmlHttp.open("GET", theUrl, false);
		this.expiresCookie();
		var ajax = $.ajax({
			type : "GET",
			url : theUrl
		});
		// se ejecuta cuando la peticion finaliza
		ajax.done(function() {
			if (options && options.success) {
				options.success();
			}
		});
		// si ocurrio un error al realizar la peticion
		ajax.fail(function(data) {
			if (options && options.failure) {
				options.failure(data);
			}
		});
		// se ejecuta siempre al final de la petición, sin importar que esta
		// haya fallado
		ajax.always(function() {
			if (options && options.always) {
				options.always();
			}
		});

	};

	/**
	 * Se encarga de procesar las cookies y hacer que expire el SESSIONID.
	 *
	 * @autor Maximiliano Báez <mxbg.py@gmail.com>
	 */
	this.expiresCookie = function() {
		$.cookie("SPRING_SECURITY_REMEMBER_ME_COOKIE", null);
		$.cookie("JSESSIONID", null);
	};

	/**
	 * Realiza un post al servlet de geoserver para establecer una sesión.
	 *
	 * @autor Maximiliano Báez <mxbg.py@gmail.com>
	 *
	 * @param user
	 *            el codigo de usuario con el cual se iniciara sesión.
	 * @param password
	 *            la contraseña para el usuario especificado.
	 * @return el codigo del estado de la petición
	 */
	this.login = function(options) {
		// url del servlet del geoserver
		var url = this.url + "/geoserver/j_spring_security_check";
		// parametros para el login
		var contentType = "application/x-www-form-urlencoded";
		//se inicializa la petición ajax
		var ajax = $.ajax({
			type : "POST",
			contentType : contentType,
			url : url
		});
		// se ejecuta cuando la peticion finaliza
		ajax.done(function() {

			if ($.cookie("JSESSIONID") != null && options && options.success) {
				options.success();
			}
		});
		// si ocurrio un error al realizar la peticion
		ajax.fail(function(data) {
			if (options && options.failure) {
				options.failure(data);
			}
		});
		// se ejecuta siempre al final de la petición, sin importar que esta
		// haya fallado
		ajax.always(function() {
			if (options && options.always) {
				options.always();
			}
		});
	};
};
