# Embeddings: fundamentos

## Qué es un embedding

Un embedding es una representación numérica de un texto (una palabra, una oración, un
documento) como un vector de punto flotante de dimensión fija (ej. 384, 768, 1536 dimensiones),
generado por un modelo entrenado para que textos con significado similar produzcan vectores
cercanos en ese espacio. La cercanía se mide típicamente con **similitud coseno** (el ángulo
entre dos vectores, ignorando su magnitud) o distancia euclidiana. A diferencia de una búsqueda
por palabras clave (que requiere coincidencia léxica exacta o parcial), una búsqueda por
embeddings encuentra resultados **semánticamente** relacionados aunque no compartan ninguna
palabra literal — por ejemplo, "cómo evitar que mi API sea lenta" y "optimización de
rendimiento en backend" pueden tener embeddings muy cercanos.

## Modelos de embeddings: locales vs API

Modelos como `sentence-transformers/all-MiniLM-L6-v2` corren localmente (CPU o GPU), son
gratuitos y livianos (~80MB, 384 dimensiones), suficientes para la mayoría de los casos de RAG
de propósito general. Modelos vía API (OpenAI `text-embedding-3-small`, Cohere) suelen tener
mayor calidad en dominios muy específicos o multilingües avanzados, a cambio de costo por
token y una dependencia de red en el pipeline de ingesta y de consulta. La elección depende del
presupuesto y de si la ganancia de calidad justifica el costo y la latencia adicional — para un
corpus de tamaño moderado y dominio bien delimitado, un modelo local suele ser suficiente.

## Normalización de embeddings

Normalizar un vector (dividirlo por su magnitud, dejándolo con longitud 1) simplifica el cálculo
de similitud: la similitud coseno entre dos vectores normalizados es simplemente su producto
punto, lo cual es más barato de calcular y es lo que la mayoría de las bases de datos
vectoriales optimizan internamente (`vector_cosine_ops` en pgvector, por ejemplo). Es importante
normalizar de forma consistente tanto en la ingesta (embeddings de los documentos) como en cada
consulta (embedding de la pregunta del usuario) — mezclar vectores normalizados y no
normalizados produce comparaciones sin sentido.

## Chunking: por qué no se embebe el documento completo

Los modelos de embeddings tienen un límite de tokens de entrada, y además un vector único para
un documento largo diluye información específica (promedia demasiados temas distintos en un solo
punto del espacio vectorial). Por eso el texto se divide en **chunks** (fragmentos) más pequeños
antes de embeber, cada uno con su propio vector, permitiendo recuperar la sección exacta más
relevante en vez de todo el documento. El tamaño de chunk es un trade-off: chunks muy pequeños
pierden contexto (una definición cortada a la mitad), chunks muy grandes diluyen la relevancia
del fragmento recuperado y desperdician espacio de contexto del LLM.

## Overlap entre chunks

Superponer una porción de texto entre chunks consecutivos (ej. 15% del tamaño del chunk) reduce
el riesgo de que una idea completa quede partida exactamente en el límite entre dos chunks, a
costa de un poco de redundancia en el índice. Es una mitigación simple y barata que mejora
notablemente el recall en la práctica sin requerir chunking "inteligente" basado en NLP.
