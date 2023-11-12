from typing import Optional, List

from pydantic import ConfigDict, BaseModel, Field, EmailStr
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated

PyObjectId = Annotated[str, BeforeValidator(str)]


class User(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str = Field(...)
    email: EmailStr = Field(...)
    booking: Optional[List[PyObjectId]] = []
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {"name": "Jane Doe", "email": "jdoe@example.com"}
        },
    )


class Booking(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    court: int = Field(ge=1, le=3)
    day: int = Field(...)
    end: int = Field(...)
    month: int = Field(...)
    start: int = Field(...)
    year: int = Field(...)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "day": 0,
                "month": 3,
                "year": 2023,
                "start": 7,
                "end": 8,
                "court": 1,
            }
        },
    )


class BookingCollection(BaseModel):
    bookings: List[Booking]


class UserCollection(BaseModel):
    users: List[User]


class Court(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    number: int = Field(ge=1, le=3)
    hours: BookingCollection
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "name": "Jane Doe",
                "email": "jdoe@example.com",
                "number": 1,
            }
        },
    )


class CourtCollection(BaseModel):
    courts: List[Court]
