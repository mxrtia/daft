from fastapi import FastAPI, Depends, HTTPException, status

from folder.views import router as northwind_api_router
from pydantic import PositiveInt
from sqlalchemy.orm import Session
from folder.database import get_db
from folder import crud, schemas


app = FastAPI()

app.include_router(northwind_api_router, tags=["northwind"])

@app.get("/suppliers", status_code = status.HTTP_200_OK)
async def suppliers(supplier_id: PositiveInt, db: Session = Depends(get_db)):
    db_suppliers = crud.get_suppliers(db, supplier_id)
    return db_suppliers

@router.get("/suppliers/{supplier_id}", response_model=schemas.Supplier)
async def get_supplier(supplier_id: PositiveInt, db: Session = Depends(get_db)):
    db_supplier = crud.get_supplier(db, supplier_id)
    if db_supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return db_supplier