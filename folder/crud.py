from sqlalchemy.orm import Session

from . import models


def get_suppliers(db: Session):
    return db.query(models.Supplier).order_by(models.Supplier.SupplierID).all()


def get_supplier(db: Session, id: int):
    return (
        db.query(models.Supplier).filter(models.Supplier.SupplierID == id).first()
    )

def get_suppliers_products(db: Session, id: int):
    return db.query(models.Product).filter(models.Product.SupplierID == id).order_by(models.Product.ProductID.desc()).all()

######################    

def get_shippers(db: Session):
    return db.query(models.Shipper).all()


def get_shipper(db: Session, shipper_id: int):
    return (
        db.query(models.Shipper).filter(models.Shipper.ShipperID == shipper_id).first()
    )

