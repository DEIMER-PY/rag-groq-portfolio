# Testing de frontend: Vitest y Testing Library

## Filosofía de Testing Library

React Testing Library (RTL) promueve probar componentes **como los usaría una persona real**:
en vez de acceder a instancias internas o estado privado del componente, se consultan elementos
por rol, texto visible o etiqueta accesible (`getByRole`, `getByText`, `getByLabelText`), y se
interactúa con ellos simulando eventos de usuario (`userEvent.click`, `userEvent.type`). Esto
hace que los tests sean resistentes a refactors internos (cambiar de `useState` a `useReducer`
no debería romper un test que solo verifica comportamiento visible) y que fallen cuando el
comportamiento real para el usuario cambia, que es justamente lo que se quiere detectar.

## Vitest como test runner

Vitest es un test runner compatible con la API de Jest pero integrado nativamente con Vite
(mismo transformador de módulos, mismo `vite.config`, arranque más rápido gracias a ESM nativo
y HMR en modo watch). Para testear componentes React se necesita el entorno `jsdom` (simula el
DOM en Node.js) configurado en `vitest.config.ts`:

```ts
export default defineConfig({
  test: {
    environment: "jsdom",
    setupFiles: "./src/setupTests.ts",
  },
});
```

## Estructura de un test de componente

Un test típico sigue el patrón Arrange-Act-Assert: renderizar el componente con las props
necesarias, simular la interacción del usuario, y verificar el resultado visible.

```tsx
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { ChatInput } from "./ChatInput";

test("deshabilita el envío al superar el límite de caracteres", async () => {
  const user = userEvent.setup();
  render(<ChatInput maxChars={10} onSend={() => {}} />);

  const textarea = screen.getByRole("textbox");
  await user.type(textarea, "esto tiene mas de diez caracteres");

  expect(screen.getByRole("button", { name: /enviar/i })).toBeDisabled();
});
```

## Qué mockear y qué no

Se recomienda **no** mockear el propio componente bajo prueba ni sus hijos directos (eso
prueba la implementación, no el comportamiento), pero sí mockear dependencias externas al
árbol de componentes: llamadas de red (`fetch`), temporizadores (`vi.useFakeTimers()`), o
módulos que acceden a APIs del navegador no soportadas por `jsdom`. Mockear demasiado profundo
("mock todo") produce tests que pasan aunque la integración real esté rota; mockear muy poco
hace los tests lentos y frágiles ante servicios externos.

## Cobertura como guía, no como objetivo

Un porcentaje alto de cobertura no garantiza ausencia de bugs: mide líneas ejecutadas, no
si las aserciones verifican el comportamiento correcto. Es más útil usar la cobertura para
encontrar código completamente no probado (ramas de error, casos límite) que para perseguir un
número arbitrario como 100%.
