from fastapi import FastAPI, Request, HTTPException as FastApiHTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from contextlib import asynccontextmanager
from fastapi.exceptions import RequestValidationError
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder



# Imported Modules From Created
from config.logger import logger
from config.database import AsyncSessionLocal, engine
from controller.MainController import MainRouter
from schema.ApiResponse import APIResponse

@asynccontextmanager
async def lifespan(app : FastAPI) :
    try :
        logger.info("Entering in LifeSpan ")
        async with AsyncSessionLocal() as session :
            await session.execute(text("select 1"))
        logger.info("✅ Database connection successful")
    except Exception as e :
        logger.error(f"❌ Database connection failed: {e}")

    
    yield
    
    try:
        await engine.dispose()
        logger.info("🛑 Database engine disposed successfully")
    except Exception as e:
        logger.error(f"⚠️ Error during shutdown: {e}")



app = FastAPI(debug=True, title="Pugazhvi Tech", version="1.0.0", lifespan=lifespan)

app.add_middleware(CORSMiddleware, allow_origins=["*"],allow_credentials=True,allow_methods=["*"],allow_headers=["*"])

app.include_router(MainRouter)

@app.get("/")
async def healthCkeck():
    return "🛑 Database engine disposed successfully"

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()

    # Sanitize ctx if it contains unserializable items
    for err in errors:
        if "ctx" in err:
            err["ctx"] = {
                k: str(v) for k, v in err["ctx"].items()
            }

    response = APIResponse.create(success=False,status_code=HTTP_422_UNPROCESSABLE_ENTITY,message="Validation Error",data=errors,)
    return JSONResponse(status_code=HTTP_422_UNPROCESSABLE_ENTITY,content=jsonable_encoder(response))


@app.exception_handler(FastApiHTTPException)
async def http_exception_handler(request: Request, exc: FastApiHTTPException):
    detail = exc.detail if isinstance(exc.detail, dict) else {"detail": exc.detail}

    response = APIResponse.create(success=False,status_code=exc.status_code,message="Error Occurred",data=detail)
    return JSONResponse(status_code=exc.status_code, content=jsonable_encoder(response))
