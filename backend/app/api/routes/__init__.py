from fastapi import APIRouter
from app.api.routes import animation 

router = APIRouter()
router.include_router(animation.router) 