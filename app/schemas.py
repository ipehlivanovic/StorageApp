from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional


class ItemBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100,
                      description="Item name")
    quantity: float = Field(..., gt=0, description="Item quantity")
    unit: str = Field(..., min_length=1, max_length=50,
                      description="Unit of measure")


class ItemCreate(ItemBase):  # POST request
    pass  # Inherits all from ItemBase


class ItemUpdate(ItemBase):  # PUT request
    # Override mandatory fields into Optional, the rest is inherited
    name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    quantity: Optional[float] = Field(default=None, gt=0)
    unit: Optional[str] = Field(default=None, min_length=1, max_length=100)


class Item(ItemBase):  # GET request
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
