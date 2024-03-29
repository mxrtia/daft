from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import PositiveInt
from sqlalchemy.orm import Session

from . import crud, schemas
from .database import get_db

router = APIRouter()


@router.get("/suppliers/{id}", response_model=schemas.Supplier2)
async def get_supplier(id: PositiveInt, db: Session = Depends(get_db)):
    db_supplier = crud.get_supplier(db, id)
    if db_supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return db_supplier


@router.get("/suppliers", response_model=List[schemas.Supplier])
async def get_suppliers(db: Session = Depends(get_db)):
    return crud.get_suppliers(db)


@router.get("/suppliers/{id}/products")
async def get_suppliers_products(id: PositiveInt, db: Session = Depends(get_db)):
    db_products = crud.get_supplier(db, id)
    if db_products is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    db_product = crud.get_suppliers_products(db, id)
    return [{"ProductID": db['ProductID'], 'ProductName': f"{db['ProductName']}",
            'Category':{'CategoryID': db['CategoryID'],'CategoryName':f"{db['CategoryName']}"},
            'Discontinued':db['Discontinued'] } for db in db_product]


@router.post("/suppliers", response_model=schemas.Supplier2, status_code=201)
async def post_supplier(new_supplier: schemas.SupplierPost, db: Session = Depends(get_db)):
    return crud.create_supplier(db, new_supplier)


@router.put("/suppliers/{id}", response_model=schemas.Supplier2)
async def put_supplier(id: PositiveInt, put_supplier: schemas.SupplierPut, db: Session = Depends(get_db)):
    db_supplier = crud.get_supplier(db, id)
    if db_supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    db_supplier = crud.put_supplier(db, id, put_supplier)
    return db_supplier


@router.delete("/suppliers/{id}", status_code=204)
async def delete_supplier(id: PositiveInt, db: Session = Depends(get_db)):
    db_supplier = crud.get_supplier(db, id)
    if db_supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    crud.delete_supplier(db, id)

#############################


@router.get("/shippers/{shipper_id}", response_model=schemas.Shipper)
async def get_shipper(shipper_id: PositiveInt, db: Session = Depends(get_db)):
    db_shipper = crud.get_shipper(db, shipper_id)
    if db_shipper is None:
        raise HTTPException(status_code=404, detail="Shipper not found")
    return db_shipper


@router.get("/shippers", response_model=List[schemas.Shipper])
async def get_shippers(db: Session = Depends(get_db)):
    return crud.get_shippers(db)