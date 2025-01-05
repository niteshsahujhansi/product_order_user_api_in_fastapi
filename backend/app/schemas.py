from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class User(BaseModel):
    username: str
    email: EmailStr | None = None
    full_name: str | None = None
    disabled: bool | None = None

class UserInDB(User):
    # id: int
    id: Optional[int] = None
    hashed_password: str

class RegisterUser(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str | None = None


# Product schemas
class ProductBase(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float = Field(gt=0)
    stock: int = Field(ge=0)
    is_active: bool

    class Config:
        orm_mode = True  # Allow SQLAlchemy model to work with Pydantic model

class ProductCreate(BaseModel):
    name: str
    description: str
    price: float = Field(gt=0)
    stock: int = Field(ge=0)

    class Config:
        orm_mode = True

class ProductUpdate(BaseModel):
    description: Optional[str]
    price: Optional[float] = Field(gt=0)
    stock: Optional[int] = Field(ge=0)

    class Config:
        orm_mode = True

class ProductResponse(ProductBase):
    pass  # Inherits from ProductBase, this will be used in response


# Order schemas
class OrderCreate(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)

    class Config:
        orm_mode = True

class OrderResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    status: str
    # created_at: str

    class Config:
        orm_mode = True

