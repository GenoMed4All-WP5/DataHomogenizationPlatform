from typing import (
    Deque, Dict, FrozenSet, List, Optional, Sequence, Set, Tuple, Union
)
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Enum
from sqlalchemy.dialects.postgresql import JSON, JSONB, ARRAY
from sqlalchemy.orm import relationship

from db.session import Base


class DatasetSchema(BaseModel):
    name: str
    tag: List[str]
    description: str
    node_id: str
    data_loader: str
    path: str


# @@@@ DB @@@@
class DBDataset(Base):
    __tablename__ = "datasets"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False, unique=True)
    tag = Column(ARRAY(String), index=False)
    description = Column(String, index=False)
    data_loader = Column(String, index=False)  # csv,txt,images
    path = Column(String, index=False)
    node_id = Column(Integer, ForeignKey("nodes.id"))
