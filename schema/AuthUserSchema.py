from enum import Enum
from typing import Annotated
from pydantic import BaseModel, ConfigDict, EmailStr, Field, StringConstraints, field_validator, constr
from datetime import datetime
from typing_extensions import Optional, List


class CreatUserSchema(BaseModel) :
    username: Annotated[str, StringConstraints(max_length=30)]
    firstname: Annotated[str, StringConstraints(max_length=100)]
    lastname: Annotated[str, StringConstraints(max_length=100)]
    password: Annotated[str, StringConstraints(min_length=8, max_length=300)]
    is_superuser: Optional[bool] = False
    is_active: Optional[bool] = True
    created_by: Optional[str] = None
    last_modified_by: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class UserResponseSchema(BaseModel) :
    id : int
    username: Annotated[str, StringConstraints(max_length=30)]
    firstname: Annotated[str, StringConstraints(max_length=100)]
    lastname: Annotated[str, StringConstraints(max_length=100)]
    is_superuser: Optional[bool]
    is_active: Optional[bool]
    created_by: Optional[str]
    last_modified_by: Optional[str]

    model_config = ConfigDict(from_attributes=True)

class UserLoginSchema(BaseModel):
    username: str
    password: str
    
    model_config = ConfigDict(from_attributes=True)

class CreateGroupsSchema(BaseModel) :
    name:Annotated[str, StringConstraints(max_length=30)]
    is_active:Optional[bool] = True
    created_by:Optional[str] = datetime.now()
    last_modified_by:Optional[str] = None

class GroupsResponseSchema(BaseModel) :
    id:int
    name:Annotated[str, StringConstraints(max_length=30)]
    is_active: Optional[bool]
    created_by: Optional[str]
    created_date:Optional[datetime]
    last_modified_date:Optional[datetime]
    last_modified_by: Optional[str]