
# app/routers/items.py
from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from datetime import datetime
from ..models.item import Item, ItemCreate, ItemUpdate

router = APIRouter(
    prefix="/items",
    tags=["items"],
    responses={404: {"description": "Not found"}},
)

# Mock database
fake_items_db = {}
item_id_counter = 1

from fastapi import APIRouter
from uuid import UUID
from datetime import datetime

router = APIRouter()

@router.get("/get_investment_data_for_user")
async def read_items(userID: UUID, fromID: datetime, toID: datetime):
    return {
        "title": "Tech",
        "percentage": 0.30,
        "Elements": [
            {"title": "Apple", "percentage": 0.05},
            {"title": "Google", "percentage": 0.05}
        ]
    }



