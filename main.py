from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.endpoints import inference, flashcards, upload
import uvicorn

app = FastAPI()
# Allow localhost and 127.0.0.1
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:1231",
    "http://127.0.0.1:1231",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Include the routers
app.include_router(inference.router, prefix="/api")
app.include_router(flashcards.router, prefix="/api")
app.include_router(upload.router, prefix="/api")


@app.get("/")
def read_root():
    return {"message": "Welcome to the Flashcard API"}

# from core.database import init_db

# init_db()


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=1231)
