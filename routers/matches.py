import os
from bson import ObjectId

import motor.motor_asyncio
from fastapi import APIRouter, HTTPException
from fastapi import Body, status
from pymongo import ReturnDocument

from src.model_design import (
    Booking,
    User,
    BookingCollection,
    UserCollection,
    Court,
    CourtCollection,
)

router = APIRouter(prefix="/matches")

os.environ[
    "MONGODB_URL"
] = "mongodb+srv://ayushmansatpathy:Ib9dTUB1Pev4KTdl@hackumasscluster.v82w1dk.mongodb.net/"

client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])
db = client.college
booking_collection = db.get_collection("bookings")
users_collection = db.get_collection("users")
court_collection = db.get_collection("courts")


@router.post(
    "/users/",
    response_description="Add new User",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_user(user: User = Body(...)):
    conflicting_user = await users_collection.count_documents({"email": user.email})

    if conflicting_user > 0:
        return user

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
    conflicting_bookings = await booking_collection.count_documents(
        {
            "day": booking.day,
            "month": booking.month,
            "year": booking.year,
            "start": booking.start,
            "court": booking.court,
        }
    )

    if conflicting_bookings > 0:
        raise HTTPException(status_code=400, detail="timeslot is already booked")

    new_booking = await booking_collection.insert_one(
        booking.model_dump(by_alias=True, exclude=["id"])
    )

    created_booking = await booking_collection.find_one(
        {"_id": new_booking.inserted_id}
    )
    return created_booking


@router.put(
    "/bookings/{id}",
    response_description="Modify booking",
    response_model=Booking,
    response_model_by_alias=False,
)
async def change_booking(id: str, booking: Booking = Body(...)):
    booking = {
        k: v for k, v in booking.model_dump(by_alias=True).items() if v is not None
    }

    if len(booking) >= 1:
        update_result = await booking_collection.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": booking},
            return_document=ReturnDocument.AFTER,
        )
        if update_result is not None:
            return update_result
        else:
            raise HTTPException(status_code=404, detail=f"Student {id} not found")

    # The update is empty, but we should still return the matching document:
    if (existing_booking := await booking_collection.find_one({"_id": id})) is not None:
        return existing_booking

    raise HTTPException(status_code=404, detail=f"Student {id} not found")


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


@router.put(
    "/users/{id}",
    response_description="Modify user booking id",
    response_model=User,
    response_model_by_alias=False,
)
async def change_user_booking(id: str, booking_id: str):
    update_result = await users_collection.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$push": {"booking": booking_id}},
        return_document=ReturnDocument.AFTER,
    )
    if update_result is not None:
        return update_result
    else:
        raise HTTPException(status_code=404, detail=f"User {id} not found")


@router.get(
    "/users/{email}",
    response_description="get a specific username",
    response_model=User,
    response_model_by_alias=False,
)
async def get_user_by_email(email):
    user = await users_collection.find_one({"email": email})
    if user:
        return user
    raise HTTPException(
        status_code=404,
        detail=f"this email is NOT in the database",
    )


@router.get(
    "/bookings/daily",
    response_model=BookingCollection
)
async def get_daily_bookings(day: int, month: int, year: int):
    bookings = await booking_collection.find({"day": day, "month": month, "year": year}).to_list(20)
    return BookingCollection(bookings=bookings)


