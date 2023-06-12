# FastAPI with auth and integration with Postgresql.
This template project can be used to jumpstart a REST API postgres backed project.

## HOTO:
Start all services
```bash
docker compose up
```
Start DB only
```bash
docker compose up db
```
Shutdown all services 
```bash
docker compose down
```
## Debug API:
* Start DB service with compose
* Execute [src/api.py](src/api.py) in debug mode (the service will start on localhost:8001)