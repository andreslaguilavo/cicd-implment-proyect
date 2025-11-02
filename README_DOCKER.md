# CI/CD Week 3: Dockerized Flask + MySQL (2 contenedores)

Este repositorio contiene una app **Flask** con **SQLAlchemy** que se conecta a **MySQL**. 
Se provee un `Dockerfile` y un `docker-compose.yml` para levantar **dos contenedores comunicados entre sí**:

- **app**: la API Flask sirviendo en `http://localhost:5000`
- **db**: MySQL 8 con el esquema inicial vacío

## Requisitos previos
- Docker y Docker Compose instalados

## Cómo ejecutar
```bash
docker compose up --build
```
Cuando MySQL esté sano, la app subirá y podrás acceder a:
- `http://localhost:5000/` (si defines una ruta raíz)
- Endpoints bajo `/api` según tus blueprints (por ejemplo `/api/productos`, `/api/clientes`).

## Variables de entorno usadas por la app
La app lee estas variables (definidas en `docker-compose.yml`):
- `DB_USER`
- `DB_PASSWORD`
- `DB_HOST` (usa `db` para resolver al contenedor MySQL)
- `DB_NAME`

## Notas
- La app se ejecuta con **Gunicorn** en el contenedor (puerto 5000).
- Los modelos se crean automáticamente al iniciar (via `db.create_all()` si está habilitado).
- El volumen `dbdata` persiste los datos de MySQL entre reinicios.

## Comandos útiles
- Ver logs:
  ```bash
  docker compose logs -f app
  docker compose logs -f db
  ```
- Reconstruir:
  ```bash
  docker compose build --no-cache
  ```
- Derribar:
  ```bash
  docker compose down -v
  ```
