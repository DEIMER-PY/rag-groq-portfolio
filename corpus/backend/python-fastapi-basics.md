# Python y FastAPI

## Por qué FastAPI

FastAPI combina tipado con type hints de Python, validación automática de datos (vía
Pydantic) y generación automática de documentación OpenAPI/Swagger a partir del mismo código,
sin necesidad de mantener especificaciones separadas. Al declarar el tipo de un parámetro o del
cuerpo de una petición, FastAPI valida la entrada, convierte tipos automáticamente (ej. un
query param `"5"` a `int`), y devuelve un `422 Unprocessable Entity` con detalle del error si la
validación falla, sin escribir ese código de validación manualmente.

## Modelos con Pydantic

Un `BaseModel` de Pydantic define la forma esperada de los datos y sus reglas de validación:

```python
from pydantic import BaseModel, Field

class QueryRequest(BaseModel):
    query: str = Field(..., max_length=500, min_length=1)
    history: list[dict] | None = None

class QueryResponse(BaseModel):
    answer: str
    sources: list[dict]
    used_web_fallback: bool
```

Usar estos modelos como firma de los endpoints (`async def query(body: QueryRequest)`) separa
claramente el contrato de la API de la lógica interna, y ese mismo modelo se reutiliza para
serializar la respuesta, evitando dos fuentes de verdad sobre la forma de los datos.

## Async/await en FastAPI

Un endpoint `async def` se ejecuta en el event loop de `asyncio` sin bloquear otras peticiones
mientras espera I/O (llamadas HTTP salientes, consultas async a la base de datos). Si dentro de
un endpoint async se llama a código síncrono y bloqueante (por ejemplo, una librería sin
soporte async, o un cómputo pesado en CPU), se bloquea el event loop completo y afecta a todas
las demás peticiones concurrentes. Para esos casos, un endpoint `def` normal (no async) hace que
FastAPI lo ejecute automáticamente en un thread pool aparte, evitando bloquear el loop principal.

## Inyección de dependencias

El sistema `Depends()` de FastAPI permite declarar dependencias reutilizables (una sesión de
base de datos, el usuario autenticado, configuración) que FastAPI resuelve automáticamente antes
de ejecutar el handler:

```python
def get_settings() -> Settings:
    return Settings()

@app.get("/health")
async def health(settings: Settings = Depends(get_settings)):
    return {"status": "ok", "env": settings.environment}
```

Esto facilita el testing: en los tests se puede sobrescribir una dependencia
(`app.dependency_overrides[get_settings] = lambda: fake_settings`) sin tocar el código del
endpoint.

## Ciclo de vida de la aplicación (`lifespan`)

Recursos costosos de inicializar (un modelo de embeddings cargado en memoria, un pool de
conexiones) deben crearse una sola vez al arrancar la aplicación, no en cada request. El patrón
`lifespan` de FastAPI (un context manager async) es el lugar correcto para esto:

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.embedder = load_embedding_model()  # se carga una sola vez
    yield
    # limpieza de recursos aquí, al apagar la app

app = FastAPI(lifespan=lifespan)
```
