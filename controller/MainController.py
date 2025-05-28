from fastapi import APIRouter
from .AuthUserController import *

MainRouter = APIRouter()
MainRouter.include_router((AuthUserRouter()).register_router())
MainRouter.include_router((AuthGroupsRouter()).register_router())


