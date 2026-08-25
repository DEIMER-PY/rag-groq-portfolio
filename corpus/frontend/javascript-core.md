# JavaScript: conceptos fundamentales

## Event loop y asincronía

JavaScript es de un solo hilo, pero maneja operaciones asíncronas (timers, I/O, peticiones de
red) mediante el **event loop**. El call stack ejecuta código síncrono; cuando encuentra una
operación asíncrona, la delega al entorno (navegador o Node.js) y sigue ejecutando el resto del
código síncrono. Al completarse, el callback se encola: los callbacks de Promesas van a la
**microtask queue** (mayor prioridad) y los de `setTimeout`/eventos van a la **macrotask
queue**. El event loop solo procesa una macrotarea después de vaciar completamente la cola de
microtareas. Esto explica por qué `Promise.resolve().then(fn)` siempre se ejecuta antes que
`setTimeout(fn, 0)`, aunque ambos se programen en el mismo instante.

## Promesas vs async/await

`async/await` es azúcar sintáctica sobre Promesas: una función `async` siempre retorna una
Promesa, y `await` pausa la ejecución de esa función (no del hilo completo) hasta que la
Promesa se resuelva. El manejo de errores se hace con `try/catch` en vez de `.catch()`, lo que
suele ser más legible en cadenas largas de operaciones dependientes. Un error común es olvidar
`await` en un bucle cuando se necesita ejecutar operaciones en paralelo: `Promise.all(items.map(fn))`
ejecuta todas las promesas concurrentemente, mientras que un `for...of` con `await` dentro las
ejecuta secuencialmente — la elección correcta depende de si las operaciones son independientes
entre sí o no.

## Closures

Un closure ocurre cuando una función "recuerda" el entorno léxico en el que fue creada, incluso
después de que ese entorno haya terminado de ejecutarse. Es la base de patrones como
factories de funciones, memoización, y encapsulamiento de estado privado antes de que
existieran clases con campos privados:

```js
function crearContador() {
  let cuenta = 0;
  return () => ++cuenta;
}
const contar = crearContador();
contar(); // 1
contar(); // 2 — "cuenta" persiste entre llamadas
```

## `this` y su comportamiento contextual

El valor de `this` en JavaScript depende de **cómo** se llama una función, no de dónde se
define (excepto en arrow functions). En un método de objeto (`obj.metodo()`), `this` es el
objeto. En una función normal invocada suelta, `this` es `undefined` en modo estricto. Las
**arrow functions** no tienen su propio `this`: lo heredan léxicamente del contexto donde se
definieron, lo que las hace ideales para callbacks dentro de métodos (evitan el clásico bug de
perder el `this` dentro de un `setTimeout` o un `.map()`).

## Tipado dinámico y coerción

JavaScript convierte tipos implícitamente en comparaciones con `==` y en operadores
aritméticos con operandos mixtos, lo que produce resultados sorprendentes (`"5" + 3` es
`"53"`, `"5" - 3` es `2`). La práctica recomendada es usar siempre `===`/`!==` para evitar la
coerción implícita en comparaciones, y ser explícito en las conversiones (`Number(x)`,
`String(x)`, `Boolean(x)`) en vez de depender de la coerción automática del lenguaje.
