package py.com.tesis.geodengue;

import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.HttpURLConnection;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import py.com.tesis.geodengue.util.DataSource;
import py.com.tesis.geodengue.util.Util;

/**
 * Este servlet se encarga de actuar como un proxy entre la aplicación y los
 * servlets de autenticación del geoserver.
 * 
 * @author Maximiliano Báez <mbaez@konecta.com.py>
 * @see Util
 */
@WebServlet("/Security")
public class Security extends HttpServlet {
	private static final long serialVersionUID = 1L;

	/**
	 * @see HttpServlet#HttpServlet()
	 */
	public Security() {
		super();
	}

	/**
	 * Las peticiones get a este servlet son para finalizar la sesión
	 * establecida con el geoserver. El cliente de pasarle como parametros al
	 * servlet la url del geoserver, de forma que estos puedan ser extraidos del
	 * request. <br/>
	 * http://miurl.com.py/Sercurity?url=http://urldelgeoserver/geoserver/
	 * servlet de logout <br/>
	 * Una vez establecida la conexion, el servlet se encarga de copiar las
	 * cabeceras de la petición al response.
	 * 
	 * @see Util#prepareConnection(HttpServletRequest, boolean)
	 * @see Util#writeResponseHeaders(HttpServletResponse, HttpURLConnection)
	 * @see HttpServlet#doGet(HttpServletRequest request, HttpServletResponse
	 *      response)
	 */
	protected void doGet(HttpServletRequest request,
			HttpServletResponse response) throws ServletException, IOException {

		BufferedInputStream conInputStream = null;
		BufferedOutputStream responseOutputStream = null;
		HttpURLConnection con;

		try {
			int statusCode;
			int oneByte;
			// se compian los datos de la petición
			con = Util.prepareConnection(request);
			// se obtene el estado de la peticion
			statusCode = con.getResponseCode();
			response.setStatus(statusCode);

			// System.out.println(getClass() + " :  > GET" + " RESPONSE : "
			// + statusCode);
			// se copian las cabeceras del conexión a las cabeceras del
			// response
			Util.writeResponseHeaders(response, con);
			// se inicializan los buffers
			conInputStream = new BufferedInputStream(con.getInputStream());
			responseOutputStream = new BufferedOutputStream(
					response.getOutputStream());
			// se escribe byte a byte en el response el resultado de la peticíon
			while ((oneByte = conInputStream.read()) != -1)
				responseOutputStream.write(oneByte);
			// se cierran los buffers
			responseOutputStream.flush();
			responseOutputStream.close();
			conInputStream.close();
			// se cierra la conexión
			con.disconnect();

		} catch (Exception e) {
			System.err.println(e.getMessage());
		}
	}

	/**
	 * Las peticiones post a este servlet son para establecer una sesión con el
	 * geoserver. El servlet actua como un proxy para realizar la autenticación,
	 * el cliente de pasarle como parametros al servlet la url el usuario y la
	 * contraseña del geoserver, de forma que estos puedan ser extraidos del
	 * request. Una vez establecida la conexion, el servlet se encarga de copiar
	 * las cabeceras de la petición al response. Posteriormente se modifican las
	 * cabeceras del cookie y el location.
	 * 
	 * @see Util#prepareConnection(HttpServletRequest, boolean)
	 * @see Util#writeResponseHeaders(HttpServletResponse, HttpURLConnection)
	 * @see HttpServlet#doPost(HttpServletRequest request, HttpServletResponse
	 *      response)
	 * @see #procesarParametros(HttpServletRequest)
	 */
	protected void doPost(HttpServletRequest request,
			HttpServletResponse response) throws ServletException, IOException {

		BufferedReader conInputStream = null;
		PrintWriter responseWriter = null;
		HttpURLConnection con;

		try {
			int statusCode;
			String urlString = procesarParametros(request);
			con = Util.prepareConnection(request, urlString, false);
			// se copian los los datos del post
			Util.prepareRequest(request, con);
			// se obtene el estado de la peticion
			statusCode = con.getResponseCode();
			response.setStatus(statusCode);
			// se copian las cabeceras del conexión a las cabeceras del
			// response
			Util.writeResponseHeaders(response, con);
			// Geoserver maneja su autenticación via una cookie, se obtiene el
			// valor
			// de la cookie y se escribe el el hader del response
			String cookie = response.getHeader("Set-Cookie");
			if (cookie != null) {
				// se extrae de la cookie el sessionid
				cookie = cookie.substring(0, cookie.indexOf(";"));
				// se escribe el cookie en el response
				response.setHeader("Set-Cookie", cookie);
			}
			// se obtiene la url el path del servlet
			String localUrl = request.getRequestURL().toString();
			// se elimina el nombre del servlet
			localUrl = localUrl.replace(getClass().getName(), "");
			// geoserver establece el location de su home "/geoserver/web..."
			// se reeplaza el location de geoserver
			response.setHeader("Location", localUrl);
			conInputStream = new BufferedReader(new InputStreamReader(
					con.getInputStream()));
			// se obtiene el writer del response
			responseWriter = response.getWriter();
			String line;
			// se escribe en el response el resultado de la peticíon
			while ((line = conInputStream.readLine()) != null) {
				responseWriter.println(line);
			}
			// se cierran los buffers
			responseWriter.flush();
			responseWriter.close();
			conInputStream.close();
			// se cierrra la conexión
			con.disconnect();

		} catch (Exception e) {
			System.err.println(e.getMessage());
		}
	}

	/**
	 * Procesa los parametros de la url, en el caso de que se le envie el token
	 * de seesion se desencripta y se extrae el usuario y contraseña. En el caso
	 * de que se reciva los parametros username y password, los extrae y genera
	 * la url. <br/>
	 * http://miurl.com.py/Sercurity?url=http://urldelgeoserver/geoserver/
	 * servlet de login <br/>
	 * Los datos del post <br/>
	 * username=miusuario&password=mipassword <br/>
	 * 
	 * @throws Exception
	 * 
	 * @see {@link Util#getRequestParameters(HttpServletRequest)}
	 * @see #desencriptar(String, String)
	 */
	private String procesarParametros(HttpServletRequest request)
			throws Exception {
		DataSource datasource = new DataSource();
		String urlString = request.getParameter("url");
		String username = datasource.getPropertyByName("username");
		String password = datasource.getPropertyByName("password");
		urlString += "?username=" + username;
		urlString += "&password=" + password;
		System.out.println(urlString);
		return urlString;
	}
}
