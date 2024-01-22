from fastapi import FastAPI
from database.config import init_db
from routers.users import user_router
from routers.roles import role_router

app = FastAPI()

init_db()

app.include_router(user_router, tags=["users"], prefix="/api/users")
app.include_router(role_router, tags=["roles"], prefix="/api/roles")
