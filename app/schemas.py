from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ListingBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=120, examples=["iPhone 15 128GB"])
    description: str = Field(..., min_length=10, examples=["Телефон в отличном состоянии"])
    price: int = Field(..., gt=0, examples=[65000])
    category: str = Field(..., min_length=2, max_length=80, examples=["Электроника"])
    city: str = Field(..., min_length=2, max_length=80, examples=["Москва"])
    seller_name: str = Field(..., min_length=2, max_length=80, examples=["Алексей"])


class ListingCreate(ListingBase):
    pass


class ListingUpdate(BaseModel):
    title: str | None = Field(None, min_length=3, max_length=120)
    description: str | None = Field(None, min_length=10)
    price: int | None = Field(None, gt=0)
    category: str | None = Field(None, min_length=2, max_length=80)
    city: str | None = Field(None, min_length=2, max_length=80)
    seller_name: str | None = Field(None, min_length=2, max_length=80)


class ListingResponse(ListingBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
