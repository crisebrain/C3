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