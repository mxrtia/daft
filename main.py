from fastapi import FastAPI, Depends, HTTPException, status


from folder.views import router as northwind_api_router
from pydantic import PositiveInt
from sqlalchemy.orm import Session
from folder.database import get_db
from folder import crud, schemas


app = FastAPI()

app.include_router(northwind_api_router, tags=["northwind"])

