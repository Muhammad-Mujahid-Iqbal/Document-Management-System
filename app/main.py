from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers.user import user
from .routers import auth
from .routers.document import metadata,status,summary
from .routers.customer import customer

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(customer.router)
app.include_router(metadata.router)
app.include_router(status.router)
app.include_router(summary.router)


@app.get("/")
async def root():
    return {"message": "Welcome to DMS APP by Mujahid"}
