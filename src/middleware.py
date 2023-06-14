import time
from uuid import uuid4

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request


class ContextIdMiddleware(BaseHTTPMiddleware):
    HEADER_NAME = "X-Context-Id"

    async def dispatch(self, request: Request, call_next):
        context_id = request.headers.get('context-id', str(uuid4()))
        request.state.context_id = context_id
        response = await call_next(request)
        response.headers[self.HEADER_NAME] = context_id
        return response

    @staticmethod
    def get_context(request: Request) -> str:
        return request.state.context_id


class TimeMiddleware(BaseHTTPMiddleware):
    """This middleware adds "X-Process-Time" header with server code execution time."""
    HEADER_NAME = "X-Process-Time"

    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers[self.HEADER_NAME] = str(f'{process_time:0.4f} sec')
        return response
