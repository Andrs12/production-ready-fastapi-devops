import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ItemCreate(BaseModel):
    name: str
    description: Optional[str] = None


class ItemOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    description: Optional[str] = None
    created_at: datetime
