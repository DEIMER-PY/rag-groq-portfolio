# Bases de datos NoSQL (MongoDB y Redis)

## Documentos vs filas

MongoDB almacena datos como documentos BSON (similar a JSON) dentro de colecciones, sin un
esquema fijo obligatorio: dos documentos en la misma colección pueden tener campos distintos.
Esto da flexibilidad para datos con estructura variable o que cambia con frecuencia, pero
traslada la responsabilidad de mantener la consistencia estructural a la aplicación (o a
validaciones de esquema opcionales que MongoDB sí soporta, `$jsonSchema`). La decisión entre un
modelo relacional y uno de documentos no es "cuál es mejor" en abstracto, sino qué patrón de
acceso predomina: si los datos se leen casi siempre completos como una unidad (un pedido con
sus líneas embebidas), un documento evita joins; si los datos se relacionan de muchas formas
distintas y consultan de igual forma (reportes, agregaciones cruzadas), un modelo relacional
suele ser más natural.

## Embeber vs referenciar

En MongoDB, la alternativa a un JOIN de SQL es decidir entre **embeber** datos relacionados
dentro del mismo documento (rápido de leer, pero duplica información y puede hacer crecer el
documento sin límite) o **referenciar** por ID a otra colección (evita duplicación, pero
requiere una consulta adicional o un `$lookup` para "unir" datos, similar a un join). Regla
práctica: embeber cuando la relación es de composición fuerte, tiene un límite natural de
tamaño y se lee siempre junta (ej. las direcciones de envío de un pedido); referenciar cuando la
entidad relacionada se actualiza independientemente, es compartida por muchos documentos, o
puede crecer sin límite (ej. los comentarios de un post con miles de comentarios).

## Índices en MongoDB

Igual que en SQL, un índice (`db.collection.createIndex({ campo: 1 })`) acelera consultas por
ese campo a costa de espacio y de velocidad de escritura. Los índices compuestos siguen la
misma regla de orden de columnas que en SQL, y MongoDB también soporta índices de texto
completo y geoespaciales para casos de uso específicos que no requieren una solución externa.

## Redis como cache y almacén de estructuras

Redis es una base de datos en memoria usada típicamente como cache (reduce carga sobre la base
de datos principal para lecturas frecuentes y costosas) o como almacén de estructuras de datos
especializadas: listas, sets, sorted sets (útiles para rankings/leaderboards), y hashes. Un
patrón común de cache es **cache-aside**: la aplicación primero consulta Redis; si no está
(`cache miss`), consulta la base de datos principal, guarda el resultado en Redis con un TTL
(tiempo de expiración), y lo devuelve. El TTL es crítico: sin expiración, el cache puede servir
datos obsoletos indefinidamente tras una actualización en la fuente de verdad.

## Consistencia eventual

Muchas bases NoSQL distribuidas priorizan disponibilidad y tolerancia a particiones sobre
consistencia inmediata (teorema CAP): una escritura puede tardar en propagarse a todas las
réplicas, por lo que una lectura inmediatamente después de escribir en un nodo distinto podría
no reflejar el cambio todavía. Esto es aceptable para casos como contadores de "me gusta" o
analíticas, pero no para datos donde la consistencia inmediata es crítica (saldos financieros),
donde una base relacional con transacciones ACID sigue siendo la elección más segura.
