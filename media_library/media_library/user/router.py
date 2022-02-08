from typing import List

from fastapi import APIRouter, Depends, status, Response, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from media_library import db
from . import schema
from . import service
from . import validator
from media_library.auth.jwt import get_current_user, create_access_token

router = APIRouter(
    tags=['Users'],
    prefix='/user'
)

templates = Jinja2Templates(directory="static/templates")
router.mount("/static", StaticFiles(directory="static"), name="static")


@router.get('/register')
def register_get(request: Request):
    return templates.TemplateResponse("auth/signup.html",
                                      {"request": request})


@router.post("/register")
async def signup(request: Request, database: Session = Depends(db.get_db)):
    form = await request.form()
    user = schema.User(name=form.get('name'),
                       email=form.get('email'),
                       password=form.get('password'))
    user_validation = await validator.verify_email_exist(user.email, database)
    if user_validation:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    await service.new_user_register(user, database)
    access_token = create_access_token(data={"sub": user.email})
    resp = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    resp.delete_cookie(key="access_token")
    resp.set_cookie("access_token", access_token)
    return resp


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_user_registration(request: schema.User, database: Session = Depends(db.get_db)):
    user = await validator.verify_email_exist(request.email, database)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )

    new_user = await service.new_user_register(request, database)
    return new_user


@router.get('/', response_model=List[schema.DisplayUser])
async def get_all_users(database: Session = Depends(db.get_db),
                        current_user: schema.User = Depends(get_current_user)):
    return await service.all_users(database)


@router.get('/{user_id}', response_model=schema.DisplayUser)
async def get_user_by_id(user_id: int, database: Session = Depends(db.get_db),
                         current_user: schema.User = Depends(get_current_user)):
    return await service.get_user_by_id(user_id, database)


@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def delete_user_by_id(user_id: int, database: Session = Depends(db.get_db),
                            current_user: schema.User = Depends(get_current_user)):
    return await service.delete_user_by_id(user_id, database)
