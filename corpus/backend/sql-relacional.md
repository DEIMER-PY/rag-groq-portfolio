# Bases de datos relacionales (SQL)

## Normalización

Normalizar una base de datos relacional significa organizar las tablas para minimizar
redundancia y evitar anomalías de actualización. Las formas normales más usadas en la práctica:
**1FN** (valores atómicos, sin listas dentro de una celda), **2FN** (sin dependencias parciales
de una clave compuesta) y **3FN** (sin dependencias transitivas: una columna no clave no debe
depender de otra columna no clave). En sistemas con lecturas muy frecuentes y pocas escrituras,
a veces se **desnormaliza** deliberadamente (duplicar un dato) para evitar joins costosos —
siempre como decisión consciente y documentada, no por descuido en el diseño inicial.

## Índices

Un índice acelera búsquedas (`WHERE`, `JOIN`, `ORDER BY`) a costa de espacio en disco y de
ralentizar `INSERT`/`UPDATE`/`DELETE` (porque el índice también debe actualizarse). La regla
general: indexar columnas usadas frecuentemente en cláusulas `WHERE` o como claves foráneas en
joins, y evitar indexar columnas con baja cardinalidad (ej. una columna booleana) donde el
índice aporta poco. Un índice compuesto `(a, b)` sirve para consultas que filtran por `a` solo o
por `a` y `b` juntos, pero no para consultas que filtran solo por `b` — el orden de las columnas
en el índice importa.

## Transacciones y ACID

Una transacción agrupa varias operaciones para que se apliquen todas o ninguna (**Atomicidad**),
dejando la base de datos siempre en un estado válido (**Consistencia**), sin que transacciones
concurrentes se interfieran de forma incorrecta (**Aislamiento**) y con los cambios persistidos
de forma duradera tras confirmar (**Durabilidad**). El nivel de aislamiento
(`READ COMMITTED`, `REPEATABLE READ`, `SERIALIZABLE`) determina qué anomalías de concurrencia
son posibles (lecturas sucias, lecturas no repetibles, lecturas fantasma) — a mayor
aislamiento, mayor seguridad pero menor concurrencia efectiva.

## JOINs

- `INNER JOIN`: solo filas que tienen coincidencia en ambas tablas.
- `LEFT JOIN`: todas las filas de la tabla izquierda, con `NULL` en las columnas de la derecha
  si no hay coincidencia — útil para "traer todos los X, tengan o no un Y relacionado".
- `RIGHT JOIN`: análogo pero desde la tabla derecha (poco usado, se suele preferir reescribir
  como `LEFT JOIN` invirtiendo el orden de las tablas por legibilidad).
- `FULL OUTER JOIN`: unión de ambos casos, con `NULL` donde no hay coincidencia en cualquiera
  de los dos lados.

## `EXPLAIN` y optimización de consultas

`EXPLAIN ANALYZE` (Postgres/MySQL) muestra el plan de ejecución real de una consulta: si usa un
índice o hace un escaneo secuencial completo de la tabla, cuántas filas estima procesar, y
dónde se concentra el tiempo. Antes de optimizar a ciegas (agregar índices al azar, reescribir
consultas por intuición), `EXPLAIN ANALYZE` indica exactamente dónde está el costo real —
frecuentemente un escaneo secuencial en una tabla grande sin índice en la columna del `WHERE`.
