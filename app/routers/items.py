
# app/routers/items.py
from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from datetime import datetime
import pandas as pd
import numpy as np
import logging
from ..models.item import Item, ItemCreate, ItemUpdate
from scripts.trade_republic_api_wrapper import *

router = APIRouter(
    prefix="/items",
    tags=["items"],
    responses={404: {"description": "Not found"}},
)

# Mock database
fake_items_db = {}
item_id_counter = 1

router = APIRouter()

def read_csv(filepath):
    '''
    Read csv files
    '''
    df = pd.read_csv(filepath, parse_dates = ['executedAt'])
    return df

def filter_customer(df, user = None, fromID = None, toID = None):
    '''
    Filter df
    '''
    if user != None:
        df[df['userId'] == user]
    if fromID != None:
        df[df['executedAt'] >= fromID]
    if toID != None:
        df[df['executedAt'] <= toID]
    return df

def add_volume(df):
    '''
    Add field volume, account for SELL.
    '''
    df['executionPrice'] = np.where(df['direction'] == 'SELL', 
                                    -df['executionPrice'], 
                                    df['executionPrice'])

    df['Volume'] = df['executionPrice'] * df['executionSize']
    return df

def group_by_ISIN_volume(df):
    '''
    Group df volume and sort values ascending.
    '''
    return df.groupby(['ISIN','sector', 'direction']).sum()

def load_top_investments(filepath, user = None, fromID = None, toID = None):

    df = read_csv('../../data/trading_sample_data.csv')
    df = filter_customer(df, user, fromID, toID)
    #df = add_volume(df)

    stock_data = pd.DataFrame()
    for i in df['ISIN']:
        try:
            stock_data = pd.concat([stock_data, pd.DataFrame([extract_info_from_isin(i)])], axis = 1)
        except:
            logging.warning('API could not fetch ISIN data')

    df = df.merge(stock_data, on = 'ISIN')
    df = group_by_ISIN_volume(df)
    df['share'] = df['your_column'] / df['your_column'].sum()



@router.get("/get_investment_data_for_user")
async def read_investment_data_user(
    userID: Optional[str] = str('00909ba7-ad01-42f1-9074-2773c7d3cf2c'),
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
async def read_investment_data(
    userID: Optional[str] = str('00909ba7-ad01-42f1-9074-2773c7d3cf2c'),
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

@router.get("/test_stock")
async def test_stock(
):
    df = read_csv('data/trading_sample_data.csv')
    stock_data = pd.DataFrame()

    for i in df['ISIN']:
        try:
            result = await extract_info_from_isin(i)  
            print(result)
            stock_data = pd.concat([stock_data, pd.DataFrame([result])], axis=0)
        except Exception as e:
            logging.warning(f'API could not fetch ISIN data for {i}: {e}')

    stock_data = stock_data.T  # Transpose if needed
    print(stock_data)

    return {"rows": stock_data.to_dict(orient="records")}


