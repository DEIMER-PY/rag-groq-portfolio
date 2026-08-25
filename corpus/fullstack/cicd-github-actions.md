# CI/CD con GitHub Actions

## Integración continua vs entrega/despliegue continuo

**CI (Integración Continua)**: cada cambio (push, pull request) dispara automáticamente
compilación, linting y tests, dando feedback rápido antes de mergear a la rama principal. **CD
(Entrega/Despliegue Continuo)**: extiende el pipeline para empaquetar y desplegar
automáticamente a un entorno (staging o producción) cuando el CI pasa. La diferencia entre
"entrega" y "despliegue" continuo es si el paso final a producción requiere una aprobación
manual (entrega) o es completamente automático (despliegue).

## Estructura de un workflow de GitHub Actions

Un workflow es un archivo YAML en `.github/workflows/` que define disparadores (`on`), y uno o
más `jobs` compuestos de `steps` secuenciales que corren en un runner (una máquina efímera
provista por GitHub):

```yaml
name: Backend CI

on:
  push:
    branches: [develop, main]
    paths: ["backend/**"]
  pull_request:
    paths: ["backend/**"]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install -r backend/requirements.txt -r backend/requirements-dev.txt
      - run: pytest backend/tests -v
```

El filtro `paths` evita correr el pipeline de backend cuando solo cambió el frontend (y
viceversa), ahorrando minutos de CI en un monorepo.

## Jobs paralelos vs secuenciales

Los `jobs` de un workflow corren en paralelo por defecto (cada uno en su propio runner);
`needs: [job_anterior]` los encadena cuando un job depende del resultado de otro (por ejemplo,
solo desplegar si los tests pasaron). Dentro de un mismo job, los `steps` siempre son
secuenciales, ejecutados en el mismo runner y compartiendo el mismo sistema de archivos.

## Secrets y variables sensibles

Las credenciales (tokens de despliegue, API keys) nunca se hardcodean en el YAML; se configuran
como Secrets del repositorio (`Settings > Secrets and variables`) y se referencian con
`${{ secrets.NOMBRE }}`. GitHub los enmascara automáticamente en los logs si aparecieran por
error, pero la responsabilidad principal sigue siendo no imprimirlos deliberadamente ni pasarlos
a comandos que los expongan en el output.

## Cache de dependencias

Reinstalar dependencias desde cero en cada ejecución es lento; `actions/setup-python` y
`actions/setup-node` soportan cachear automáticamente el gestor de paquetes (`cache: "pip"`,
`cache: "npm"`) usando el hash del archivo de lockfile como clave — el cache se invalida
automáticamente cuando las dependencias cambian, pero se reutiliza en el resto de los casos.
