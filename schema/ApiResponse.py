from pydantic import BaseModel, Field, ConfigDict
from typing import Any, Optional
from datetime import datetime
from http import HTTPStatus


class APIResponse(BaseModel):
    success: bool = Field(..., examples=[True])
    status_code: int = Field(..., examples=[200])
    status: str = Field(..., examples=["OK"])
    message: str = Field(..., examples=["Request processed successfully"])
    response: Optional[Any] = Field(default=None, examples=[{"id": 1, "name": "Admin"}])

  
    @classmethod
    def create(cls,success: bool,status_code: int,message: str,data: Optional[Any] = None,) -> "APIResponse":
        return cls(success=success,status_code=status_code,status=HTTPStatus(status_code).phrase,message=message,response=data)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "success": True,
                "status_code": 201,
                "status": "Created",
                "message": "Group created successfully",
                "response": [{
                    "id": 1,
                    "name": "Engineering",
                    "is_active": True,
                    "created_by": "admin",
                    "last_modified_by": "admin",
                    "created_date": "2025-04-05T12:00:00.000Z",
                    "last_modified_date": "2025-04-05T12:00:00.000Z"
                }]
            }
        }
    )
