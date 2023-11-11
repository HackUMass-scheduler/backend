from fastapi import FastAPI

from routers import matches
from routers import users

app = FastAPI()

app.include_router(users.router)
app.include_router(matches.router)
