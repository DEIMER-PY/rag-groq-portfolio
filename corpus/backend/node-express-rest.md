# Node.js, Express y APIs REST

## El modelo de I/O no bloqueante de Node.js

Node.js ejecuta JavaScript en un solo hilo, pero delega operaciones de I/O (lectura de disco,
red, bases de datos) a libuv, que las procesa en un thread pool o de forma asíncrona a nivel de
sistema operativo, y notifica a Node mediante el event loop cuando terminan. Esto permite que un
servidor Node.js maneje miles de conexiones concurrentes sin crear un hilo por conexión, siempre
que el código de la aplicación no bloquee el hilo principal con cómputo intensivo síncrono (por
ejemplo, un `JSON.parse` de un archivo enorme o un bucle CPU-bound) — ese tipo de trabajo debe
delegarse a un `worker_thread` o a un proceso separado.

## Middleware en Express

Express estructura una API como una cadena de funciones middleware `(req, res, next) => {}` que
se ejecutan en orden para cada request. Cada middleware puede modificar `req`/`res`, terminar la
respuesta, o llamar a `next()` para pasar el control al siguiente. Este patrón permite componer
responsabilidades transversales (logging, autenticación, parseo de body, manejo de errores) sin
acoplarlas a la lógica de cada ruta:

```js
app.use(express.json());              // parseo de body
app.use(requestLogger);               // logging
app.use("/api/users", authMiddleware, usersRouter); // auth solo para este router
app.use(errorHandler);                // debe ir al final, con 4 parámetros (err, req, res, next)
```

## Diseño de una API REST

Una API REST bien diseñada usa los sustantivos (recursos) en la URL y los verbos HTTP para la
acción: `GET /users` (listar), `GET /users/:id` (obtener uno), `POST /users` (crear),
`PUT/PATCH /users/:id` (actualizar completo/parcial), `DELETE /users/:id` (eliminar). Los
códigos de estado HTTP deben ser semánticamente correctos: `200` éxito con cuerpo, `201`
recurso creado, `204` éxito sin cuerpo, `400` error de validación del cliente, `401` no
autenticado, `403` autenticado pero sin permiso, `404` recurso inexistente, `409` conflicto
(ej. duplicado), `500` error no controlado del servidor. Devolver siempre `200` con un campo
`success: false` en el body (anti-patrón común) rompe el contrato HTTP y complica el manejo de
errores en el cliente.

## Manejo de errores centralizado

En vez de repetir `try/catch` con `res.status(...).json(...)` en cada handler, se centraliza el
manejo de errores en un middleware de error de Express (el que recibe 4 argumentos), y cada
ruta simplemente lanza o pasa el error con `next(err)`. Con rutas `async`, se necesita envolver
el handler (o usar un wrapper como `express-async-errors`) para que los rechazos de promesas
lleguen al middleware de error en vez de quedar como `UnhandledPromiseRejection`.

## Versionado y CORS

Versionar la API (`/api/v1/...`) desde el inicio evita romper clientes existentes cuando el
contrato cambia. CORS (Cross-Origin Resource Sharing) es una cabecera de respuesta que el
navegador exige antes de permitir que JavaScript de un origen distinto lea la respuesta; se
configura en el servidor (`cors()` en Express) especificando orígenes permitidos explícitos en
producción — usar `origin: "*"` es aceptable solo para APIs públicas de solo lectura sin
credenciales.
