
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
from datetime import datetime

router = APIRouter()

#def read_csv

@router.get("/get_investment_data_for_user")
async def read_items(
    userID: Optional[str] = str('123e4567-e89b-12d3-a456-426614174000'),
    fromID: Optional[datetime] = datetime.fromisoformat('2025-01-01T00:00:00'),
    toID: Optional[datetime] = datetime.fromisoformat('2025-01-01T00:00:00')
):
    return [
            {
                "title": "Tech",
                "percentage": 0.70,
                "Elements": [
                    {
                        "title": "Apple",
                        "percentage": 0.5
                    },
                    {
                        "title": "Google",
                        "percentage": 0.5
                    }
                ]
            },
            {
                "title": "Health",
                "percentage": 0.30,
                "Elements": [
                    {
                        "title": "Siemens",
                        "percentage": 0.30
                    },
                    {
                        "title": "MedTech",
                        "percentage": 0.25
                    },
                    {
                        "title": "GSK",
                        "percentage": 0.45
                    }
                ]
            }
        ]
    

@router.get("/get_aggregated_investment_data")
async def read_items(
    userID: Optional[str] = str('123e4567-e89b-12d3-a456-426614174000'),
    fromID: Optional[datetime] = datetime.fromisoformat('2025-01-01T00:00:00'),
    toID: Optional[datetime] = datetime.fromisoformat('2025-01-01T00:00:00')
):
    return [
            {
                "title": "Tech",
                "percentage": 0.70,
                "Elements": [
                    {
                        "title": "Apple",
                        "percentage": 0.5
                    },
                    {
                        "title": "Google",
                        "percentage": 0.5
                    }
                ]
            },
            {
                "title": "Health",
                "percentage": 0.30,
                "Elements": [
                    {
                        "title": "Siemens",
                        "percentage": 0.30
                    },
                    {
                        "title": "MedTech",
                        "percentage": 0.25
                    },
                    {
                        "title": "GSK",
                        "percentage": 0.45
                    }
                ]
            }
        ]


