from fastapi import FastAPI
from .database import engine
from . import models
from .routers import post,user,auth,vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

# Since alembic is creating the tables , the below code is for creating tables using sqlalchemy
# models.Base.metadata.create_all(bind=engine)



app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], #allows specific requests
    allow_headers=["*"], #allows specific headers
)

@app.get('/')
def s():
    return {'hello':"wer"}

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)




