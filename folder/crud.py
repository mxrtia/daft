from sqlalchemy.orm import Session

from . import models, schemas
from sqlalchemy.sql.expression import func, update

#5.1

def get_suppliers(db: Session):
    return db.query(models.Supplier).order_by(models.Supplier.SupplierID).all()


def get_supplier(db: Session, id: int):
    return (
        db.query(models.Supplier).filter(models.Supplier.SupplierID == id).first()
    )

#5.2

def get_suppliers_products(db: Session, id: int):
    return db.query(models.Product.ProductID, models.Product.ProductName, models.Product.CategoryID, models.Category.CategoryName, models.Product.Discontinued).filter(models.Product.SupplierID == id, models.Product.CategoryID == models.Category.CategoryID).order_by(models.Product.ProductID.desc()).all()

#5.3
def create_supplier(db: Session, new_supplier: schemas.SupplierPost):
    highest_id = db.query(func.max(models.Supplier.SupplierID)).scalar()
    new_supplier.SupplierID = highest_id + 1
    db.add(models.Supplier(**new_supplier.dict()))
    db.commit()
    return get_supplier(db, highest_id + 1)

#5.4
def put_supplier(db: Session, id: int, put_supplier: schemas.SupplierPut):
    db_supplier = db.query(models.Supplier).filter(models.Supplier.SupplierID == id).one_or_none()
    if db_supplier is None:
        return None
    for var, value in vars(put_supplier).items():
        setattr(db_supplier, var, value) if value else None
    db.add(db_supplier)
    db.commit()
    db.refresh(db_supplier)
    return db_supplier

#5.5

def delete_supplier(db: Session, id: int):
    db.query(models.Supplier).filter(models.Supplier.SupplierID == id).delete()
    db.commit()

######################    

def get_shippers(db: Session):
    return db.query(models.Shipper).all()


def get_shipper(db: Session, shipper_id: int):
    return (
        db.query(models.Shipper).filter(models.Shipper.ShipperID == shipper_id).first()
    )

