# Frameworks de orquestación: LangChain y LlamaIndex

## Qué problema resuelven

LangChain y LlamaIndex son frameworks que estandarizan piezas comunes de aplicaciones con LLMs:
carga de documentos desde múltiples formatos, chunking, integración con decenas de proveedores
de embeddings y vector stores intercambiables, plantillas de prompts, y "chains"/"pipelines"
que encadenan estos pasos. Su valor principal es reducir el código repetitivo de "plomería"
(boilerplate de conectar cada proveedor con su SDK propio) y dar abstracciones ya probadas para
patrones comunes (RAG, agentes, resúmenes de documentos largos).

## LangChain: orientado a cadenas y agentes

LangChain modela un pipeline como una cadena de componentes componibles (`Runnable`), con
soporte extenso para agentes (LLMs que deciden qué herramientas invocar en un ciclo de
razonamiento-acción) y una enorme cantidad de integraciones con proveedores de LLMs, vector
stores y fuentes de datos. Su curva de aprendizaje es más pronunciada por la cantidad de
abstracciones y ha tenido varios cambios de API entre versiones mayores, lo que a veces hace
que ejemplos encontrados en internet queden desactualizados.

## LlamaIndex: orientado a indexación de datos

LlamaIndex nació con foco específico en la fase de "conectar tus datos a un LLM": tiene
abstracciones más maduras para distintos tipos de índices (no solo vectorial: índices de
lista, de árbol, de grafo de conocimiento) y estrategias de recuperación más sofisticadas
listas para usar (recuperación jerárquica, re-ranking, fusión de múltiples estrategias de
búsqueda). Para un caso de uso puramente de "preguntas y respuestas sobre documentos", suele
requerir menos código que armar el equivalente en LangChain.

## Cuándo NO usar un framework y escribir el pipeline a mano

Para un pipeline RAG simple (un solo tipo de fuente, un solo vector store, un flujo lineal
embed→retrieve→prompt→generar), escribir el código directamente sobre los SDKs oficiales
(cliente de Supabase, cliente de Groq, `sentence-transformers`) da control total sobre cada
paso, es más fácil de debuguear (no hay que entender las abstracciones internas del framework
para saber qué prompt exacto se envió), y evita una dependencia pesada para un problema que en
esencia son unas pocas funciones bien definidas. La recomendación práctica: adoptar un
framework cuando el proyecto realmente necesita muchas integraciones intercambiables o patrones
avanzados (agentes con herramientas, múltiples fuentes heterogéneas); para un RAG con un
dominio y un flujo bien delimitado, código propio suele ser más mantenible y transparente.

## Interoperabilidad

Ambos frameworks no son mutuamente excluyentes con un enfoque manual: es común usar solo la
pieza específica que aporta valor (por ejemplo, un text splitter de LangChain) sin adoptar todo
el framework de orquestación, evitando el costo de aprendizaje completo por una sola utilidad.
