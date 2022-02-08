from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse

from media_library import db
from media_library.user import hashing
from media_library.user.model import User

from starlette.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from .jwt import create_access_token

router = APIRouter(
    tags=['auth']
)

templates = Jinja2Templates(directory="static/templates")
router.mount("/static", StaticFiles(directory="static"), name="static")


@router.get('/login')
def login_get(request: Request):
    return templates.TemplateResponse("auth/login.html",
                                      {"request": request})


@router.post("/login")
async def login(request: Request, database: Session = Depends(db.get_db)):
    """
    POST /logn. It validates if the user exists and if the password is correct.
    if everything is correct, it sets a cookie with the access token.
    :param request: Request data.
    :param database: Session of the database.
    :return: redirects to the home endpoint with the session logged.
    """
    form = await request.form()
    username = form.get('email')
    password = form.get('password')
    user = database.query(User).filter(User.email == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invalid Credentials')
    if not hashing.verify_password(password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invalid Credentials')
    access_token = create_access_token(data={"sub": user.email})

    resp = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    resp.delete_cookie(key="access_token")
    resp.set_cookie("access_token", access_token)
    return resp


@router.get("/logout")
async def logout():
    """
    It clears the cookie access token and return to the home with the user logged out.
    :return: redirects to the home endpoint without any session logged.
    """
    resp = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    resp.delete_cookie(key="access_token")
    return resp
