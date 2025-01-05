from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas import OrderCreate, OrderResponse
from models import Order, Product
from database import get_db
from auth import get_current_user, TokenData 
from typing import List

router = APIRouter()

# @router.post("/order")
# def create_order(order: OrderCreate, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
#     db_order = Order(product_id=order.product_id, 
#                     quantity=order.quantity,
#                     user_id=current_user.id
#                     )
#     db.add(db_order)
#     db.commit()
#     db.refresh(db_order)
#     return db_order

@router.post("/order")
def create_order(
    order: OrderCreate, 
    db: Session = Depends(get_db), 
    current_user: TokenData = Depends(get_current_user)
):
    # Check if the product exists
    product = db.query(Product).filter(Product.id == order.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Check if the product has sufficient stock
    if product.stock < order.quantity:
        raise HTTPException(
            status_code=400, 
            detail=f"Insufficient stock for product '{product.name}'. Available stock: {product.stock}"
        )
    
    # Create the order
    db_order = Order(
        product_id=order.product_id,
        quantity=order.quantity,
        user_id=current_user.id
    )
    db.add(db_order)
    
    # Reduce product stock
    product.stock -= order.quantity
    db.commit()
    db.refresh(db_order)
    
    return db_order


@router.get("/orders", response_model=List[OrderResponse])
def get_all_orders(
    db: Session = Depends(get_db), 
    current_user: TokenData = Depends(get_current_user)
):
    orders = db.query(Order).filter(Order.user_id == current_user.id).all()
    return orders

from fastapi import Path
from typing import Literal

@router.put("/order/{order_id}")
def update_order_status(
    status: Literal["pending", "processing", "shipped", "delivered", "cancelled"],
    order_id: int = Path(..., description="The ID of the order to update"),
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user)
):
    order = db.query(Order).filter(Order.id == order_id, Order.user_id == current_user.id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    order.status = status
    db.commit()
    db.refresh(order)
    return order

@router.delete("/order/{order_id}")
def delete_order(
    order_id: int = Path(..., description="The ID of the order to delete"),
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user)
):
    order = db.query(Order).filter(Order.id == order_id, Order.user_id == current_user.id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    db.delete(order)
    db.commit()
    return {"message": "Order deleted successfully"}


