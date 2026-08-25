# REST vs GraphQL

## Modelo de recursos vs modelo de grafo

REST expone datos como recursos identificados por URLs, con una forma de respuesta fija por
endpoint. GraphQL expone un único endpoint donde el cliente describe exactamente qué campos
necesita de un grafo de tipos, y el servidor responde solo con eso. Esto resuelve dos problemas
clásicos de REST: **over-fetching** (recibir más datos de los que la vista necesita, ej. un
endpoint `/users/:id` que siempre devuelve 20 campos aunque la UI solo muestre el nombre) y
**under-fetching** (necesitar varias peticiones encadenadas para armar una sola vista, ej.
`/posts/:id` y luego `/users/:authorId` para mostrar el nombre del autor).

## Cuándo conviene cada uno

REST es más simple de cachear (HTTP cache estándar funciona por URL), más fácil de razonar para
APIs con pocos consumidores o consumidores muy uniformes, y no requiere infraestructura
adicional. GraphQL brilla cuando hay múltiples clientes con necesidades de datos muy distintas
(app móvil vs web vs dashboard interno) sobre el mismo backend, o cuando el frontend cambia con
frecuencia y no se quiere coordinar un nuevo endpoint REST por cada variación de vista. El costo
de GraphQL es mayor complejidad en el servidor (resolvers, N+1 de forma menos visible, control
de profundidad de queries para evitar abuso) y cacheo HTTP menos directo (todo pasa por POST a
un solo endpoint).

## El problema N+1 en GraphQL

Al resolver un campo que trae una lista de entidades relacionadas (ej. `posts { author { name } }`
para 50 posts), un resolver ingenuo dispara una consulta por cada `author`, igual que el N+1 de
un ORM. La solución estándar es **DataLoader**: agrupa (batch) todas las solicitudes de un
mismo tipo dentro del mismo tick del event loop y las resuelve en una sola consulta con
`WHERE id IN (...)`, además de cachear resultados dentro de la misma request.

## Versionado

REST suele versionarse con un prefijo en la URL (`/api/v2/...`) cuando el contrato cambia de
forma incompatible. GraphQL evita el versionado explícito: los campos se pueden deprecar
(`@deprecated`) y agregar sin romper a los clientes existentes, porque cada cliente pide
explícitamente los campos que usa — un campo nuevo no afecta a queries que no lo solicitan.
