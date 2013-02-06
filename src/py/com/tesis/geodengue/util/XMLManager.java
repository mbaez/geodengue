/**
 * 
 */
package py.com.tesis.geodengue.util;

import java.io.IOException;
import java.io.InputStream;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;

import org.w3c.dom.Document;
import org.w3c.dom.NamedNodeMap;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;
import org.xml.sax.SAXException;

/**
 * @author Maximiliano Báez <mbaez@konecta.com.py>
 * @version 1.0 03/06/2012
 */
public class XMLManager {
	/**
	 * Lista de nodos del xml
	 */
	private NodeList nodeList;
	/**
	 * Nodo actualmnete visitado
	 */
	private Node nodeCima;
	/**
	 * Indice que apunta a la posición del nodo actual
	 */
	private int index = 0;
	/**
	 * Clase en cuyo .jar se encuentra el el xml que se desea procesar
	 */
	@SuppressWarnings("rawtypes")
	private Class clazzSource;

	/**
	 * Consturctor de la clase XMLManager, encargada de manejar las
	 * configuraciones establecidas en archivos xml.
	 * 
	 * @param xmlFile
	 *            Nombre del archivo xml.
	 * @param tagName
	 *            Nombre del tag contenido en la raiz.
	 * @param clazzSoruce
	 *            Referencia a la clase desde la cual se utilizara el
	 *            XMLManager, en cuyo .jar se encuentra el el xml que se desea
	 *            procesar.
	 * 
	 * @throws SAXException
	 *             Si ocurrio un error parsear el XML de configuración.
	 * @throws IOException
	 *             Si no se pudo cargar el archivo de configuración.
	 * @throws ParserConfigurationException
	 *             Si ocurrio un error al configurar el parser XML.
	 * 
	 * @see #parse(String, String)
	 */
	public XMLManager(String xmlFile, String tagName, Class<?> clazzSource)
			throws SAXException, IOException, ParserConfigurationException {
		this.clazzSource = clazzSource;
		parse(xmlFile, tagName);
	}

	/**
	 * Este método se encarga de cargar y parsear el xmlFile, posteriormente se
	 * obtiene de la lista de nodos identificados por el tagName existentes en
	 * el xmlFile.
	 * 
	 * @param xmlFile
	 *            Nombre del archivo xml.
	 * @param tagName
	 *            Nombre del tag contenido en la raiz.
	 * 
	 * @throws SAXException
	 *             Si ocurrio un error parsear el XML.
	 * @throws IOException
	 *             Si no se pudo cargar el xmlFile.
	 * @throws ParserConfigurationException
	 *             Si ocurrio un error al configurar el parser XML.
	 */
	private void parse(String xmlFile, String tagName) throws SAXException,
			IOException, ParserConfigurationException {

		DocumentBuilderFactory docFactory = DocumentBuilderFactory
				.newInstance();

		DocumentBuilder docBuilder = docFactory.newDocumentBuilder();
		// Se carga el archivo que se encuentra en el path del clazzSource
		InputStream is = clazzSource.getClassLoader().getResourceAsStream(
				xmlFile);
		// se parsea el xml apartir del inpuntStream
		Document doc = docBuilder.parse(is);

		doc.getDocumentElement().normalize();
		// se obtienen la lista de nodos identificados con el tagName
		nodeList = doc.getElementsByTagName(tagName);

	}

	/**
	 * Este método obtiene el nodo de la cima e incrementa el indice de la
	 * lista.
	 * 
	 * @return el nodo cima de la lista.
	 * @see #reset()
	 */
	public Node getNextNode() {
		nodeCima = null;
		if (nodeList.getLength() > index) {
			// se obtiene el nodo de la cima
			nodeCima = nodeList.item(index);
			// se incrementa el puntero
			index++;
		}
		return nodeCima;
	}

	/**
	 * Este método obtiene los atributos del nodo que se encuentra en la cima de
	 * la lista.
	 * 
	 * @return los atributos del nodo que se encuentra en la cima.
	 * @see #getNextNode()
	 */
	public NamedNodeMap getNodeAttributes() {
		return nodeCima.getAttributes();
	}

	/**
	 * Este método reinicia el valor del indice de la lista, una vez reiniciado
	 * el indice, este apunta al primer nodo de la lista.
	 * 
	 * @see #getNextNode()
	 */
	public void reset() {
		// se reinicia el indice de la lista para que apunte al primer nodo de
		// la lista
		index = 0;
	}

	/**
	 * Este método retorna una referencia a la lista de nodos del archivo xml
	 * 
	 * @return la lista de nodos que poseen el tag especificado en el
	 *         constructor
	 * @see #XMLManager(String, String)
	 */
	public NodeList getNodeLis() {
		return nodeList;
	}

}
