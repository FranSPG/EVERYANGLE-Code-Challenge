from typing import List, Optional

from fastapi import HTTPException, status

from . import model


async def new_user_register(request, database) -> model.User:
    new_user = model.User(name=request.name, email=request.email, password=request.password)
    database.add(new_user)
    database.commit()
    database.refresh(new_user)
    return new_user


async def all_users(database) -> List[model.User]:
    users = database.query(model.User).all()
    return users


async def get_user_by_id(user_id, database) -> Optional[model.User]:
    user_info = database.query(model.User).get(user_id)
    if not user_info:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data Not Found !")
    return user_info


async def delete_user_by_id(user_id, database):
    database.query(model.User).filter(model.User.id == user_id).delete()
    database.commit()
