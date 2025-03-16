from fastapi import FastAPI
from api.endpoints import inference, flashcards, upload

app = FastAPI()

# Include the routers
app.include_router(inference.router, prefix="/api")
app.include_router(flashcards.router, prefix="/api")
app.include_router(upload.router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Flashcard API"}

from core.database import init_db

init_db()

print("This works!")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="localhost", port=1111)