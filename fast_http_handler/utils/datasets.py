from fastapi import status, APIRouter, Depends, Security
from db.session import get_db
from models.dataset import DatasetSchema
from sqlalchemy.orm import Session
from db.cruds import create_dataset, get_dataset_by_id, get_datasets, delete_dataset_by_id
from fastapi.responses import JSONResponse
from helpers import auth

router = APIRouter(
    prefix="/datasets",
    tags=["datasets"],
    dependencies=None
)


@router.post("/")
async def add_datasets(dataset: DatasetSchema, db: Session = Depends(get_db)):
    try:
        resp = create_dataset(db, dataset)
        return {"inserted": resp.id}
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content=str(e))


@router.delete("/{dataset_id}")
async def remove_dataset(dataset_id: int, db: Session = Depends(get_db)):
    try:
        resp = delete_dataset_by_id(db, dataset_id)
        return {"deleted": dataset_id}
    except  Exception as e:
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content=str(e))


@router.get("/")
async def read_datasets(current_user=Security(auth.get_current_user), db: Session = Depends(get_db)):
    try:
        resp = get_datasets(db)
        # Dataset.parse_obj(resp[0].__dict__)
        return resp
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content=str(e))


@router.get("/{dataset_id}")
async def read_dataset_by_id(dataset_id: int, db: Session = Depends(get_db)):
    try:
        resp = get_dataset_by_id(db, dataset_id)
        # Dataset.parse_obj(resp[0].__dict__)
        return {"data": resp}
    except  Exception as e:
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content=str(e))
