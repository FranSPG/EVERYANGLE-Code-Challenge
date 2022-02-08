from fastapi import FastAPI

from media_library.user import router as user_router
from media_library.media import router as media_router
from media_library.auth import router as auth_router
from media_library.main import router as main_router

app = FastAPI(title="Media Library",
              description="This is a personal media library. Users are able "
                          "to add, edit, remove, categorize, and view media items like movies, games, and music.",
              version="0.1")

app.include_router(main_router.router)
app.include_router(auth_router.router)
app.include_router(user_router.router)
app.include_router(media_router.router)
