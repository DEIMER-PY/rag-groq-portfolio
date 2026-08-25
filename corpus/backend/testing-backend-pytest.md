# Testing de backend con pytest

## Pirámide de testing

La pirámide de testing sugiere tener muchos tests unitarios rápidos y aislados (lógica pura,
sin red ni base de datos), menos tests de integración (verifican que varias piezas reales
trabajen juntas: la API con la base de datos), y pocos tests end-to-end (todo el sistema
desplegado, incluyendo frontend). La proporción importa porque los tests unitarios son baratos
de correr y de mantener; abusar de tests end-to-end hace la suite lenta y frágil (fallan por
razones ajenas al bug que se busca detectar, como timing o infraestructura).

## Fixtures en pytest

Una fixture es una función decorada con `@pytest.fixture` que provee un valor o recurso
reutilizable a los tests que la declaran como parámetro. Reemplaza el patrón `setUp`/`tearDown`
de `unittest` con algo más composable:

```python
import pytest
from app.main import app
from fastapi.testclient import TestClient

@pytest.fixture
def client():
    return TestClient(app)

def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
```

El `scope` de una fixture (`function`, `module`, `session`) controla cuántas veces se
recrea: `session` es útil para recursos costosos que pueden compartirse entre tests sin efectos
secundarios (ej. un contenedor de base de datos de test), `function` (el default) es más seguro
cuando el recurso debe empezar limpio en cada test.

## Mocking de dependencias externas

Los tests unitarios no deben depender de servicios externos reales (APIs de terceros, bases de
datos remotas) para ser rápidos y deterministas. `unittest.mock` o `pytest-mock` permiten
reemplazar esas dependencias por dobles controlados:

```python
def test_rag_pipeline_uses_web_fallback_on_low_similarity(mocker):
    mocker.patch("app.services.retrieval.match_documents", return_value=[])
    mock_web = mocker.patch("app.services.web_search.search", return_value=[{"url": "...", "snippet": "..."}])

    result = answer_query("¿qué framework es tendencia en 2026?")

    mock_web.assert_called_once()
    assert result.used_web_fallback is True
```

Es importante mockear en el **punto de uso** (el módulo que importa y llama a la dependencia),
no en el módulo original, porque Python resuelve el import al momento de la llamada.

## Tests parametrizados

`@pytest.mark.parametrize` evita duplicar un test casi idéntico para distintas entradas,
dejando explícita la tabla de casos:

```python
@pytest.mark.parametrize("query,expected_in_scope", [
    ("¿cómo optimizo una consulta SQL lenta?", True),
    ("¿cuál es la mejor receta de arroz con pollo?", False),
    ("explícame qué es un closure en JavaScript", True),
])
def test_scope_guardrail(query, expected_in_scope):
    assert is_in_scope(query) == expected_in_scope
```

## Cobertura y calidad de aserciones

`pytest-cov` mide qué líneas se ejecutaron durante la suite, pero un test que ejecuta código
sin aserciones significativas (o con aserciones triviales como `assert result is not None`)
infla la cobertura sin verificar comportamiento real. La pregunta útil no es "¿qué porcentaje
de líneas se ejecutó?" sino "¿este test fallaría si el comportamiento correcto se rompiera?".
