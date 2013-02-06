package py.com.tesis.geodengue;


import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.IOException;
import java.net.HttpURLConnection;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import py.com.tesis.geodengue.util.Util;

/**
 * Servlet implementation class Proxy
 * 
 * @author Maximiliano Báez <mbaez@konecta.com.py>
 */
@WebServlet("/Proxy")
public class Proxy extends HttpServlet {
	private static final long serialVersionUID = 1L;

	/**
	 * @see HttpServlet#HttpServlet()
	 */
	public Proxy() {
		super();
	}

	/**
	 * @see HttpServlet#doGet(HttpServletRequest request, HttpServletResponse
	 *      response)
	 */
	protected void doGet(HttpServletRequest request,
			HttpServletResponse response) throws ServletException, IOException {
		BufferedInputStream webToProxyBuf = null;
		BufferedOutputStream proxyToClientBuf = null;
		HttpURLConnection con;

		try {
			int statusCode;
			int oneByte;
			con = Util.prepareConnection(request, false);
			statusCode = con.getResponseCode();
			// System.out.println(request.getParameter("url")
			// + " > GET RESPONSE : " + statusCode);
			response.setStatus(statusCode);
			Util.writeResponseHeaders(response, con);

			webToProxyBuf = new BufferedInputStream(con.getInputStream());
			proxyToClientBuf = new BufferedOutputStream(
					response.getOutputStream());

			while ((oneByte = webToProxyBuf.read()) != -1)
				proxyToClientBuf.write(oneByte);

			proxyToClientBuf.flush();
			proxyToClientBuf.close();

			webToProxyBuf.close();
			con.disconnect();

		} catch (Exception e) {
			System.err.println(e.getMessage());
		} finally {
		}
	}

	/**
	 * @see HttpServlet#doPost(HttpServletRequest request, HttpServletResponse
	 *      response)
	 */
	protected void doPost(HttpServletRequest request,
			HttpServletResponse response) throws ServletException, IOException {
		BufferedInputStream webToProxyBuf = null;
		BufferedOutputStream proxyToClientBuf = null;
		HttpURLConnection con;

		try {
			int statusCode;
			int oneByte;
			con = Util.prepareConnection(request, false);
			// se copian los los datos del post
			Util.prepareRequest(request, con);

			statusCode = con.getResponseCode();
			//System.out.println(request.getParameter("url")
			//		+ " > POST RESPONSE : " + statusCode);

			response.setStatus(statusCode);
			Util.writeResponseHeaders(response, con);

			webToProxyBuf = new BufferedInputStream(con.getInputStream());
			proxyToClientBuf = new BufferedOutputStream(
					response.getOutputStream());

			while ((oneByte = webToProxyBuf.read()) != -1)
				proxyToClientBuf.write(oneByte);

			proxyToClientBuf.flush();
			proxyToClientBuf.close();

			webToProxyBuf.close();
			con.disconnect();

		} catch (Exception e) {
			System.err.println(e.getMessage());
			
		} finally {
		}
	}
}
