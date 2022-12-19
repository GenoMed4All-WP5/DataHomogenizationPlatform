import os
from io import StringIO
import pandas as pd
from utils.ClassLoader import ClassLoader
from fastapi import FastAPI, File, Request, Response
from fastapi.responses import FileResponse, StreamingResponse
from typing import Optional
from fastapi import status, Depends, Security
from utils.db.session import get_db
from utils.models.dataset import DatasetSchema
from sqlalchemy.orm import Session
from utils.db.cruds import create_dataset, get_dataset_by_id, get_datasets, delete_dataset_by_id
from fastapi.responses import JSONResponse
from utils.helpers import auth

genomed4all_api = FastAPI()


@genomed4all_api.post("/")
async def add_datasets(dataset: DatasetSchema, db: Session = Depends(get_db)):
    try:
        resp = create_dataset(db, dataset)
        return {"inserted": resp.id}
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content=str(e))


@genomed4all_api.delete("/{dataset_id}")
async def remove_dataset(dataset_id: int, db: Session = Depends(get_db)):
    try:
        resp = delete_dataset_by_id(db, dataset_id)
        return {"deleted": dataset_id}
    except  Exception as e:
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content=str(e))


@genomed4all_api.get("/")
async def read_datasets(current_user=Security(auth.get_current_user), db: Session = Depends(get_db)):
    try:
        resp = get_datasets(db)
        # Dataset.parse_obj(resp[0].__dict__)
        return resp
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content=str(e))


@genomed4all_api.get("/{dataset_id}")
async def read_dataset_by_id(dataset_id: int, db: Session = Depends(get_db)):
    try:
        resp = get_dataset_by_id(db, dataset_id)
        # Dataset.parse_obj(resp[0].__dict__)
        return {"data": resp}
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content=str(e))


def run_util_class(service, definition):
    class_path = "extensions.Genomed4All.fast_http_handler.utils." + service
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
    response = srv.execute(definition)
    return response
