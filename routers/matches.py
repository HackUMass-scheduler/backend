import os

import motor.motor_asyncio
from fastapi import APIRouter
from fastapi import Body, status

from src.model_design import Booking, User, BookingCollection, UserCollection

router = APIRouter(prefix="/matches")

os.environ[
    "MONGODB_URL"
] = "mongodb+srv://ayushmansatpathy:Ib9dTUB1Pev4KTdl@hackumasscluster.v82w1dk.mongodb.net/"

client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])
db = client.college
booking_collection = db.get_collection("bookings")
users_collection = db.get_collection("users")


@router.post(
    "/users/",
    response_description="Add new User",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_user(user: User = Body(...)):
    new_user = await users_collection.insert_one(
        user.model_dump(by_alias=True, exclude=["id"])
    )
    created_user = await users_collection.find_one({"_id": new_user.inserted_id})
    return created_user


@router.post(
    "/bookings/",
    response_description="Add new booking",
    response_model=Booking,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_booking(booking: Booking = Body(...)):
    """
    Insert a new student record.

    A unique `id` will be created and provided in the response.
    """
    new_booking = await booking_collection.insert_one(
        booking.model_dump(by_alias=True, exclude=["id"])
    )
    created_booking = await booking_collection.find_one(
        {"_id": new_booking.inserted_id}
    )
    return created_booking


@router.get(
    "/bookings/",
    response_description="List all bookings",
    response_model=BookingCollection,
    response_model_by_alias=False,
)
async def list_bookings():
    return BookingCollection(bookings=await booking_collection.find().to_list(1000))


@router.get(
    "/users/",
    response_description="List all users",
    response_model=UserCollection,
    response_model_by_alias=False,
)
async def list_bookings():
    return UserCollection(users=await users_collection.find().to_list(1000))
