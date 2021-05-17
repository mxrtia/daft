from pydantic import BaseModel, PositiveInt, constr
from typing import Optional


class Supplier(BaseModel):
    SupplierID: PositiveInt
    CompanyName: constr(max_length=40)

    class Config:
        orm_mode = True

class Supplier2(BaseModel):
    SupplierID: PositiveInt
    CompanyName: Optional[constr(max_length=50)]
    ContactName: Optional[constr(max_length=50)]
    ContactTitle: Optional[constr(max_length=50)]
    Address: Optional[constr(max_length=50)]
    City: Optional[constr(max_length=50)]
    Region: Optional[constr(max_length=50)]
    PostalCode: Optional[constr(max_length=50)]
    Country: Optional[constr(max_length=50)]
    Phone: Optional[constr(max_length=50)]
    Fax: Optional[constr(max_length=50)]
    HomePage: Optional[constr(max_length=50)]

    class Config:
        orm_mode = True


######################

class Shipper(BaseModel):
    ShipperID: PositiveInt
    CompanyName: constr(max_length=40)
    Phone: constr(max_length=24)

    class Config:
        orm_mode = True

