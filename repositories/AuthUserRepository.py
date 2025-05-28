from sqlalchemy.ext.asyncio import AsyncSession
from models.AuthUserModels import User, Groups
from schema.AuthUserSchema import CreatUserSchema, UserResponseSchema, CreateGroupsSchema, GroupsResponseSchema
from config.logger import logger
from typing import Optional
from sqlalchemy import select,or_



class UserRepository :
    def __init__(self, db:AsyncSession):
        self.db = db
        self.logger = logger.getChild(self.__class__.__name__)
        self.className = "UserRepository"
    
    async def create(self, data : CreatUserSchema) -> Optional[UserResponseSchema] :
        try :
            self.logger.info(f"Entering in {self.className} (create) -->  ")
            stmt = User(**data)
            self.db.add(stmt)
            await self.db.commit()
            await self.db.refresh(stmt)
            self.logger.info(f"Exiting in {self.className} (create) -->  ")
            return stmt
                    
        except Exception as e :
            # await self.db.rollback()
            self.logger.error(f"Exception raised in {self.className} (create) --> {str(e)}")
            raise Exception(f"Repository error {str(e)}")
    
    async def get_by_username(self, username:str) -> Optional[UserResponseSchema] :
        try :
            self.logger.info(f"Entering in {self.className} (get_by_username) -->  ")
            stmt = select(User).where(User.username == username)
            result = await self.db.execute(statement=stmt)
            user = result.scalar_one_or_none()
            self.logger.info(f"Exiting in {self.className} (create) -->  ")
            return user
        except Exception as e :
            self.logger.error(f"Exception raised in {self.className} (get_by_username) --> {str(e)}")
            raise Exception(f"Repository error {str(e)}")
        
    async def is_details_occured(self, username : str) -> Optional[UserResponseSchema]:
        try:
            self.logger.info(f"Entering in {self.className} (is_details_occured) -->  ")
            stmt = select(User).where(or_(User.username == username))
            result = await self.db.execute(statement=stmt)
            users =  result.scalars().first()
            self.logger.info(f"Exiting in {self.className} (is_details_occured) --> ")
            return UserResponseSchema.model_validate(users) if users else None
        
        except Exception as e :
            await self.db.rollback()
            self.logger.error(f"Exception raised in {self.className} (is_details_occured) --> {str(e)}")
            raise Exception(f"Repository error {str(e)}")
    

class GroupsRepository :
    def __init__(self, user, db:AsyncSession):
        self.db = db
        self.logger = logger.getChild(self.__class__.__name__)
        self.className = "GroupsRepository"
        self.user = user
    
    async def create(self, data:CreateGroupsSchema) -> Optional[GroupsResponseSchema]:
        try:
            self.logger.info(f"Entering in {self.className} (create) -->  {self.user.username}")
            stmt = Groups(**data)
            self.db.add(stmt)
            # await self.db.commit()
            # await self.db.refresh(stmt)

            self.logger.info(f"After Refresh in Group User {self.className} (create) -->  {self.user.username}")

            result  = await self.db.execute(select(Groups).where(Groups.id == stmt.id))
            created_group = result.scalar_one()
            self.logger.info(f"Exiting in {self.className} (create) -->  {self.user.username}")
            return created_group
        except Exception as e:
            await self.db.rollback()
            self.logger.error(f"Exception raised in {self.className} (create) --> {str(e)}")
            raise Exception(f"Repository error {str(e)}")

