# C3
Repositorio para el proyecto C3

Plataforma ed trabajo para el equipo desarrollador del proyecto C3

Cambios lunes 23
- Un metodo para la clase IntentTree para que se creen los nodos a partir de un json
- Que cada nodo se guarde en una lista atributo del intentTree
- Y un método para que dado el nombre de un nodo lo devuelva ya sea en forma de un objeto json o el nodo en sí

Cambios martes 24
- Edicion de las clases IntentNode e IntentTree para que se puedan añadir nuevos nodos sobre un parent dado su nombre o tambien puede añadirse al árbol por su profundidad.
- Los nodos son creados con dos parametros: parent - que puede ser el nombre del nodo padre o el mismo nodo padre mediante una búsqueda, o por la posición que ocupa en la lista de nodos atributo del arbol, los demás parámetros como nombre del nodo, valor, etc, se añaden desde el json que se le pasé como argumento al constructor.

Cambios miercoles 25
- Modificación de nombres de componentes a Inglés y asignación de módulos para cada uno con imports relativos.
- Reubicación de módulos por servicios

Cambios (28/04/2018 y 29/04/2018):
- Moví el ChatBotWrapper.py fuera de su folder para poder leer de Utils y escribir en Sessions (estoy escribiendo un objeto lista de IntentTrees que fue lo que vimos en la reunión).
- Corregí el método find_node, agregando una validación por si el node es None y to_dict es True, probé los métodos init y add_node del IntentTree. No pude probar el SessionContainer pues no encontré un ejemplo, en la raíz del branch habían ejemplos para interactuar con el árbol y esos fue los que utilicé.
- En DialogFlow ya está el chatbot y en el folder chatbots están todos los json asociados, para automatizar este proceso se necesita vincular a projecto google y hay que insertar una tarjeta de crédito, de lo contrario este proceso de export se tiene que hacer manual. Si se automatiza hay que cambiar la implementación actual.
- Se completó el método publishIntentTree a partir del folder donde deben aparecer todos los chatbots disponibles.

Cambios (30/04/2018 y 1/05/2018):
- Ajuste de conversación de dialogFlow a flujo de conversaciones con infomanager.
- Navegacion de intents con sessioncontainer, el arbol lo construye chatbotwrapper y sessioncontainer lo resguarda para poder navegar sobre él.
- por ahora se puede probar corriendo ejemplo_infomanager con "python ejemplo_infomanager".

Adición de servicio de webhook vdn (13/05/2018):
- Servicio de Webhook con busqueda de vdn por request de dialogFlow. Nota: Falta probar con dialog Flow, pero ya debería de funcionar puesto que se utiliza la estructura de intent que se supone envía en el request.
- Uso de un json almacenado en query_VDN.json como el query enviado por DialogFlow.
- Creación de mensaje y código de error según el numero de coincidencias de la petición a dialogFlow.
- Uso de Base de datos ficticia con un txt.

Cambios 12/05/2018:
- Se especificó la clase CognitiveSearchEngine.py, se implementó un NER para nombres, locaciones y se extraen todos los números de la sentencia.
- Cada método fue especificado para su posterior implementación. Incluyendo en la especificación: entrada, algoritmia, salida.

Cambios 15/05/2018:
- Se terminó la validación de los webservices de prueba para la fase uno, mismos que trabajan con DialogFlow y ngrok para exponer el servicio.
