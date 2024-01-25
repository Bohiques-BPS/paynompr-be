from fastapi import FastAPI
import os
import uvicorn
from dotenv import load_dotenv
from database.config import init_db
from sqlalchemy import event
from routers.users import user_router
from routers.roles import role_router
from routers.auth import auth_router
from routers.code import code_router

from models.users import User, Role
from fastapi.middleware.cors import CORSMiddleware

from database.seed.user import initialize_table

load_dotenv()

URL = os.environ.get("URL")
PORT = os.environ.get("PORT")


# I set up this event before table creation
event.listen(User.__table__, "after_create", initialize_table)
event.listen(Role.__table__, "after_create", initialize_table)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()


app.include_router(auth_router, tags=["auth"], prefix="/api/auth")
app.include_router(user_router, tags=["users"], prefix="/api/users")
app.include_router(role_router, tags=["roles"], prefix="/api/roles")
app.include_router(code_router, tags=["codes"], prefix="/api/codes")


if __name__ == "__main__":
    uvicorn.run(app, port=PORT, host="0.0.0.0")
