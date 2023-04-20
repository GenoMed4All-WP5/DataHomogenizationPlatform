from sqlalchemy.orm import Session
from models.task import DBTask, BaseTask
from models.dataset import DBDataset, DatasetSchema
from models.node import DBNode, NodeSchema
from helpers import logger
log = logger.setup_applevel_logger()


# ######### TASK #############
def create_task(db: Session, task: BaseTask, user_id: int, org: int):
    db_item = DBTask(
        name=task.name,
        model_name=task.model.name,
        model_version=task.model.version,
        user_id=user_id,
        status="CREATED",
        dataset_ids=task.dataset_ids,
        org=org,
        num_rounds=task.num_rounds,
        library=task.library
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def delete_task_by_id(db: Session, task_id: int):
    task = db.query(DBTask).get(task_id)
    db.delete(task)
    db.commit()


def update_task_status_by_id(db: Session, task_id: int, status: str):
    task = db.query(DBTask).get({"id": task_id})
    task.status = status
    db.commit()
    db.refresh(task)
    return task


def get_tasks(db: Session):
    tasks = db.query(DBTask).order_by(DBTask.id.desc()).all()
    return tasks


def get_finished_tasks(db: Session):
    tasks = db.query(DBTask).filter((DBTask.status=="FAILURE") | (DBTask.status=="SUCCESS")).all()
    return tasks


def get_task_by_id(db: Session, task_id: int):
    task = db.query(DBTask).get(task_id)
    return task


def get_task_state_by_id(db: Session, task_id: int):
    task = db.query(DBTask).get(task_id)
    return task.status


def create_dataset(db: Session, dataset: DatasetSchema):
    node: DBNode = db.query(DBNode).get(dataset.node_id)
    db_item = DBDataset(
        name=dataset.name,
        tag=dataset.tag,
        description=dataset.description,
        data_loader=dataset.data_loader,
        path=dataset.path,
        # **dataset.dict()
    )
    node.datasets.append(db_item)
    db.add(db_item)
    try:
        db.commit()
        db.refresh(db_item)
        return db_item
    except Exception as e:
        raise Exception


def get_datasets(db: Session):
    datasets = db.query(DBDataset).all()
    return datasets


def get_dataset_by_id(db: Session, dataset_id: int):
    datasets = db.query(DBDataset).get(dataset_id)
    return datasets


def get_dataset_by_name(db: Session, dataset_name: str):
    task = db.query(DBDataset).filter_by(name=dataset_name).first()
    return task


def delete_dataset_by_id(db: Session, dataset_id: int):
    dataset = db.query(DBDataset).get(dataset_id)
    db.delete(dataset)
    db.commit()

# ############# NODE #################

def create_node(db: Session, node: NodeSchema):
    db_item = DBNode(**node.dict())
    db.add(db_item)
    try:
        db.commit()
        db.refresh(db_item)
        return db_item
    except Exception as e:
        raise Exception


def get_nodes(db: Session):
    nodes = db.query(DBNode).all()
    return nodes


def get_node_by_id(db: Session, node_id):
    node = db.query(DBNode).get(node_id)
    return node

def get_node_by_name(db: Session, node_name):
    node = db.query(DBNode).filter_by(name=node_name).first()
    return node


def delete_node_by_id(db: Session, node_id: int):
    dataset = db.query(DBNode).get(node_id)
    db.delete(dataset)
    db.commit()


def get_dataset_node(db: Session, dataset_id: int):
    dataset = get_dataset_by_id(db, dataset_id)
    return dataset.node

