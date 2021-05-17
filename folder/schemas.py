from pydantic import BaseModel, PositiveInt, constr
from typing import Optional, List


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
    HomePage: Optional[str]

    class Config:
        orm_mode = True


class SupplierPost(BaseModel):
    SupplierID: int = 0
    CompanyName: constr(max_length=60)
    ContactName: Optional[constr(max_length=60)]
    ContactTitle: Optional[constr(max_length=60)]
    Address: Optional[constr(max_length=60)]
    City: Optional[constr(max_length=60)]
    PostalCode: Optional[constr(max_length=60)]
    Country: Optional[constr(max_length=60)]
    Phone: Optional[constr(max_length=60)]

    class Config:
        orm_mode = True


class SupplierUpdate(BaseModel):
    CompanyName: constr(max_length=60)
    ContactName: Optional[constr(max_length=60)]
    ContactTitle: Optional[constr(max_length=60)]
    Address: Optional[constr(max_length=60)]
    City: Optional[constr(max_length=60)]
    PostalCode: Optional[constr(max_length=60)]
    Country: Optional[constr(max_length=60)]
    Phone: Optional[constr(max_length=60)]
    Fax: Optional[constr(max_length=60)] = None
    HomePage: Optional[str] = None

    class Config:
        orm_mode = True

class SupplierPut(BaseModel):
    SupplierID: PositiveInt
    CompanyName: Optional[constr(max_length=50)]
    ContactName: Optional[constr(max_length=50)]
    ContactTitle: Optional[constr(max_length=50)]
    Address: Optional[constr(max_length=50)]
    City: Optional[constr(max_length=50)]
    PostalCode: Optional[constr(max_length=50)]
    Country: Optional[constr(max_length=50)]
    Phone: Optional[constr(max_length=50)]
    Fax: Optional[constr(max_length=50)]
    HomePage: Optional[str]

    class Config:
        orm_mode = True

class Category(BaseModel):
    CategoryID: PositiveInt
    CategoryName: Optional[constr(max_length=50)]

    class Config:
        orm_mode = True


class Products(BaseModel):
    ProductID: PositiveInt
    ProductName: Optional[constr(max_length=50)]
    Category: List[Category]
    Discontinued: Optional[constr(max_length=50)]

    class Config:
        orm_mode = True

######################

class Shipper(BaseModel):
    ShipperID: PositiveInt
    CompanyName: constr(max_length=40)
    Phone: constr(max_length=24)

    class Config:
        orm_mode = True

