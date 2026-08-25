# Fundamentos de Docker

## Contenedores vs máquinas virtuales

Un contenedor comparte el kernel del sistema operativo host y aísla procesos mediante
namespaces y cgroups de Linux, lo que lo hace mucho más liviano y rápido de iniciar que una
máquina virtual (que virtualiza hardware completo y corre un kernel propio). La ventaja central
de Docker para desarrollo y despliegue es la **reproducibilidad**: una imagen empaqueta la
aplicación junto con exactamente las versiones de sus dependencias del sistema, eliminando el
clásico "en mi máquina funciona" causado por diferencias de entorno entre desarrollo, CI y
producción.

## Imágenes en capas

Un `Dockerfile` describe una imagen como una secuencia de instrucciones, cada una generando una
capa inmutable cacheada. Docker reutiliza capas sin cambios entre builds, por lo que el **orden**
de las instrucciones importa para aprovechar el cache: las instrucciones que cambian con menos
frecuencia (instalar dependencias del sistema, copiar `requirements.txt`/`package.json` e
instalar paquetes) deben ir antes que copiar el código fuente completo, que cambia en casi cada
build.

```dockerfile
FROM python:3.12-slim
WORKDIR /app

# Se cachea mientras requirements.txt no cambie, aunque el código sí cambie
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Esta capa se invalida en cada cambio de código, pero es la más barata de rehacer
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Multi-stage builds

Para no incluir herramientas de compilación o dependencias de desarrollo en la imagen final
(que aumentan tamaño y superficie de ataque), un Dockerfile multi-stage compila/instala en una
etapa y copia solo los artefactos necesarios a una imagen final más pequeña:

```dockerfile
FROM node:20 AS build
WORKDIR /app
COPY . .
RUN npm ci && npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
```

## Volúmenes y persistencia

Los contenedores son efímeros por diseño: al eliminarse, cualquier dato escrito dentro de su
sistema de archivos se pierde. Los **volúmenes** (gestionados por Docker) o **bind mounts**
(una carpeta del host montada dentro del contenedor) son el mecanismo para persistir datos
(bases de datos, archivos subidos) más allá del ciclo de vida de un contenedor específico. En
desarrollo, un bind mount del código fuente permite hot-reload sin reconstruir la imagen en
cada cambio.

## Docker Compose para desarrollo local

`docker-compose.yml` define y orquesta múltiples servicios relacionados (backend, base de
datos, cache) como una unidad, con su propia red interna donde los servicios se resuelven por
nombre (`http://db:5432` en vez de `localhost`). Es la forma estándar de levantar un entorno de
desarrollo completo con un solo comando (`docker compose up`) sin instalar cada dependencia
directamente en la máquina del desarrollador.
