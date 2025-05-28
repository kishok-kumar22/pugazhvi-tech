from fastapi import APIRouter, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from config.logger import logger
from config.database import get_db

from auth.security import oauth2_scheme

# Service Layer Imports
from service.AuthUserService import GroupsService, UserService

# Schema Layer Imports
from schema.ApiResponse import APIResponse
from schema.AuthUserSchema import CreatUserSchema, UserLoginSchema, UserResponseSchema, CreateGroupsSchema

# Auth Layer Imports
from auth.security import auth_handler


class AuthUserRouter:
    def __init__(self):
        self.logger = logger.getChild(self.__class__.__name__)
        self.classname = "AuthUserRouter"
       
    def _get_request(self, db: AsyncSession) -> UserService:
        return UserService(db)

    def register_router(self):
        router = APIRouter(prefix="/api/auth/users", tags=["Users"])

        @router.post("/register", response_model=APIResponse)
        async def register(data: CreatUserSchema, db=Depends(get_db)):
            try:
                self.logger.info(f"Entering in {self.classname} (register) --> : ")
                service = self._get_request(db)
                response = await service.create(payload=data)
                self.logger.info(f"Exiting in {self.classname} (register) --> : ")
                return JSONResponse(status_code=response.status_code, content=jsonable_encoder(response))
            except Exception as e:
                self.logger.error(f"Exception in {self.classname} (register): {e}")
                response_data = APIResponse.create(
                    success=False, 
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    message="Internal Server Error", 
                    data=[]
                )
                return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=jsonable_encoder(response_data))

        @router.post("/login", response_model=APIResponse)
        async def login(data: UserLoginSchema, db=Depends(get_db)):
            try:
                self.logger.info(f"Entering in {self.classname} (login) --> : ")
                service = self._get_request(db)
                response = await service.login(data)
                self.logger.info(f"Exiting in {self.classname} (login) --> : ")
                return JSONResponse(status_code=response.status_code, content=jsonable_encoder(response))
            except Exception as e:
                self.logger.error(f"Exception in {self.classname} (login): {e}")
                response_data = APIResponse.create(
                    success=False, 
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    message="Internal Server Error", 
                    data=[]
                )
                return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=jsonable_encoder(response_data))

        @router.post("/login-status", response_model=APIResponse)
        async def check_login_status(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
            try:
                self.logger.info(f"Entering in {self.classname} (check_login_status) --> : ")
                service = self._get_request(db)
                response = await service.check_login_status(token)
                self.logger.info(f"Exiting in {self.classname} (check_login_status) --> : ")
                return JSONResponse(status_code=response.status_code, content=jsonable_encoder(response))
            except Exception as e:
                self.logger.error(f"Exception in {self.classname} (check_login_status): {e}")
                response_data = APIResponse.create(
                    success=False, 
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    message="Internal Server Error", 
                    data=[]
                )
                return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=jsonable_encoder(response_data))

        @router.post("/me", response_model=APIResponse)
        async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
            try:
                self.logger.info(f"Entering in {self.classname} (get_current_user) --> : ")
                service = self._get_request(db)
                response = await service.get_current_user(token)
                self.logger.info(f"Exiting in {self.classname} (get_current_user) --> : ")
                return JSONResponse(status_code=response.status_code, content=jsonable_encoder(response))
            except Exception as e:
                self.logger.error(f"Exception in {self.classname} (get_current_user): {e}")
                response_data = APIResponse.create(
                    success=False, 
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    message="Internal Server Error", 
                    data=[]
                )
                return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=jsonable_encoder(response_data))
        

        @router.post("/checkValid")
        async def checkUserValid(user = Depends(auth_handler.get_user_login_in), db:AsyncSession = Depends(get_db)):

            print("User Details ==>  : ", user)
            print("User Namwe Details ==>  : ", user.username)
            print("User Id Details ==>  : ", user.id)
            return "Welcome To Millennium Desk , You are Loged IN !"

        return router
    

class AuthGroupsRouter :
    def __init__(self):
        self.logger = logger.getChild(self.__class__.__name__)
        self.classname = "AuthUserRouter"
       
    def _get_request(self, user, db: AsyncSession) -> GroupsService:
        return GroupsService(user=user, db=db)
    
    def register_router(self):
        router = APIRouter(prefix="/api/auth/groups", tags=["Groups"])

        @router.post("/create", response_model=APIResponse)
        async def create(data: CreateGroupsSchema, user=Depends(auth_handler.get_user_login_in), db=Depends(get_db)):
            try:
                self.logger.info(f"Entering in {self.classname} (create) --> : {user.username}")
                service = self._get_request(user=user, db=db)
                response = await service.create(payload=data)
                self.logger.info(f"Exiting in {self.classname} (create) --> : {user.username}")
                return JSONResponse(status_code=response.status_code, content=jsonable_encoder(response))
            except Exception as e:
                self.logger.error(f"Exception in {self.classname} (create): {e}")
                response_data = APIResponse.create(success=False,status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,message="Internal Server Error", 
                    data=[]
                )
                return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=jsonable_encoder(response_data))
        

        return router