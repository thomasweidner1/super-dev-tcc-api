from fastapi import FastAPI, APIRouter
from starlette.middleware.cors import CORSMiddleware

router = APIRouter()

app = FastAPI()

origins = [
    "http://localhost:4200",
    "https://hoosty.com.br"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)