# Principios SOLID

## S — Single Responsibility Principle

Una clase o módulo debe tener una sola razón para cambiar. Si una clase `UserService` maneja
tanto la validación de datos del usuario como el envío de emails de bienvenida como el guardado
en base de datos, un cambio en la lógica de envío de emails obliga a tocar (y potencialmente
romper) una clase que también contiene lógica de validación no relacionada. Separar estas
responsabilidades en `UserValidator`, `EmailNotifier` y `UserRepository` hace que cada cambio
tenga un radio de impacto acotado y predecible.

## O — Open/Closed Principle

El código debe estar abierto a extensión pero cerrado a modificación: se debe poder agregar
comportamiento nuevo sin editar código existente que ya funciona y está probado. Esto se logra
típicamente con polimorfismo: en vez de un `switch` gigante sobre un tipo que crece con cada
caso nuevo (`if tipo == "credito" ... else if tipo == "debito" ...`), se define una interfaz
común (`MetodoPago`) con una implementación por cada tipo, y agregar un método de pago nuevo
significa crear una clase nueva, no modificar un `switch` existente que ya maneja otros casos.

## L — Liskov Substitution Principle

Una subclase debe poder usarse en cualquier lugar donde se espera su clase base, sin romper el
comportamiento esperado por quien la usa. El ejemplo clásico: si `Cuadrado` hereda de
`Rectangulo` y sobrescribe `setAncho`/`setAlto` para mantener ambos lados iguales, romper el
contrato implícito de que cambiar el ancho de un rectángulo no afecta su alto — código que
funciona correctamente con cualquier `Rectangulo` puede fallar inesperadamente al recibir un
`Cuadrado`. La lección práctica: la herencia debe modelar una relación real de "es un", no
solo reutilización de código conveniente.

## I — Interface Segregation Principle

Es preferible tener varias interfaces pequeñas y específicas que una sola interfaz grande de
propósito general. Si una interfaz `Trabajador` obliga a implementar `trabajar()` y `comer()`,
una clase `Robot` que implementa esa interfaz se ve forzada a implementar `comer()` sin sentido
real. Separar en `Trabajable` y `Comestible` (o el nombre que corresponda) permite que cada
clase implemente solo lo que realmente le aplica, evitando métodos vacíos o que lanzan
excepciones "no implementado".

## D — Dependency Inversion Principle

Los módulos de alto nivel (reglas de negocio) no deben depender de módulos de bajo nivel
(detalles de implementación como una base de datos específica); ambos deben depender de
abstracciones. En la práctica, esto significa que una clase de lógica de negocio recibe una
interfaz (`RepositorioUsuarios`) inyectada, en vez de instanciar directamente
`PostgresUserRepository`. Esto permite cambiar la implementación concreta (o sustituirla por un
mock en tests) sin tocar la lógica de negocio, y es la base técnica que hace posible la
inyección de dependencias usada en frameworks como FastAPI (`Depends`) o Spring.
