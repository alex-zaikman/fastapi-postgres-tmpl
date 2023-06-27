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
# Use with logg
logger = logging.getLogger("api")
bt.add_task(logger.info, f'Informative log message.', extra={"context_id": context_id})
```

### TimeMiddleware
This middleware adds a ```X-Process-Time``` header to the response indicating server execution time, usfull for performance visabilty.

## DB environment variables

* ```DB_HOST```:   Host name
* ```DB_PORT```:  Port
* ```DB_USER```:  Username name
* ```DB_PASSWORD```:  Password
* ```DB_NAME```: Database name
* ```DB_NULL_POOL```: If set will set to not use pool (Useful for unit testing to avoid ```different loop``` error. )
* ```DB_ECHO```: If set will echo db messages

## DB API environment variables

* ```API_ALGORITHM``` : JWT token algorithm  ```default = HS256```
* ```API_ACCESS_TOKEN_EXPIRE_MINUTES``` : Access JWT token expiration time (minutes) ```default = 15```
* ```API_REFRESH_TOKEN_EXPIRE_DAYS``` : Refresh JWT token expiration time (minutes) ```default = 30```
* ```API_SECRET_KEY``` : Access secret key ```default = random```
* ```API_REFRESH_SECRET_KEY``` : Refresh secret key ```default = random```

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
