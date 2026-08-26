# LLMs: familias de modelos y cómo elegir

## Dimensiones para comparar modelos

No existe "el mejor modelo" en abstracto; la elección depende de: **capacidad de razonamiento**
(tareas complejas de varios pasos), **velocidad/latencia**, **costo por token**, **ventana de
contexto** (cuánto texto puede procesar en una sola llamada), y **si el proveedor ofrece un
tier gratuito o de bajo costo** para prototipos y proyectos personales. Un error común es usar
el modelo más grande y costoso disponible para tareas simples (clasificación, extracción corta)
donde un modelo pequeño y rápido da resultados equivalentes a una fracción del costo y la
latencia.

## Familias de modelos relevantes (2026)

- **Familia Claude (Anthropic)**: Opus 5, Sonnet 5 y Haiku 4.5 cubren el rango de mayor
  capacidad de razonamiento (Opus), mejor balance costo/capacidad para uso general (Sonnet), y
  máxima velocidad/menor costo (Haiku). Sonnet 5 es frecuentemente el default recomendado para
  aplicaciones de agentes y desarrollo de software por su balance.
- **Modelos servidos por Groq**: Groq no entrena sus propios modelos, sino que sirve modelos
  open-weight de terceros sobre hardware propio (LPU) optimizado para inferencia de muy baja
  latencia; su catálogo cambia con el tiempo a medida que se lanzan nuevas familias (en distintos
  momentos ha incluido Llama de Meta, y actualmente incluye modelos como `openai/gpt-oss-120b`).
  Conviene siempre listar los modelos disponibles vía la API (`client.models.list()`) en vez de
  asumir un nombre fijo, porque los proveedores retiran modelos antiguos. Un detalle no obvio:
  los modelos de tipo "razonador" (reasoning), como la familia `gpt-oss`, consumen tokens de
  salida para su razonamiento interno **antes** de emitir la respuesta final — si el
  `max_tokens` es demasiado bajo, la respuesta llega vacía (`finish_reason="length"`) porque se
  truncó a mitad del razonamiento, no porque el modelo no supiera responder.
- **Modelos open-weight descargables**: Llama, Mistral, y variantes fine-tuneadas de la
  comunidad se pueden correr localmente (con suficiente GPU/CPU) o auto-hospedar, eliminando
  costo por token a cambio de gestionar la infraestructura de inferencia.

## Ventana de contexto y RAG

La ventana de contexto determina cuánta información (system prompt + contexto recuperado +
historial de conversación + pregunta) cabe en una sola llamada. Un RAG bien diseñado no depende
de ventanas de contexto gigantescas: en vez de meter todo el corpus en el prompt, la
recuperación selectiva (top-k chunks relevantes) mantiene el prompt compacto, más barato y con
menor riesgo de que el modelo "se pierda" entre información irrelevante — un fenómeno documentado
como degradación de atención con contextos muy largos ("lost in the middle").

## Temperatura y determinismo

El parámetro `temperature` controla cuánta aleatoriedad hay al elegir el siguiente token:
`temperature=0` favorece siempre el token más probable (respuestas más consistentes y
predecibles, deseable para tareas factuales como responder sobre una base de conocimiento),
mientras que valores más altos (`0.7`-`1.0`) aumentan la diversidad y creatividad, útiles para
generación de contenido creativo pero indeseables cuando se busca precisión factual y
respuestas reproducibles ante la misma pregunta.
