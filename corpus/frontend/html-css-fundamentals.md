# HTML y CSS: fundamentos

## Semántica en HTML5

HTML5 introdujo etiquetas semánticas (`<header>`, `<nav>`, `<main>`, `<section>`, `<article>`,
`<aside>`, `<footer>`) que describen el propósito de un bloque de contenido en lugar de solo su
apariencia. Usar semántica correcta mejora tres cosas al mismo tiempo: accesibilidad (los
lectores de pantalla anuncian regiones con sentido), SEO (los buscadores entienden mejor la
estructura de la página) y mantenibilidad (un `<div class="header">` no comunica intención,
un `<header>` sí). Una regla práctica: si una etiqueta semántica existe para el propósito que
necesitas, úsala antes que un `<div>` genérico.

## El modelo de caja (box model)

Todo elemento en CSS se renderiza como una caja rectangular compuesta por `content`,
`padding`, `border` y `margin`, de adentro hacia afuera. Por defecto (`box-sizing: content-box`),
`width`/`height` solo miden el contenido, y el padding/border se suman por fuera, lo que hace
difícil predecir el tamaño final de un elemento. La práctica moderna es forzar
`box-sizing: border-box` globalmente:

```css
*, *::before, *::after {
  box-sizing: border-box;
}
```

Con `border-box`, `width`/`height` incluyen padding y border, así que el tamaño declarado es el
tamaño real ocupado en pantalla.

## Flexbox vs CSS Grid

- **Flexbox** es unidimensional: distribuye elementos en una fila o columna, ideal para barras
  de navegación, alineación de elementos dentro de un contenedor, o distribuir espacio entre
  tarjetas de tamaño variable.
- **CSS Grid** es bidimensional: define filas y columnas simultáneamente, ideal para el layout
  general de una página (header/sidebar/main/footer) o para galerías con posiciones explícitas.

Regla práctica: si estás alineando elementos en una sola dirección, usa Flexbox; si estás
definiendo la estructura completa de una página o un componente con filas y columnas, usa Grid.
Ambos se combinan sin problema (un Grid puede contener elementos que internamente usan Flexbox).

## Especificidad y cascada

Cuando varias reglas CSS aplican al mismo elemento, gana la de mayor especificidad, calculada
como una tupla `(inline, IDs, clases/atributos/pseudo-clases, elementos)`. Un ID (`#nav`) le
gana a cualquier cantidad de clases; una clase le gana a cualquier cantidad de selectores de
elemento. `!important` rompe este orden y debe evitarse salvo para sobrescribir estilos de
librerías de terceros que no se pueden modificar. Para mantener la especificidad baja y
predecible, se recomienda estilizar principalmente por clases (metodologías como BEM ayudan a
esto) y reservar los IDs para JavaScript/anclas, no para CSS.

## Diseño responsive

Mobile-first significa escribir los estilos base para pantallas pequeñas y usar `min-width`
media queries para agregar complejidad en pantallas más grandes, en vez de partir de desktop y
usar `max-width` para "achicar". Esto produce hojas de estilo más simples porque el caso base
(móvil) suele requerir menos reglas. Unidades relativas (`rem`, `%`, `vw/vh`, `clamp()`) en
lugar de `px` fijos permiten que el layout se adapte al tamaño de fuente del usuario y al
viewport sin necesidad de docenas de breakpoints.
