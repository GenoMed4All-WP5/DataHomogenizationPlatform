from typing import Optional

from fastapi import FastAPI
from fastapi.responses import JSONResponse, PlainTextResponse
from pydantic import BaseModel
from starlette import status

from utils.ClassLoader import ClassLoader


class ErrorMessage(BaseModel):
    message: str


class ResponseMessage(BaseModel):
    id: str
    value: str


class Item(BaseModel):
    service: Optional[str] = None
    useCase: Optional[str] = None


homogenizationPlatformAPI = FastAPI()

homogenizationPlatformAPI.description = """
Executor API allow the user to run any AIReady pipeline from a HTTP Request.

You will be able to:

* **Run an AIReady pipeline with id**.
* **Run an AIReady pipeline with some limited input parameters**.
"""


@homogenizationPlatformAPI.get("/")
async def root():
    return {"message": "Hello World"}

@homogenizationPlatformAPI.post("/feature", responses={
    404: {
        "model": ErrorMessage,
        "description": "The item was not found",
        "content": {
            "application/json": {
                "example": {"message": "The item was not found"}
            }
        }
    },
    200: {
        "model": ResponseMessage,
        "description": "Process requested by ID",
        "content": {
            "application/json": {
                "example": {"id": "process_id", "value": "Process run properly"}
            }
        },
    },
}, description="Run an AIReady pipeline with id")
def post(item: Item = None):
    try:
        out = run_util_class(item)
        return out
    except BaseException as exp:
        content = {
            "error": str(exp),
            "errorCode": status.HTTP_500_INTERNAL_SERVER_ERROR
        }
        return JSONResponse(content=content, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@homogenizationPlatformAPI.post("/data_homogenization", responses={
    404: {
        "model": ErrorMessage,
        "description": "The item was not found",
        "content": {
            "application/json": {
                "example": {"message": "The item was not found"}
            }
        }
    },
    200: {
        "model": ResponseMessage,
        "description": "Process requested by ID",
        "content": {
            "application/json": {
                "example": {"id": "process_id", "value": "Process run properly"}
            }
        },
    },
}, description="Run an AIReady pipeline with id")
async def post(item: Item = None):
    try:
        out = run_util_class(item)
        return out
    except BaseException as exp:
        content = {
            "error": str(exp),
            "errorCode": status.HTTP_500_INTERNAL_SERVER_ERROR
        }
        return JSONResponse(content=content, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@homogenizationPlatformAPI.post("/mds/{service}", status_code=200)
async def run_mds_service(service: str):
    response = run_util_class(service_name=service, use_case="mds")
    return response


def run_util_class(service: Item = None, service_name: str = None, use_case: str = None):
    use_case = service.useCase
    service_id = service.service
    class_path = f'extensions.DataHomogenizationPlatform.fast_http_handler.utils.pipelines.{use_case.lower()}.{service_id}'
    try:
        service = ClassLoader.load('', class_path, '')
    except:
        try:
            service = ClassLoader.load('', class_path + "Util", '')
        except:
            return {"errors": {"status": "404",
                               "title": "Service " + service + "not found"
                               }
                    }
    srv = service()
    response = srv.execute()
    return response

