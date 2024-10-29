from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Auditoria
import time

class AudiMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        method = request.method
        path = request.url.path
        start_time = time.time() 
        response: Response = await call_next(request)
        process_time = time.time() - start_time
        status_code = response.status_code

        db: Session = SessionLocal()
        db.add(Auditoria(
            method=method,
            path=path,
            status_code=status_code,
            client_ip=client_ip,
            process_time=process_time
        ))
        db.commit()
        db.close()

        return response
