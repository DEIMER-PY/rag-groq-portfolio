# MCP (Model Context Protocol)

## Qué problema resuelve MCP

Antes de MCP, cada aplicación que quería dar a un LLM acceso a herramientas externas (leer
archivos, consultar una base de datos, llamar a una API de terceros) tenía que implementar esa
integración de forma específica para ese LLM y ese cliente. MCP es un protocolo abierto,
propuesto por Anthropic, que estandariza cómo un modelo (a través de un cliente, como Claude
Code o Claude Desktop) descubre y usa herramientas expuestas por **servidores MCP**
independientes del modelo. Un servidor MCP para, por ejemplo, Supabase o GitHub, se implementa
una sola vez y funciona con cualquier cliente compatible con el protocolo, en vez de
reimplementarse por cada aplicación de IA que quiera esa integración.

## Componentes del protocolo

- **Servidor MCP**: expone un conjunto de **tools** (funciones invocables, con nombre,
  descripción y esquema de parámetros que el modelo puede leer para saber cómo llamarlas),
  opcionalmente **resources** (datos de solo lectura que el cliente puede adjuntar como
  contexto) y **prompts** (plantillas reutilizables).
- **Cliente MCP**: la aplicación que aloja al modelo (ej. Claude Code) y actúa como
  intermediario entre el modelo y uno o más servidores MCP, presentando las tools disponibles al
  modelo y ejecutando las llamadas que el modelo decide hacer.
- **Transporte**: la comunicación entre cliente y servidor ocurre vía stdio (proceso local) o
  HTTP/SSE (servidor remoto), independiente de la lógica de negocio del servidor.

## MCP vs "function calling" tradicional

El function calling de un LLM (definir funciones en el payload de la API y dejar que el modelo
elija cuál invocar) es el mecanismo de bajo nivel que hace posible que un modelo "use
herramientas". MCP se construye sobre ese mecanismo pero estandariza el **descubrimiento y
empaquetado** de esas herramientas como servidores reutilizables e independientes de la
aplicación que los consume — la diferencia es similar a la que hay entre "una función que
escribes para tu proyecto" y "una librería publicada que cualquier proyecto puede instalar".

## Relación con RAG y agentes

Un servidor MCP puede exponer exactamente el tipo de capacidades que un sistema RAG o un agente
necesita: una tool de búsqueda semántica sobre una base vectorial, una tool que ejecute SQL de
solo lectura, una tool que dispare un despliegue. Esto permite construir agentes que combinan
recuperación de conocimiento (RAG) con acciones concretas sobre sistemas reales (crear un
ticket, desplegar un servicio), todo dentro del mismo protocolo estandarizado de herramientas,
en vez de que cada capacidad requiera su propia integración ad-hoc.

## Skills como complemento a MCP

Mientras que un servidor MCP expone *capacidades ejecutables* (tools), una "skill" es un
paquete de instrucciones y contexto (documentación, convenciones, pasos a seguir) que guía
*cómo* un agente debe abordar un tipo de tarea recurrente, sin necesariamente ejecutar código
por sí misma. Un mismo proyecto puede combinar ambos: MCP para dar acceso real a sistemas
externos (Supabase, GitHub, Render), y skills/`AGENTS.md` para documentar las convenciones y el
criterio con el que un agente debe usar esas capacidades dentro de ese proyecto específico.
