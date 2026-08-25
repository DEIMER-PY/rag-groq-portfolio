# Metodologías ágiles: Scrum y Kanban

## Qué tienen en común los enfoques ágiles

Tanto Scrum como Kanban nacen del mismo principio: entregar valor de forma incremental y
frecuente, con retroalimentación continua, en vez de planificar todo el proyecto por
adelantado y entregarlo completo al final (el enfoque "cascada"). La diferencia principal está
en **cómo** estructuran el flujo de trabajo: Scrum lo organiza en iteraciones de tiempo fijo
(sprints); Kanban lo organiza como un flujo continuo sin ciclos de tiempo fijos.

## Scrum: sprints, roles y ceremonias

Un sprint es un periodo fijo (normalmente 1-4 semanas) al final del cual el equipo entrega un
incremento potencialmente utilizable del producto. Los tres roles definidos son: **Product
Owner** (define y prioriza qué se construye, representando el valor de negocio), **Scrum
Master** (facilita el proceso y remueve impedimentos, no es un gestor jerárquico del equipo) y
el **equipo de desarrollo** (autoorganizado, decide cómo construir lo priorizado). Las
ceremonias estructuran la comunicación: **Sprint Planning** (qué se hará este sprint), **Daily
Standup** (sincronización diaria breve: qué se hizo, qué se hará, qué bloquea), **Sprint
Review** (demostrar el incremento a interesados) y **Retrospectiva** (el equipo reflexiona
sobre su propio proceso y ajusta).

## Kanban: flujo continuo y límites de trabajo en progreso

Kanban visualiza el trabajo en un tablero de columnas (ej. "Por hacer", "En progreso", "En
revisión", "Hecho") y limita explícitamente cuántos ítems pueden estar en cada columna a la vez
(**WIP limits** — Work In Progress). Este límite es la herramienta central de Kanban: fuerza al
equipo a terminar trabajo antes de empezar más, exponiendo cuellos de botella (si una columna
se llena constantemente hasta su límite, ahí está el problema real de flujo) en vez de
esconderlos bajo la ilusión de "todos están ocupados". A diferencia de Scrum, no hay
iteraciones de tiempo fijo: el trabajo fluye continuamente y se mide con métricas como el
**lead time** (tiempo desde que un ítem entra al tablero hasta que se completa).

## Cuándo conviene cada uno

Scrum funciona bien cuando el trabajo se puede planificar en bloques de alcance razonablemente
estable por unas semanas (desarrollo de producto con roadmap claro). Kanban se adapta mejor a
flujos de trabajo con alta variabilidad e interrupciones frecuentes (soporte, mantenimiento,
equipos de plataforma que atienden solicitudes entrantes impredecibles), donde forzar
iteraciones de tiempo fijo añade fricción sin beneficio real. Muchos equipos usan una
combinación práctica ("Scrumban"): sprints para planificación de mediano plazo, con un tablero
Kanban y límites de WIP para gestionar el flujo día a día dentro de cada sprint.

## User stories e historias bien escritas

Una user story describe una necesidad desde la perspectiva de quien la usa: "Como
[rol], quiero [acción], para [beneficio]". Su valor no está en el formato en sí sino en forzar
a pensar en el *para qué* antes de la implementación — una historia sin un beneficio claro
suele ser una señal de que el trabajo no está realmente priorizado por su valor, sino añadido
por inercia o suposición.
