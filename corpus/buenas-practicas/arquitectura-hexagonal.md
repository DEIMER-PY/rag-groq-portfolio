# Arquitectura hexagonal (Ports & Adapters)

## La idea central

La arquitectura hexagonal (propuesta por Alistair Cockburn) organiza una aplicación en un
núcleo de lógica de negocio (dominio) completamente aislado de detalles externos —
frameworks web, bases de datos, colas de mensajes, APIs de terceros. El dominio define
**puertos** (interfaces que describen qué necesita o qué expone, en términos del propio
dominio, no de tecnología concreta), y los detalles externos se conectan a esos puertos
mediante **adaptadores** (implementaciones concretas: un adaptador de FastAPI para exponer el
dominio vía HTTP, un adaptador de PostgreSQL para persistir, un adaptador de Groq para generar
texto). La dependencia siempre apunta hacia adentro: el dominio no sabe nada de FastAPI ni de
PostgreSQL, pero los adaptadores sí conocen al dominio.

## Por qué importa esta dirección de dependencia

Si la lógica de negocio depende directamente de un framework o una librería de base de datos
específica, cambiar esa tecnología (o simplemente probar la lógica sin levantar una base de
datos real) se vuelve costoso. Con el dominio aislado detrás de puertos, se puede: (1) testear
la lógica de negocio con implementaciones de prueba de los puertos (in-memory, sin red ni
base de datos real), y (2) cambiar de PostgreSQL a otra base de datos, o de Groq a otro
proveedor de LLM, implementando un adaptador nuevo sin tocar una sola línea del dominio.

## Ejemplo aplicado a un sistema RAG

En un pipeline RAG, el dominio podría definir un puerto `BuscadorDeContexto` (con un método
`buscar(pregunta) -> list[Fragmento]`) y un puerto `GeneradorDeRespuestas`
(`generar(prompt) -> str`), sin mencionar Supabase ni Groq en ninguna parte del dominio. Los
adaptadores concretos (`SupabaseBuscadorDeContexto`, `GroqGeneradorDeRespuestas`) implementan
esos puertos usando sus SDKs específicos. Esto permite, por ejemplo, testear la lógica de
orquestación del RAG (¿se dispara el fallback web cuando corresponde? ¿se rechaza una pregunta
fuera de alcance?) con implementaciones falsas de ambos puertos, sin llamar realmente a
Supabase ni a Groq en cada test.

## Cuándo vale la pena esta complejidad adicional

La arquitectura hexagonal introduce indirección (interfaces, inyección de dependencias) que no
siempre se justifica en un proyecto pequeño de corta vida o un prototipo. Su valor crece con el
tamaño del proyecto, la cantidad de integraciones externas que probablemente cambiarán, y la
necesidad de tests rápidos y aislados de la lógica de negocio. Aplicarla dogmáticamente a un
script simple de un solo archivo añade ceremonia sin beneficio real — como toda decisión de
arquitectura, es un trade-off que debe evaluarse contra la complejidad real del problema.
