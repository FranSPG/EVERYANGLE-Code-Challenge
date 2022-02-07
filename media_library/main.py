from fastapi import FastAPI
# from media_library.config import
from media_library.user import router as user_router
from media_library.media import router as media_router

app = FastAPI(title="Media Library",
              description="This is a personal media library. Users are able "
                          "to add, edit, remove, categorize, and view media items like movies, games, and music.",
              version="0.1")

app.include_router(user_router.router)
app.include_router(media_router.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
