from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from ..models.item import Item, ItemCreate, ItemUpdate

router = APIRouter(
    prefix="/items",
    tags=["items"],
    responses={404: {"description": "Not found"}},
)

# Mock database
fake_items_db = {}
item_id_counter = 1

@router.post("/", response_model=Item, status_code=201)
async def create_item(item: ItemCreate):
    global item_id_counter
    item_id = item_id_counter
    item_id_counter += 1
    item_dict = item.model_dump()
    fake_items_db[item_id] = Item(id=item_id, **item_dict)
    return fake_items_db[item_id]

@router.get("/", response_model=List[Item])
async def read_items(skip: int = 0, limit: int = 10):
    return list(fake_items_db.values())[skip : skip + limit]

@router.get("/{item_id}", response_model=Item)
async def read_item(item_id: int):
    if item_id not in fake_items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return fake_items_db[item_id]

@router.put("/{item_id}", response_model=Item)
async def update_item(item_id: int, item: ItemUpdate):
    if item_id not in fake_items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    
    stored_item = fake_items_db[item_id]
    update_data = item.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(stored_item, field, value)
    
    fake_items_db[item_id] = stored_item
    return stored_item

@router.delete("/{item_id}", response_model=Item)
async def delete_item(item_id: int):
    if item_id not in fake_items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    
    item = fake_items_db[item_id]
    del fake_items_db[item_id]
    return item
