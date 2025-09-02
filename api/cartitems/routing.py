from fastapi import APIRouter, Depends, HTTPException, status, Response
from typing import List
from sqlmodel import Session, select
from api.cartitems.modules import CartItemResponse, CartItem, CartItemCreate, CartItemUpdate
from auth.utils import get_current_user
from database.config import get_session

router = APIRouter()


@router.get("/", response_model=List[CartItemResponse])
async def cart_item_get(
        session: Session = Depends(get_session),
        current_user=Depends(get_current_user)
):
    statement = select(CartItem).where(CartItem.user_id == current_user.id)
    cart_items = session.exec(statement)
    return cart_items


@router.post("/add", response_model=CartItemResponse)
def add_to_cart(
        cart_item: CartItemCreate,
        session: Session = Depends(get_session),
        current_user=Depends(get_current_user)
):
    stmt = select(CartItem).where(
        CartItem.user_id == current_user.id,
        CartItem.product_id == cart_item.product_id
    )
    existing_item = session.exec(stmt).first()

    if existing_item:
        existing_item.quantity += cart_item.quantity
        session.add(existing_item)
        session.commit()
        session.refresh(existing_item)
        return existing_item

    new_item = CartItem(
        user_id=current_user.id,
        product_id=cart_item.product_id,
        quantity=cart_item.quantity
    )
    session.add(new_item)
    session.commit()
    session.refresh(new_item)
    return new_item


@router.put("/{cart_item_id}", response_model=CartItemResponse)
def update_cart_item(
        cart_item_id: int,
        cart_update: CartItemUpdate,
        session: Session = Depends(get_session),
        current_user=Depends(get_current_user)
):
    stmt = select(CartItem).where(
        CartItem.id == cart_item_id,
        CartItem.user_id == current_user.id
    )
    cart_item = session.exec(stmt).first()

    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    if cart_update.quantity is not None:
        if cart_update.quantity <= 0:
            session.delete(cart_item)
            session.commit()
            return {"detail": "Item removed from cart"}
        else:
            cart_item.quantity = cart_update.quantity

    session.add(cart_item)
    session.commit()
    session.refresh(cart_item)
    return cart_item


@router.delete("/{cart_item_id}")
def delete_cart_item(
        cart_item_id: int,
        session: Session = Depends(get_session),
        current_user=Depends(get_current_user)
):
    stmt = select(CartItem).where(
        CartItem.id == cart_item_id,
        CartItem.user_id == current_user.id
    )
    cart_item = session.exec(stmt).first()

    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    session.delete(cart_item)
    session.commit()
    return {"detail": "Item removed from cart"}


@router.delete("/")
def clear_cart(
        session: Session = Depends(get_session),
        current_user=Depends(get_current_user)
):
    cart_items = session.exec(
        select(CartItem).where(CartItem.user_id == current_user.id)
    ).all()

    for item in cart_items:
        session.delete(item)

    session.commit()
    return {"detail": f"Cleared {len(cart_items)} items from cart"}


@router.get("/summary")
def get_cart_summary(
        session: Session = Depends(get_session),
        current_user=Depends(get_current_user)
):

    cart_items = session.exec(
        select(CartItem).where(CartItem.user_id == current_user.id)
    ).all()

    total_items = len(cart_items)
    total_quantity = sum(item.quantity for item in cart_items)

    return {
        "user_id": current_user.id,
        "total_items": total_items,
        "total_quantity": total_quantity,
        "items": cart_items
    }