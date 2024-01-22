import bcrypt

from fastapi import APIRouter

from database.config import session
from models.users import Role, User
from schemas.users import UserSchema, UserUpdateSchema


user_router = APIRouter()


@user_router.post("/")
async def create_user(user_data: UserSchema):
    is_user = (
        session.query(User)
        .where(User.email == user_data.email or User.phone == user_data.phone)
        .one_or_none()
    )

    if is_user:
        msg = "Already exists user with "
        email_msg = ""
        phone_msg = ""

        if is_user.email == user_data.email:
            email_msg = f"email: {user_data.email}"

        if is_user.phone == user_data.phone:
            phone_msg = f"phone: {user_data.phone}"

        if email_msg and phone_msg:
            return {
                "ok": False,
                "msg": f"{msg} {email_msg} and {phone_msg}",
                "result": is_user,
            }

        if email_msg:
            return {
                "ok": False,
                "msg": f"{msg}{email_msg}",
                "result": is_user,
            }

        if phone_msg:
            return {
                "ok": False,
                "msg": f"{msg}{phone_msg}",
                "result": is_user,
            }

    hashed_password = bcrypt.hashpw(
        user_data.password.encode("utf-8"), bcrypt.gensalt()
    )

    user_query = User(
        name=user_data.name,
        lastname=user_data.lastname,
        email=user_data.email,
        phone=user_data.phone,
        password=hashed_password,
        role_id=user_data.role_id,
    )
    session.add(user_query)
    session.commit()
    session.refresh(user_query)
    return {"ok": True, "msg": "user was successfully created", "result": user_query}


@user_router.get("/")
async def get_all_users():
    users_query = session.query(User).join(Role).filter(User.role_id == Role.id).all()

    return {
        "ok": True,
        "msg": "users were successfully retrieved",
        "result": users_query,
    }


@user_router.get("/{user_id}")
async def get_user_by_id(user_id: int):
    user_query = session.query(User).filter_by(id=user_id).first()

    if not user_query:
        return {"ok": False, "msg": "user not found", "result": None}

    return {"ok": True, "msg": "user was successfully retrieved", "result": user_query}


@user_router.put("/{user_id}")
async def update_user(user_id: int, new_user_data: UserUpdateSchema):
    user_query = session.query(User).filter_by(id=user_id).first()

    if not user_query:
        return {"ok": False, "msg": "user not found", "result": new_user_data}
    if new_user_data.phone:
        user_query.phone = new_user_data.phone
    if new_user_data.password:
        user_query.password = new_user_data.password

    session.add(user_query)
    session.commit()
    session.refresh(user_query)

    return {"ok": True, "msg": "user was successfully updated", "result": user_query}
