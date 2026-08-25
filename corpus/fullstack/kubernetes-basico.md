# Kubernetes: conceptos básicos

## Por qué Kubernetes

Docker resuelve empaquetar y correr un contenedor; Kubernetes resuelve **orquestar muchos
contenedores en muchas máquinas**: reiniciar contenedores que fallan, distribuir tráfico entre
réplicas, escalar automáticamente según carga, y desplegar actualizaciones sin downtime. Tiene
sentido adoptarlo cuando la complejidad operativa real (múltiples servicios, necesidad de
autoescalado, alta disponibilidad) lo justifica — para un proyecto pequeño con un backend y una
base de datos, una plataforma gestionada tipo Render o Railway suele ser más simple y suficiente
sin la sobrecarga operativa de administrar un clúster.

## Pods, Deployments y Services

- **Pod**: la unidad más pequeña desplegable, uno o más contenedores que comparten red y
  almacenamiento. Los pods son efímeros y no se crean directamente en producción.
- **Deployment**: describe el estado deseado de un conjunto de pods idénticos (qué imagen, cuántas
  réplicas) y se encarga de reconciliar la realidad con ese estado — si un pod muere, el
  Deployment crea uno nuevo automáticamente.
- **Service**: una IP/nombre DNS estable que balancea tráfico entre los pods de un Deployment,
  necesario porque los pods individuales aparecen y desaparecen con IPs cambiantes.

## Manifiestos declarativos

Kubernetes se gestiona declarando el estado deseado en YAML, no con comandos imperativos paso a
paso. `kubectl apply -f deployment.yaml` le dice al clúster "asegúrate de que la realidad
coincida con esto", y el control plane reconcilia continuamente cualquier diferencia (un nodo
que cae, un pod que crashea) sin intervención manual.

## ConfigMaps y Secrets

La configuración no debe estar hardcodeada en la imagen de un contenedor, porque eso obliga a
reconstruir la imagen para cambiar un valor de configuración entre entornos. `ConfigMap` externaliza
configuración no sensible (URLs, flags), y `Secret` hace lo mismo para datos sensibles
(contraseñas, API keys), inyectados como variables de entorno o archivos montados en el pod sin
modificar la imagen.

## Autoescalado horizontal

Un `HorizontalPodAutoscaler` ajusta automáticamente el número de réplicas de un Deployment según
una métrica (uso de CPU, memoria, o métricas custom), agregando pods bajo carga alta y
removiéndolos cuando baja. Esto solo funciona si la aplicación es **stateless** entre réplicas
(cualquier instancia puede atender cualquier request) — el estado que necesita persistir vive en
servicios externos al pod (base de datos, cache), nunca en el sistema de archivos local del
contenedor.
