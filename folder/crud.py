from sqlalchemy.orm import Session

from . import models, schemas
from sqlalchemy.sql.expression import func, update



def get_suppliers(db: Session):
    return db.query(models.Supplier).order_by(models.Supplier.SupplierID).all()


def get_supplier(db: Session, id: int):
    return (
        db.query(models.Supplier).filter(models.Supplier.SupplierID == id).first()
    )

def get_suppliers_products(db: Session, id: int):
    return db.query(models.Product).filter(models.Product.SupplierID == id).order_by(models.Product.ProductID.desc()).all()

#5.3
def create_supplier(db: Session, new_supplier: schemas.SupplierPost):
    highest_id = db.query(func.max(models.Supplier.SupplierID)).scalar()
    new_supplier.SupplierID = highest_id + 1
    db.add(models.Supplier(**new_supplier.dict()))
    db.commit()
    return get_supplier(db, highest_id + 1)

# def post_supplier(db: Session, new_supplier: schemas.SupplierPost):
#     properties_to_update = {key: value for key, value in post_supplier.dict().items() if value is not None}
#     update_statement = update(models.Supplier).where(models.Supplier.SupplierID == id).values(**properties_to_update)
#     db.execute(update_statement)
#     db.commit()
#     return get_supplier(db, id)

#5.4
def put_supplier(db: Session, put_supplier: schemas.SupplierPut):
    properties_to_update = {key: value for key, value in post_supplier.dict().items() if value is not None}
    update_statement = update(models.Supplier).where(models.Supplier.SupplierID == id).values(**properties_to_update)
    db.execute(update_statement)
    db.commit()
    return get_supplier(db, id)

######################    

def get_shippers(db: Session):
    return db.query(models.Shipper).all()


def get_shipper(db: Session, shipper_id: int):
    return (
        db.query(models.Shipper).filter(models.Shipper.ShipperID == shipper_id).first()
    )

