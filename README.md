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

## Run pylint on all *.py files
```bash
pylint $(git ls-files '*.py')
 ```
## Run coverage locally
 
```bash
python -m coverage run && python -m coverage html -i --skip-empty &&  open htmlcov/index.html 
 ```