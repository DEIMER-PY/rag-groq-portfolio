# Agentes de código

## Qué distingue a un agente de un simple chat con un LLM

Un chat tradicional con un LLM es un ciclo pregunta-respuesta sin acceso al mundo exterior más
allá del texto de la conversación. Un **agente** añade un ciclo de razonamiento-acción: el
modelo puede decidir invocar herramientas (leer un archivo, ejecutar un comando, hacer una
petición HTTP, llamar a un servidor MCP), observar el resultado, y decidir el siguiente paso —
repitiendo este ciclo hasta completar una tarea de varios pasos, en vez de responder todo en un
solo turno de texto. Los agentes de código (como Claude Code, Cursor, GitHub Copilot Workspace)
aplican este patrón específicamente a tareas de desarrollo de software: explorar un repositorio,
editar archivos, correr tests, interpretar errores y corregir el código en base a ellos.

## El ciclo ReAct (Reason + Act)

Un patrón común detrás de los agentes es alternar explícitamente entre "razonar" (el modelo
genera un pensamiento sobre qué hacer a continuación) y "actuar" (invocar una herramienta),
incorporando el resultado de la acción de vuelta al contexto antes del siguiente paso de
razonamiento. Esto permite que el agente corrija el rumbo con información nueva (por ejemplo,
un test que falla revela que la primera solución propuesta era incorrecta) en vez de comprometerse
a un plan fijo generado sin retroalimentación del entorno real.

## Planificación vs ejecución directa

Para tareas complejas o con alto costo de reversión (cambios estructurales grandes, decisiones
de arquitectura), separar una fase explícita de **planificación** (explorar el código,
diseñar el enfoque, y presentarlo para revisión humana) de la fase de **ejecución** reduce el
riesgo de que el agente tome un camino equivocado sin que el humano tenga oportunidad de
corregirlo a tiempo. Para tareas pequeñas y de bajo riesgo (un fix acotado, agregar un test),
ese overhead de planificación explícita suele no justificarse frente a simplemente ejecutar
directamente.

## Contexto y memoria de un agente

A diferencia de un humano, un agente no retiene memoria entre sesiones a menos que se le dé
explícitamente un mecanismo para ello: archivos de memoria persistente, un resumen guardado de
decisiones previas, o documentación del propio proyecto (`AGENTS.md`, `README.md`) que el
agente lee al iniciar. Diseñar bien esa "memoria externa" —qué convenciones documentar, qué
decisiones registrar y por qué— es tan importante para la efectividad de un agente de código
como el modelo subyacente que lo impulsa.

## Riesgos y límites de autonomía

Dar a un agente la capacidad de ejecutar acciones reales (comandos de shell, llamadas a APIs
externas, cambios en producción) introduce riesgo si actúa sobre instrucciones incorrectas o
maliciosas incrustadas en contenido que procesa (por ejemplo, un comentario en un issue de
GitHub que intenta manipular al agente). Por eso los agentes de código bien diseñados distinguen
entre acciones reversibles/locales (que pueden ejecutarse con más autonomía) y acciones
irreversibles o de alto impacto (push a producción, borrado de datos, envío de mensajes en
nombre del usuario), reservando estas últimas para confirmación explícita humana.
