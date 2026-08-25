# React: componentes y estado

## Componentes y props

Un componente de React es una función que recibe `props` (datos de solo lectura pasados por el
padre) y retorna JSX describiendo la UI resultante. Los componentes deben ser puros respecto a
sus props: dado el mismo conjunto de props y estado, deben renderizar siempre el mismo
resultado, sin efectos secundarios durante el render (esos van en `useEffect`). Esta pureza es
lo que permite a React optimizar re-renders y, en el futuro, ejecutar renders concurrentes sin
romper la UI.

## `useState` y actualizaciones de estado

`useState` crea una porción de estado local al componente. Las actualizaciones son
**asíncronas y por lotes** (batched): React no vuelve a renderizar inmediatamente tras cada
`setState`, sino que agrupa varias actualizaciones dentro del mismo evento y las aplica juntas.
Cuando el nuevo estado depende del anterior, se debe usar la forma funcional para evitar leer
un valor obsoleto:

```jsx
// Incorrecto si se llama varias veces seguidas en el mismo ciclo
setCount(count + 1);

// Correcto: siempre parte del valor más reciente
setCount(prev => prev + 1);
```

## Levantar el estado (lifting state up)

Cuando dos componentes hermanos necesitan compartir o sincronizar estado, la solución idiomática
en React es mover ese estado al ancestro común más cercano y pasarlo hacia abajo vía props
(junto con las funciones para modificarlo). Esto evita duplicar fuentes de verdad. Cuando el
árbol de componentes que necesita el mismo estado es profundo, `useContext` evita el "prop
drilling" (pasar props a través de componentes intermedios que no las usan), pero no reemplaza
a `useState`: sigue siendo estado de React, solo que compartido vía contexto.

## Listas y `key`

Al renderizar listas con `.map()`, cada elemento necesita una prop `key` **estable y única**
entre renders (idealmente un ID del dato, nunca el índice del array si la lista puede
reordenarse, filtrarse o tener elementos insertados/eliminados). React usa `key` para decidir
qué instancias de componentes reutilizar entre renders; una `key` inestable (como el índice)
puede causar que el estado interno de un componente "se pegue" al elemento equivocado tras un
reordenamiento.

## Renderizado condicional y composición

React favorece la composición sobre la herencia: en vez de crear jerarquías de componentes que
extienden comportamiento, se combinan componentes pequeños vía `children` o props de tipo
función (render props) o simplemente componiendo JSX. El renderizado condicional se expresa con
operadores de JavaScript nativos (`&&`, ternarios, early returns) en vez de directivas
especiales, lo que mantiene el modelo mental de "JSX es solo JavaScript".
