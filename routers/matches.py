from fastapi import APIRouter, FastAPI, HTTPException
import os
from typing import Optional, List
from routers.model_design import Booking, User, BookingCollection
from fastapi import FastAPI, Body, HTTPException, status
from fastapi.responses import Response
from pydantic import ConfigDict, BaseModel, Field, EmailStr
from pydantic.functional_validators import BeforeValidator

from typing_extensions import Annotated

from bson import ObjectId
import motor.motor_asyncio
from pymongo import ReturnDocument

router = APIRouter(prefix="/matches")
# match_db = {
#     "match1": {
#         "player": "niranjan",
#         "winner": "me",
#     },
#     "match2": {
#         "player": "mathirajan",
#         "winner": "you",
#     },
# }

# app = FastAPI(
#     title="Student Course API",
#     summary="A sample application showing how to use FastAPI to add a ReST API to a MongoDB collection.",
# )

os.environ[
    "MONGODB_URL"
] = "mongodb+srv://ayushmansatpathy:Ib9dTUB1Pev4KTdl@hackumasscluster.v82w1dk.mongodb.net/"

client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])
db = client.college
booking_colleciton = db.get_collection("bookings")


# @app.get("/{match_id}")
# async def match_info(match_id: str):
#     if match_id not in db:
#         raise HTTPException(status_code=404)
#     return {
#         "match player": match_db[match_id]["player"],
#         "match winner": match_db[match_id]["winner"],
#     }


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
    new_booking = await booking_colleciton.insert_one(
        booking.model_dump(by_alias=True, exclude=["id"])
    )
    created_booking = await booking_colleciton.find_one(
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
    return BookingCollection(bookings=await booking_colleciton.find().to_list(1000))
