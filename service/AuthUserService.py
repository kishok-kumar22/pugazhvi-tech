from fastapi import status
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from config.logger import logger
from schema.ApiResponse import APIResponse
from auth.security import AuthSecurity

from repositories.AuthUserRepository import UserRepository, GroupsRepository
from schema.AuthUserSchema import UserResponseSchema, CreatUserSchema as UserCreationSchema, UserLoginSchema, CreateGroupsSchema, GroupsResponseSchema

class UserService :
    
    def __init__(self, db=AsyncSession):
        self.db = db
        self.repo = UserRepository(db=db)
        self.security = AuthSecurity()
        self.logger = logger.getChild(self.__class__.__name__)
        self.class_name = "UserService"

    async def create(self, payload : UserCreationSchema) :
        try :
            self.logger.info(f"Entering in {self.class_name} (create) --> :  ")
            existing = await self.repo.is_details_occured(username=payload.username)

            if existing :
                payload_dict = payload.model_dump()
                existing_dict = existing.model_dump()
                
                conflict_fields = [field for field in ["username"] if existing_dict.get(field) == payload_dict.get(field)]
                self.logger.info(f"Exiting in {self.class_name} (create) --> :  ")
                response = APIResponse.create(success=False, status_code=status.HTTP_409_CONFLICT, message="The following fields data already exist.", data=conflict_fields)
                return response
            
            hashed_password = self.security.get_hashed_password(password=payload.password)
            payload_dict = payload.model_dump()
            payload_dict["password"] = hashed_password           
            request = await self.repo.create(data=payload_dict)
            serialized_data = UserResponseSchema.model_validate(request).model_dump()
            response = APIResponse.create(success=True, status_code=status.HTTP_201_CREATED, message="User Account Created Successfully", data=[serialized_data])
            return response

        except Exception as e :
            self.logger.error(f"Exception raised in {self.class_name} (create) -> : {str(e)}")
            raise Exception(f"Service error : {str(e)}")
    
    async def login(self, payload: UserLoginSchema):
        try:
            self.logger.info(f"Entering in {self.class_name} (login) --> :  ")
            user = await self.repo.get_by_username(username=payload.username)

            if not user:
                self.logger.info(f"Exiting in {self.class_name} (login) --> :  ")
                response = APIResponse.create(success=False, status_code=status.HTTP_404_NOT_FOUND,message="User Not Found", data=[])
                return response
        
            if not self.security.verify_hashed_password(plain_password=payload.password, 
                                                  hashed_password=user.password):
                self.logger.info(f"Exiting in {self.class_name} (login) --> :  ")
                response = APIResponse.create(success=False, status_code=status.HTTP_401_UNAUTHORIZED,message="Invalid Password", data=[])
                return response
        
            access_token = self.security.create_access_token(data={"sub": user.username})
            refresh_token = self.security.create_refresh_token(data={"sub": user.username})

            token_data = {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "bearer"
            }

            response = APIResponse.create(success=True, status_code=status.HTTP_200_OK, 
                                   message="Login Successfully", data=[token_data])
            return response
    
        except Exception as e:
            self.logger.error(f"Exception raised in {self.class_name} (login) -> : {str(e)}")
            raise Exception(f"Service error : {str(e)}")

    async def check_login_status(self, token: str) -> APIResponse:
        try:
            self.logger.info(f"Entering in {self.class_name} (check_login_status) --> : ")
            token_data = self.security.verify_token(token)
            
            if not token_data["valid"]:
                self.logger.info(f"Exiting in {self.class_name} (check_login_status) --> : ")
                return APIResponse.create(
                    success=False,
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    message="Invalid or expired token",
                    data=[]
                )

            user = await self.repo.get_by_username(username=token_data["username"])
            
            if not user:
                self.logger.info(f"Exiting in {self.class_name} (check_login_status) --> : ")
                return APIResponse.create(
                    success=False,
                    status_code=status.HTTP_404_NOT_FOUND,
                    message="User not found",
                    data=[]
                )

            self.logger.info(f"Exiting in {self.class_name} (check_login_status) --> : ")
            return APIResponse.create(
                success=True,
                status_code=status.HTTP_200_OK,
                message="User is logged in",
                data=[{
                    "username": user.username,
                    "firstName": user.firstname,
                    "lastName": user.lastname,
                    "is_active": user.is_active,
                    "is_superuser": user.is_superuser
                }]
            )
        except Exception as e:
            self.logger.error(f"Exception raised in {self.class_name} (check_login_status) -> : {str(e)}")
            raise Exception(f"Service error : {str(e)}")

    async def get_current_user(self, username: str) -> APIResponse:
        try:
            self.logger.info(f"Entering in {self.class_name} (get_current_user) --> : ")
            user = await self.repo.get_by_username(username=username)
            self.logger.info(f"Exiting in {self.class_name} (get_current_user) --> : ")
            return user
        except Exception as e:
            self.logger.error(f"Exception raised in {self.class_name} (get_current_user) -> : {str(e)}")
            raise Exception(f"Service error : {str(e)}")
        
    
            
class GroupsService:
    def __init__(self, user=None, db=AsyncSession):
        self.db = db
        self.repo = GroupsRepository(db=db, user=user)
        self.logger = logger.getChild(self.__class__.__name__)
        self.class_name = "GroupsService"
        self.user = user
    
    async def create(self, payload:CreateGroupsSchema) :
        try:
            self.logger.info(f"Entering in {self.class_name} (create) --> : {self.user.username}")
            print("Grouped Data ==> :  ", payload)
            payload = payload.model_copy(update={"created_by" : self.user.username})
            payload = payload.model_copy(update={"last_modified_by" : self.user.username})

            print("Grouped Data ==> :  ", payload)
            groups = await self.repo.create(data=payload)
            serialized_data = GroupsResponseSchema.model_validate(groups).model_dump()
            response = APIResponse.create(success=True, status_code=status.HTTP_201_CREATED, message="User Group Created Successfully", data=[serialized_data])
            self.logger.info(f"Exiting in {self.class_name} (create) --> : { self.user.username}")
            return response
        except Exception as e:
            self.logger.error(f"Expection raised in {self.class_name} (create) --> : {e}")
            raise Exception(f"Service error : {str(e)}")