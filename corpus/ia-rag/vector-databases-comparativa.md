# Bases de datos vectoriales: comparativa

## Qué resuelven

Una base de datos vectorial indexa embeddings para responder eficientemente a la pregunta
"¿cuáles son los k vectores más cercanos a este vector de consulta?" sobre millones de vectores,
sin comparar contra cada uno linealmente (búsqueda exacta por fuerza bruta, `O(n)`). Usan
estructuras de índice aproximado (ANN — Approximate Nearest Neighbor) como HNSW o IVF, que
sacrifican una pequeña cantidad de precisión (puede no devolver *exactamente* los k más
cercanos, sino una aproximación muy buena) a cambio de búsquedas sub-lineales, mucho más rápidas
a gran escala.

## Opciones principales

| Opción | Tipo | Cuándo tiene sentido |
|---|---|---|
| **pgvector** (extensión de Postgres) | Extensión SQL | Ya usas Postgres/Supabase; quieres vectores y datos relacionales en la misma base, con transacciones y joins normales. Ideal para proyectos pequeños-medianos sin infraestructura extra. |
| **Pinecone** | Servicio gestionado dedicado | Necesitas escalar a decenas de millones de vectores con SLA de latencia garantizado, sin operar infraestructura propia. Tiene costo desde cierto volumen. |
| **Weaviate** | Base vectorial open-source, self-hosted o cloud | Quieres búsqueda híbrida (vectorial + palabras clave) y filtros complejos con un motor especializado, con la opción de auto-hospedarlo. |
| **Milvus** | Base vectorial open-source, orientada a gran escala | Casos de miles de millones de vectores, alta necesidad de tuning fino del índice, equipo con capacidad de operar infraestructura compleja. |
| **Chroma** | Embebida / local | Prototipado rápido, demos, proyectos sin necesidad de un servicio separado — corre en el mismo proceso de la aplicación. |

## Índices HNSW vs IVF

**HNSW** (Hierarchical Navigable Small World) construye un grafo en capas donde cada nodo se
conecta a sus vecinos más cercanos; la búsqueda navega el grafo desde una capa superior (menos
nodos, saltos grandes) hacia capas inferiores (más nodos, saltos precisos). No requiere una
fase de "entrenamiento" previa con datos representativos y da muy buen recall/latencia para
la mayoría de los tamaños de corpus, por lo que es el default recomendado en pgvector moderno.
**IVF** (Inverted File Index) agrupa vectores en clusters (`lists`) mediante k-means y solo
busca dentro de los clusters más cercanos al vector de consulta; requiere elegir el número de
`lists` según el tamaño del dataset y re-entrenar si los datos cambian mucho, lo que lo hace más
delicado de mantener que HNSW para un corpus que crece incrementalmente.

## Filtrado por metadata

En RAG casi siempre se necesita combinar la búsqueda vectorial con filtros exactos (por
ejemplo, "solo documentos del módulo `backend`"). Todas las opciones anteriores soportan
filtrado por metadata junto con la búsqueda ANN, pero la eficiencia de combinar ambos varía: en
pgvector, un índice B-tree normal sobre la columna de metadata (ej. `module`) complementa al
índice HNSW del vector, y Postgres decide el plan de ejecución óptimo igual que en cualquier
consulta SQL normal.
