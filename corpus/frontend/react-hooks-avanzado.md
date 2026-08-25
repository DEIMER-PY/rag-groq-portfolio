# React: hooks avanzados

## `useEffect` y sincronización con sistemas externos

`useEffect` sirve para sincronizar un componente con algo fuera del modelo de React:
suscripciones, temporizadores, peticiones de red, manipulación directa del DOM. No es un hook
de "ciclo de vida" en el sentido de clases; es más útil pensarlo como "después de este render,
sincroniza con X". El array de dependencias determina cuándo se vuelve a ejecutar el efecto: si
se omite, corre en cada render; si es `[]`, corre solo al montar; si tiene valores, corre cuando
alguno de esos valores cambia entre renders (comparación por referencia, no por valor profundo).
La función de limpieza (return dentro del efecto) se ejecuta antes de la siguiente ejecución del
efecto y al desmontar el componente — es obligatoria para suscripciones y timers, para evitar
fugas de memoria o efectos duplicados.

## `useMemo` y `useCallback`

Ambos son optimizaciones, no herramientas de corrección: memorizan un valor (`useMemo`) o una
función (`useCallback`) entre renders mientras sus dependencias no cambien. Se justifican en dos
casos concretos: (1) un cálculo costoso que no debe repetirse en cada render, o (2) evitar que
un componente hijo memorizado con `React.memo` se re-renderice innecesariamente porque recibió
una nueva referencia de función/objeto aunque el valor "lógico" sea el mismo. Usarlos en todas
partes "por si acaso" añade complejidad y overhead de comparación sin beneficio real — la
recomendación es medir primero (con el Profiler de React) y memorizar donde el perfil muestre
un problema real.

## Custom hooks

Un custom hook es simplemente una función que empieza con `use` y puede llamar a otros hooks
dentro. Su valor está en extraer lógica con estado que se repite entre componentes (por ejemplo,
`useFetch`, `useDebounce`, `useLocalStorage`) sin duplicar código ni forzar una jerarquía de
componentes artificial solo para compartir comportamiento. A diferencia de una función utilitaria
normal, un custom hook mantiene su propio estado y efectos aislados por cada componente que lo
usa — dos componentes que llaman al mismo custom hook no comparten estado entre sí a menos que
ese estado viva en un contexto compartido.

## Reglas de los hooks

Los hooks deben llamarse siempre en el mismo orden en cada render: no dentro de condicionales,
bucles o funciones anidadas. React identifica cada hook por su posición en la secuencia de
llamadas de un componente, no por nombre; romper el orden (por ejemplo, un `useState`
condicional) desincroniza esa lista interna y produce bugs difíciles de rastrear. Si se necesita
lógica condicional, la condición va **dentro** del hook (por ejemplo, dentro del cuerpo de
`useEffect`), no alrededor de la llamada al hook.

## `useReducer` para estado complejo

Cuando el estado de un componente tiene múltiples sub-valores que cambian juntos, o las
transiciones de estado siguen una lógica de tipo "acción → nuevo estado" (como un formulario
con muchos campos o un flujo con varios pasos), `useReducer` centraliza esa lógica en una
función pura `(estado, accion) => nuevoEstado`, similar al patrón usado por Redux. Esto hace
más fácil testear las transiciones de estado de forma aislada, sin necesidad de renderizar
componentes.
