# Arquitectura de un sistema RAG

## Por qué RAG en vez de fine-tuning o un LLM "puro"

Un LLM entrenado tiene conocimiento congelado a la fecha de su entrenamiento y no conoce datos
privados o específicos de un dominio (documentación interna, tu propio contenido). El
fine-tuning (reentrenar el modelo con datos propios) es costoso, requiere reentrenar cada vez
que los datos cambian, y no elimina las alucinaciones. RAG (Retrieval-Augmented Generation)
resuelve esto de forma más barata y actualizable: en vez de "enseñarle" datos al modelo, se le
**da el contexto relevante en el prompt** en el momento de la consulta, recuperado desde una
base de conocimiento externa que se puede actualizar sin volver a entrenar nada.

## Las dos fases de un pipeline RAG

1. **Ingesta (offline, se ejecuta cuando cambian los datos)**: cargar documentos fuente →
   dividir en chunks → generar embeddings de cada chunk → guardar chunk + embedding + metadata
   en una base de datos vectorial.
2. **Consulta (online, en cada pregunta del usuario)**: generar embedding de la pregunta →
   buscar los k chunks más similares en la base vectorial → construir un prompt que incluya esos
   chunks como contexto → enviar el prompt al LLM → devolver la respuesta generada, idealmente
   con las fuentes citadas.

## Componentes y responsabilidad de cada uno

- **Chunker**: decide cómo dividir el texto (tamaño, overlap, respeto de límites semánticos
  como headings o párrafos).
- **Modelo de embeddings**: convierte texto en vectores; debe ser el **mismo modelo** en
  ingesta y en consulta, porque espacios vectoriales de modelos distintos no son comparables
  entre sí.
- **Vector store**: indexa y busca por similitud, opcionalmente combinado con filtros de
  metadata exactos.
- **Orquestador del pipeline**: la lógica que conecta retrieval → construcción de prompt →
  llamada al LLM → post-procesamiento de la respuesta. Puede ser código propio (más
  transparente y controlable) o un framework como LangChain/LlamaIndex (más rápido de
  prototipar, pero añade una capa de abstracción sobre el flujo real).
- **LLM generador**: produce la respuesta final en lenguaje natural a partir del contexto
  recuperado y la pregunta.

## Retrieval como el cuello de botella real

En la práctica, la calidad de un sistema RAG depende más de la calidad del retrieval (¿se
recuperaron los chunks realmente relevantes?) que del LLM elegido — un LLM excelente no puede
responder bien con contexto irrelevante o incompleto ("garbage in, garbage out"). Mejorar
retrieval suele dar más beneficio por esfuerzo invertido que cambiar de modelo generador:
ajustar el tamaño de chunk, agregar metadata útil para filtrar, o combinar búsqueda vectorial
con búsqueda por palabras clave (retrieval híbrido) para casos donde la coincidencia léxica
exacta importa (nombres propios, códigos de error, términos técnicos exactos).

## Umbral de confianza y honestidad del sistema

Un RAG bien diseñado no fuerza siempre una respuesta: si la similitud de los mejores resultados
recuperados es baja, es preferible que el sistema indique explícitamente que no tiene
información suficiente (o recurra a una fuente alternativa, como búsqueda web) en vez de dejar
que el LLM "rellene" con conocimiento genérico o inventado que parece parte de la base de
conocimiento pero no lo es. Ese umbral (`min_similarity`) es una decisión de producto tanto
como técnica: bajarlo demasiado aumenta alucinaciones con contexto irrelevante; subirlo
demasiado hace que el sistema declare "no lo sé" con más frecuencia de la necesaria.
