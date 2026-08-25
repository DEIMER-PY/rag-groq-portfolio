# Clean Code

## Nombrar bien es la mitad del trabajo

Un nombre de variable, función o clase debe comunicar su propósito sin necesitar un comentario
adicional. `d` no dice nada; `elapsedDaysSinceLastLogin` sí. Las funciones deben nombrarse como
verbos que describan exactamente lo que hacen (`calculateTotal`, no `process` o `handle`, que no
comunican intención real). Si nombrar algo correctamente resulta difícil, frecuentemente es una
señal de que esa función o clase está haciendo más de una cosa y debería dividirse.

## Funciones pequeñas y de un solo nivel de abstracción

Una función debe hacer una sola cosa, y hacerla bien. Cuando una función mezcla detalles de bajo
nivel (parseo de strings, manejo de errores de red) con lógica de alto nivel (reglas de
negocio), se vuelve difícil de leer porque el lector tiene que cambiar constantemente de
"nivel mental". Extraer las partes de bajo nivel a funciones auxiliares bien nombradas permite
que la función principal se lea casi como una lista de pasos en lenguaje natural.

## Comentarios: el código debe explicarse solo

Un comentario que describe *qué* hace el código (`// incrementa el contador`) generalmente es
una señal de que el código no es lo suficientemente claro por sí mismo y debería reescribirse
con mejores nombres, no comentarse. Un comentario tiene valor cuando explica el **por qué** de
una decisión no obvia (una restricción externa, un workaround para un bug conocido de una
librería, una razón histórica) que el código en sí no puede comunicar. Los comentarios
desactualizados son peores que la ausencia de comentarios, porque mienten con autoridad.

## DRY (Don't Repeat Yourself) sin abstraer de más

Duplicar lógica de negocio (la misma regla de validación escrita en dos lugares) es un riesgo
real: un cambio futuro puede actualizarse en un lugar y olvidarse en el otro. Pero no toda
similitud superficial de código justifica una abstracción compartida — dos funciones que se
parecen hoy pero representan conceptos de negocio distintos pueden divergir con el tiempo, y
forzarlas a compartir una abstracción prematura las acopla artificialmente. La regla práctica:
abstraer cuando la duplicación representa la **misma** regla o concepto, no solo texto
parecido.

## Manejo de errores explícito

Los errores deben manejarse en el nivel donde hay contexto suficiente para decidir qué hacer
(reintentar, mostrar un mensaje al usuario, propagar), no silenciarse con un `catch` vacío que
oculta fallos reales. Las excepciones deben usarse para condiciones verdaderamente
excepcionales, no como mecanismo de control de flujo normal (por ejemplo, usar una excepción
para "el usuario no fue encontrado" en un flujo donde eso es un caso esperado y común es
preferible modelarlo como un valor de retorno explícito, ej. `Optional`/`None`).
