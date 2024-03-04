from fastapi import FastAPI, HTTPException
from typing import List
from models import User, Gender, Role, UserUpdate
from uuid import UUID, uuid4

app = FastAPI()

db: List[User] = [
    User(
        id=uuid4(),
        first_name="Vignesh",
        last_name="P",
        gender=Gender.male,
        roles=[Role.admin, Role.user]
    ),
    User(
        id=uuid4(),
        first_name="Karthik",
        last_name="P",
        gender=Gender.male,
        roles=[Role.student]
    )
]

@app.get("/api/users")
def users():
    return db

@app.post("/api/users")
def addUser(user: User):
    db.append(user)
    return {"id": user.id}

@app.put("/api/users/{user_id}")
def updateUser(user_update: UserUpdate, user_id: UUID):
    for user in db:
        if user.id == user_id:
            if user_update.first_name is not None:
                user.first_name = user_update.first_name
            if user_update.last_name is not None:
                user.last_name = user_update.last_name
            if user_update.roles is not None:
                user.roles = user_update.roles
            return {"message": "User updated successfully"}
    raise HTTPException(status_code=404, detail=f"User with id: {user_id} not found")

@app.delete("/api/users/{user_id}")
def deleteUser(user_id: UUID):
    for user in db:
        if user.id == user_id:
            db.remove(user)
            return {"message": "User deleted successfully"}
    raise HTTPException(status_code=404, detail=f"User with id: {user_id} not found")
