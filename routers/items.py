from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from cache import get_cache, set_cache
from database import get_db
from models import Item
from schemas import ItemCreate, ItemOut

router = APIRouter(prefix="/items")


@router.post("", response_model=ItemOut, status_code=201)
async def create_item(payload: ItemCreate, db: AsyncSession = Depends(get_db)):
    item = Item(name=payload.name, description=payload.description)
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item


@router.get("", response_model=list[ItemOut])
async def list_items(db: AsyncSession = Depends(get_db)):
    cached = await get_cache("items:all")
    if cached is not None:
        return cached

    result = await db.execute(select(Item).order_by(Item.created_at.desc()))
    items = result.scalars().all()

    await set_cache("items:all", [ItemOut.model_validate(i).model_dump() for i in items])
    return items
