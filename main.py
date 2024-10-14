# root/main.py
from app.main import app
from fastapi.middleware.cors import CORSMiddleware

allowed_origins = [
    "http://localhost:3000",
    "https://ecoinstrument.com.kz/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["X-Requested-With", "Content-Type", "Authorization"],
)


if __name__ == "__main__":
    app.run()
