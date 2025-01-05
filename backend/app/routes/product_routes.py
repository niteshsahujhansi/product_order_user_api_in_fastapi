from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Product
from database import get_db
from typing import List
from schemas import ProductCreate, ProductUpdate, ProductResponse
from auth import get_current_user, TokenData 

router = APIRouter()

@router.post("/product")
def create_product(product: ProductCreate, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
    new_product = Product(**product.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@router.get("/product", response_model=List[ProductResponse])
def get_all_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
    return db.query(Product).offset(skip).limit(limit).all()
    # orders = db.query(Product).filter(Product.user_id == current_user.id).all()
    # return orders
