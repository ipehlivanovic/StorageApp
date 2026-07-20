from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session

from app.database import get_db
from app import schemas
from app import crud

# Create a router instance
router = APIRouter(
    prefix="/items",        # All routes start with /items
    tags=["items"]          # Groups endpoints in docs
)


@router.get("/", response_model=List[schemas.Item])
def read_items(
    db: Session = Depends(get_db)
):
    return crud.get_items(db=db)


@router.get("/{item_id}", response_model=schemas.Item)
def read_item(
    item_id: int,
    db: Session = Depends(get_db)
):
    item = crud.get_item(db=db, querry_id=item_id)

    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with ID {item_id} not found"
        )

    return item


@router.post("/", response_model=schemas.Item, status_code=status.HTTP_201_CREATED)
def create_item(
    item: schemas.ItemCreate,
    db: Session = Depends(get_db)
):
    return crud.create_item(db=db, item_data=item)


@router.put("/{item_id}", response_model=schemas.Item)
def update_item(
    item_id: int,
    item_data_update: schemas.ItemUpdate,
    db: Session = Depends(get_db)
):
    updated_item = crud.update_item(
        db=db, querry_id=item_id, item_data=item_data_update)
    if updated_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with ID {item_id} not found"
        )

    return updated_item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(
    item_id: int,
    db: Session = Depends(get_db)
):
    success = crud.delete_item(db=db, querry_id=item_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with ID {item_id} not found"
        )

    return None
