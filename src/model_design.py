from typing import Optional, List

from pydantic import ConfigDict, BaseModel, Field, EmailStr
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated

PyObjectId = Annotated[str, BeforeValidator(str)]


class User(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str = Field(...)
    email: EmailStr = Field(...)
    booked: bool = Field(...)
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "name": "Jane Doe",
                "email": "jdoe@example.com",
                "booked": False,
            }
        },
    )


class Booking(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    user: User
    start: int = Field(...)
    end: int = Field(...)
    court: int = Field(ge=1, le=3)
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "user": {
                    "name": "Jane Doe",
                    "email": "jdoe@example.com",
                    "booked": False,
                },
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
