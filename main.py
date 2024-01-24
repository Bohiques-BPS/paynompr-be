from fastapi import FastAPI
import uvicorn
from database.config import init_db
from sqlalchemy import event
from routers.users import user_router
from routers.roles import role_router
from routers.auth import auth_router
from routers.code import code_router

from models.users import User, Role
from fastapi.middleware.cors import CORSMiddleware

origins = ["http://localhost:5173", "https://app-paynompr.onrender.com"]


from database.seed.user import initialize_table

# I set up this event before table creation
event.listen(User.__table__, "after_create", initialize_table)
event.listen(Role.__table__, "after_create", initialize_table)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
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
    uvicorn.run(app, port=8080, host="0.0.0.0")
