# Autenticación: JWT y OAuth2

## Qué es un JWT

Un JSON Web Token es una cadena con tres partes codificadas en Base64URL separadas por puntos:
header (algoritmo de firma), payload (claims — datos del usuario, expiración) y firma
(criptográfica, calculada con una clave secreta o un par de claves). El servidor puede verificar
que un JWT no fue alterado revisando la firma, sin necesidad de consultar una base de datos ni
mantener estado de sesión en el servidor — de ahí que se lo describa como "stateless". Esto es
una ventaja para escalar horizontalmente (cualquier instancia del backend puede validar el
token sin compartir estado), pero también su principal limitación: **un JWT no puede
invalidarse antes de su expiración** sin infraestructura adicional (una lista negra), porque el
servidor no "recuerda" haberlo emitido.

## Access token vs refresh token

El patrón estándar usa dos tokens: un **access token** de vida corta (minutos) que se envía en
cada petición (`Authorization: Bearer <token>`) y un **refresh token** de vida larga, almacenado
de forma más protegida (idealmente en una cookie `httpOnly`, no en `localStorage`, para
mitigar robo vía XSS), usado solo para pedir un nuevo access token cuando el actual expira. Esto
limita la ventana de exposición si un access token se filtra, sin forzar al usuario a
reautenticarse cada pocos minutos.

## OAuth2 y OpenID Connect

OAuth2 es un protocolo de **autorización** (delegar acceso a un recurso a una aplicación de
terceros, ej. "permitir que esta app lea mis repos de GitHub"), no de autenticación en sí mismo.
OpenID Connect (OIDC) se construye sobre OAuth2 para agregar una capa estándar de
**autenticación** (identificar quién es el usuario) mediante un `id_token` en formato JWT. El
flujo más común y seguro para aplicaciones web es **Authorization Code con PKCE**: la app
redirige al usuario al proveedor de identidad, recibe un código de un solo uso, y lo intercambia
por tokens desde el backend (nunca exponiendo el `client_secret` en el navegador); PKCE agrega
una verificación adicional que protege ese intercambio incluso en apps que no pueden guardar un
secreto de forma segura (SPAs, apps móviles).

## Dónde almacenar tokens en el cliente

`localStorage` es accesible por cualquier script que corra en la página, así que un ataque XSS
puede robar el token directamente. Una cookie `httpOnly` no es legible por JavaScript, lo que
mitiga XSS, pero introduce el riesgo de CSRF (un sitio malicioso puede hacer que el navegador
envíe esa cookie automáticamente) — mitigado con el atributo `SameSite=Strict/Lax` y tokens
anti-CSRF en operaciones que modifican estado. No existe una opción sin trade-offs; la elección
depende de qué vector de ataque es más relevante para la aplicación concreta.

## Hashing de contraseñas

Las contraseñas nunca se almacenan en texto plano ni con hashes rápidos de propósito general
(MD5, SHA-256 solos) porque son vulnerables a ataques de fuerza bruta con hardware moderno. Se
usan funciones diseñadas para ser lentas y costosas en cómputo/memoria (bcrypt, scrypt, Argon2),
con un "salt" único por contraseña para que dos usuarios con la misma contraseña no produzcan el
mismo hash, y un factor de costo configurable que se aumenta con el tiempo a medida que el
hardware se vuelve más rápido.
