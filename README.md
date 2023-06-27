# FastAPI with auth and integration with Postgresql.
This template project can be used to jumpstart a REST API postgres backed project.
It has stubs for testing and some usfull middleware.
## Middleware
### ContextIdMiddleware
This middleware adds a ```X-Context-Id``` header to the response, if such a header present in the request it will send it back if not a new one will be generated.
This id can be used a dependancy in the endpoints and used to achieve tracabilty in loggs.
i.e.

```python
# Inject as Dependency
@app.post('/foo', tags=['Example'])
async def foo(context_id: str = Depends(ContextIdMiddleware.get_context)):
 ...
```

```python
# Use in with logg
logger = logging.getLogger("api")
bt.add_task(logger.info, f'Informative log message.', extra={"context_id": context_id})
```

### TimeMiddleware
This middleware adds a ```X-Process-Time``` header to the response indicating server execution time, usfull for performance visabilty.
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
