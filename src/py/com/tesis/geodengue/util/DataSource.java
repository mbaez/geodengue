/**
 * 
 */
package py.com.tesis.geodengue.util;

import java.util.HashMap;

import org.w3c.dom.NamedNodeMap;
import org.w3c.dom.Node;

/**
 * Se encarga de leer los datos del datasource e inicializar el hashMap para
 * facilitar el acceso a los parámetros
 * 
 * @author Maximiliano Báez <mbaez@konecta.com.py>
 * @version 1.0 03/06/2012
 */
public class DataSource {

	private XMLManager xmlDataSource;
	private HashMap<String, String> dataSourceHashMap;
	private String xmlFile = "datasource.xml";

	/**
	 * Consturctor de la clase DataSource, encargada de manejar el datasource
	 * definidos en xml.
	 * 
	 * @throws Exception
	 *             si ocurrio un problema al procesar el xml del datasource
	 * 
	 * @see XMLManger
	 */
	public DataSource() throws Exception {
		try {
			// se establece el path de los archivos xml
			Package pack = getClass().getPackage();
			String packageName = pack.getName();
			String path = "/" + packageName.replace(".", "/");
			// se procesan los tags property unicamente
			xmlDataSource = new XMLManager(path + "/" + xmlFile, "property",
					getClass());
			// se inicializa la tabla hash
			dataSourceHashMap = new HashMap<String, String>();
			// se cargan los tags en la tabla
			initTable();
		} catch (Exception e) {
			e.printStackTrace();
			throw new Exception("Error al leer el archivo " + xmlFile, e);
		}

	}

	/**
	 * Inicializa la una tabla hash en donde se genera una entrada por cada
	 * property
	 */
	private void initTable() {
		Node cima;
		NamedNodeMap atributos;
		// se reinicia el puntero de la lista para comenzar a buscar desde el
		// inicio.
		xmlDataSource.reset();
		// se obtiene la cima
		cima = xmlDataSource.getNextNode();
		while (cima != null) {

			// se obtienen los atributos de la cima
			atributos = cima.getAttributes();
			/*
			 * se obtiene el nombre del query y el valor del mismo y se genera
			 * una nueva entrada en la tabla hash
			 */
			if (atributos.getNamedItem("name") != null) {
				dataSourceHashMap.put(atributos.getNamedItem("name")
						.getNodeValue(), cima.getTextContent());
			}
			// se obtiene el siguiente nodo
			cima = xmlDataSource.getNextNode();

		}
	}

	/**
	 * Este método obtiene valor del atributo value definido para el property de
	 * nombre name. Las configuraciones poseen la siguiente estructura <br/>
	 * < property name="nombreDeLaPropiedad" > value < /property>
	 * 
	 * @param name
	 *            es nombre de la propiedad
	 * @return el valor del property
	 */
	public String getPropertyByName(String name) throws Exception {

		String property = (String) dataSourceHashMap.get(name);
		if (property == null) {
			throw new Exception("La configuración " + name + " no existe");
		}
		return property;
	}
}
