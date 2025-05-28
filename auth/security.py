from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from config.settings import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM
from fastapi import status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from config.database import get_db
from config.logger import logger
from sqlalchemy.ext.asyncio import AsyncSession
from schema.ApiResponse import APIResponse
from repositories.AuthUserRepository import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")



class AuthSecurity:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.secret_key = SECRET_KEY
        self.algorithm = ALGORITHM
        self.access_token_expire = ACCESS_TOKEN_EXPIRE_MINUTES
        self.logger = logger.getChild(self.__class__.__name__)
        self.class_name = "AuthSecurity"
        self.status = status

    def _get_request(self, db: AsyncSession) -> UserRepository:
        return UserRepository(db)

    def get_hashed_password(self, password: str) -> str:
        return self.pwd_context.hash(password)
    
    def verify_hashed_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hash=hashed_password)
    
    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expires_delta = timedelta(minutes=int(self.access_token_expire))
        expire = datetime.now(timezone.utc) + expires_delta
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
    
    def create_refresh_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(days=7)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

    def verify_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            username: str = payload.get("sub")
            if username is None:
                return {"valid": False, "username": None}
            return {"valid": True, "username": username}
        except JWTError:
            return {"valid": False, "username": None}
        
    async def get_user_login_in(self, token:str = Depends(oauth2_scheme), db:AsyncSession = Depends(get_db)) :
        try :
            getUserName = self.verify_token(token=token)
            if not getUserName["valid"] :
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"isLogin" : False, "message" : "User Not Logged In" })
            
            service = self._get_request(db=db)
            user = await service.get_by_username(username=getUserName["username"])
            self.logger.info(f"Exiting in {self.class_name} (check_login_status) --> : ")
            
            if not user:
                self.logger.info(f"Exiting in {self.class_name} (check_login_status) --> : ")
                return APIResponse.create(success=False,status_code=status.HTTP_404_NOT_FOUND,message="User not found",data=[])
            
            return user
        except JWTError :
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, data={"isLogin" : False, "message" : "User Not Logged In" })

    
    
    

auth_handler = AuthSecurity()
    