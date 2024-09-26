import asyncio

import uvicorn
from fastapi import FastAPI

from src.api.routers import all_routers
from src.db.db import create_database

app = FastAPI()

for router in all_routers:
    app.include_router(router)


if __name__ == "__main__":
    asyncio.run(create_database())
    uvicorn.run(app="main:app", reload=True)