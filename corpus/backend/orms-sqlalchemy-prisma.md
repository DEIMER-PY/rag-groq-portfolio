# ORMs: SQLAlchemy y Prisma

## Qué resuelve un ORM

Un ORM (Object-Relational Mapper) traduce entre filas de una tabla SQL y objetos/estructuras
del lenguaje de programación, evitando escribir SQL a mano para las operaciones CRUD más
comunes y dando tipado/autocompletado sobre el esquema de la base de datos. El costo es una
capa de abstracción que, mal usada, puede generar consultas ineficientes sin que sea obvio
leyendo el código de la aplicación — por eso entender el SQL que un ORM genera sigue siendo
necesario, no opcional.

## El problema N+1

El error de rendimiento más común en cualquier ORM: iterar sobre una lista de entidades y
acceder a una relación de cada una dentro del bucle dispara una consulta adicional por cada
elemento, en vez de una sola consulta con `JOIN`.

```python
# N+1: una consulta para los posts + una consulta POR CADA post para su autor
posts = session.query(Post).all()
for post in posts:
    print(post.author.name)  # dispara una query aquí, N veces

# Correcto: eager loading trae todo en una sola consulta (o dos, controladas)
posts = session.query(Post).options(joinedload(Post.author)).all()
```

En Prisma, el equivalente es usar `include`/`select` explícitamente en la consulta inicial en
vez de acceder a relaciones no cargadas después.

## Migraciones

Tanto SQLAlchemy (vía Alembic) como Prisma (vía `prisma migrate`) generan migraciones
versionadas que describen cambios incrementales al esquema (crear tabla, agregar columna,
modificar tipo). Las migraciones deben ser el único mecanismo para cambiar el esquema en
cualquier entorno más allá de local — nunca modificar la estructura de producción a mano —
porque permiten reproducir el estado exacto del esquema en cualquier entorno (desarrollo, CI,
staging, producción) aplicando la misma secuencia de pasos.

## Sesiones y transacciones en SQLAlchemy

Una `Session` de SQLAlchemy no es solo una conexión: mantiene una unidad de trabajo (identity
map) que rastrea los objetos cargados y sus cambios, y los persiste con `commit()` en una sola
transacción. Un patrón común y seguro es abrir una sesión por request (en FastAPI, vía
`Depends`), y cerrarla/hacer rollback automáticamente si la request termina con una excepción,
para no dejar conexiones o transacciones abiertas colgadas.

## Cuándo NO usar un ORM

Para reportes complejos con agregaciones pesadas, CTEs recursivos, o consultas que dependen
fuertemente de características específicas del motor de base de datos, escribir SQL crudo (con
el driver directo o herramientas como `sqlc`) suele ser más claro y controlable que forzar esa
lógica a través de la API del ORM. Un ORM es una herramienta para el 80-90% de las operaciones
CRUD estándar, no un mandato absoluto para el 100% del acceso a datos de una aplicación.
