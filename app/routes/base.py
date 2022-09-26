from fastapi import APIRouter
from starlette.responses import Response
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.routes.user_auth.user_auth_handler import UserAuthHandler
from app.utils.auth import auth_manager
from app.common.config import config


base_router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


@base_router.get("/", include_in_schema=False)
async def index():
    current_time = datetime.utcnow() + timedelta(hours=9)
    return Response(f"Neubility Task API ( {current_time} )")

