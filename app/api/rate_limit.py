import time
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, HTTPException

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, limit=10, window=60):
        super().__init__(app)
        self.limit = limit
        self.window = window
        self.clients = {}

    async def dispatch(self, request: Request, call_next):
        ip = request.client.host
        now = time.time()

        history = self.clients.get(ip, [])
        history = [t for t in history if now - t < self.window]

        if len(history) >= self.limit:
            raise HTTPException(status_code=429, detail="Too many requests")

        history.append(now)
        self.clients[ip] = history

        return await call_next(request)