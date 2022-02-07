from fastapi import FastAPI

app = FastAPI(title="Media Library",
              description="This is a personal media library. Users are able "
                          "to add, edit, remove, categorize, and view media items like movies, games, and music.",
              version="0.1")


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
