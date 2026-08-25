# CORS (Cross-Origin Resource Sharing)

## El problema que resuelve

Por defecto, el navegador aplica la **same-origin policy**: un script cargado desde
`https://app.midominio.com` no puede leer la respuesta de una petición a
`https://api.otrodominio.com` a menos que ese servidor lo permita explícitamente. CORS es el
mecanismo mediante el cual un servidor comunica, vía cabeceras HTTP, qué orígenes distintos
tienen permitido leer sus respuestas. Es importante entender que CORS es una protección del
**navegador para el usuario**, no una protección del servidor contra ataques — una petición
`curl` o de servidor a servidor ignora completamente CORS, porque no hay un navegador
aplicando la política.

## Peticiones simples vs preflight

Una petición "simple" (`GET`/`POST`/`HEAD` con content-types y headers estándar) se envía
directamente, y el navegador solo bloquea la **lectura** de la respuesta si falta la cabecera
`Access-Control-Allow-Origin` correspondiente. Una petición que usa métodos como `PUT`/`DELETE`,
headers personalizados (ej. `Authorization`), o `Content-Type: application/json` en algunos
casos, dispara primero una petición **preflight** (`OPTIONS`) donde el navegador pregunta al
servidor si esa combinación de método/headers está permitida antes de enviar la petición real.

## Cabeceras clave

- `Access-Control-Allow-Origin`: qué orígenes pueden leer la respuesta (`*` o un origen
  específico; nunca `*` si la petición incluye credenciales).
- `Access-Control-Allow-Credentials: true`: necesaria si la petición incluye cookies o
  cabeceras de autenticación (`credentials: "include"` en `fetch`); en este caso
  `Allow-Origin` **no puede** ser `*`, debe ser un origen explícito.
- `Access-Control-Allow-Methods` / `Access-Control-Allow-Headers`: qué métodos/headers están
  permitidos, respondidos en el preflight `OPTIONS`.

## Error común: "CORS error" que en realidad es otra cosa

Muchos errores reportados en consola como "bloqueado por CORS" en realidad son un servidor que
devolvió un error (500, timeout) **antes** de llegar a agregar las cabeceras CORS, o un
preflight que falla porque el servidor no maneja explícitamente `OPTIONS`. El mensaje de error
del navegador puede ser engañoso: revisar primero si la petición real llegó al servidor y qué
respondió, antes de asumir que el problema es la configuración de CORS en sí.

## Buenas prácticas

Configurar una lista explícita de orígenes permitidos por entorno (desarrollo, staging,
producción) en vez de `*`, especialmente si la API maneja datos autenticados. Frameworks como
Express (`cors()`) o FastAPI (`CORSMiddleware`) facilitan esta configuración declarativamente,
evitando manejar las cabeceras manualmente en cada respuesta.
