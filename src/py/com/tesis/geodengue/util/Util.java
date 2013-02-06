/**
 * 
 */
package py.com.tesis.geodengue.util;

import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.net.HttpURLConnection;
import java.net.URL;
import java.net.URLEncoder;
import java.util.Enumeration;
import java.util.Iterator;
import java.util.List;
import java.util.Map;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

/**
 * @author Maximiliano Báez <mbaez@konecta.com.py>
 * 
 */
public class Util {
	public static void prepareRequest(HttpServletRequest request,
			HttpURLConnection con) throws IOException {
		int oneByte;
		BufferedInputStream clientToProxyBuf = new BufferedInputStream(
				request.getInputStream());
		BufferedOutputStream proxyToWebBuf = new BufferedOutputStream(
				con.getOutputStream());
		while ((oneByte = clientToProxyBuf.read()) != -1) {
			proxyToWebBuf.write(oneByte);
		}
		proxyToWebBuf.flush();
		proxyToWebBuf.close();
		clientToProxyBuf.close();
	}

	/**
	 * 
	 * @param response
	 * @param con
	 */
	@SuppressWarnings("rawtypes")
	public static void writeResponseHeaders(HttpServletResponse response,
			HttpURLConnection con) {

		for (Iterator i = con.getHeaderFields().entrySet().iterator(); i
				.hasNext();) {
			Map.Entry mapEntry = (Map.Entry) i.next();
			if (mapEntry.getKey() != null) {
				String key = mapEntry.getKey().toString();
				String value = ((List) mapEntry.getValue()).get(0).toString();
				response.setHeader(key, value);
			}
		}
	}

	/**
	 * 
	 * @param request
	 * @return
	 * @throws IOException
	 */
	public static HttpURLConnection prepareConnection(HttpServletRequest request)
			throws IOException {
		return prepareConnection(request, true);
	}

	/**
	 * 
	 * @param request
	 * @param requestParameters
	 * @param followRedirects
	 * @return
	 * @throws IOException
	 */
	public static HttpURLConnection prepareConnection(
			HttpServletRequest request, String urlString,
			boolean followRedirects) throws IOException {
		String methodName;
		HttpURLConnection con;
		// se concatena los parametros
		URL url = new URL(urlString);

		con = (HttpURLConnection) url.openConnection();

		methodName = request.getMethod();
		con.setRequestMethod(methodName);
		con.setDoOutput(true);
		con.setDoInput(true);
		con.setInstanceFollowRedirects(followRedirects);
		con.setAllowUserInteraction(true);
		con.setUseCaches(true);

		for (Enumeration<String> e = request.getHeaderNames(); e
				.hasMoreElements();) {
			String headerName = e.nextElement().toString();
			con.setRequestProperty(headerName, request.getHeader(headerName));
		}
		con.connect();
		return con;

	}

	/**
	 * 
	 * @param request
	 * @param con
	 * @return
	 * @throws IOException
	 */
	public static HttpURLConnection prepareConnection(
			HttpServletRequest request, boolean followRedirects)
			throws IOException {
		String urlString = request.getParameter("url");
		urlString += getRequestParameters(request);

		return prepareConnection(request, urlString, followRedirects);
	}

	/**
	 * Este método extrae los parametros del request.
	 * 
	 * @param request
	 *            El request de la petición
	 * @return Una cadena que contienelos parametros del request.
	 * @throws UnsupportedEncodingException
	 */
	@SuppressWarnings("deprecation")
	public static String getRequestParameters(HttpServletRequest request)
			throws UnsupportedEncodingException {
		String formData = "?";
		// se procesan los parametros del request
		for (Enumeration<String> e = request.getParameterNames(); e
				.hasMoreElements();) {
			String name = e.nextElement();
			// no se tienen el parametro url
			if (!name.equals("url")) {
				formData += URLEncoder.encode(name);
				formData += "=" + URLEncoder.encode(request.getParameter(name));
				// se añade el and entre los parametros
				formData += "&";
			}
		}
		// si no exiten parametros
		formData = formData.substring(0, formData.length() - 1);
		// se retorna los parametros
		return formData;
	}
}
