from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field


class DonationBase(BaseModel):
    full_amount: Optional[int]
    comment: Optional[str]

    class Config:
        extra = Extra.forbid


class DonationCreate(DonationBase):
    full_amount: int = Field(..., gt=0)


class DonationUpdate(DonationBase):
    pass


class DonationRead(DonationCreate):
    id: int
    create_date: datetime
    user_id: int
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime]

    class Config:
        orm_mode = True