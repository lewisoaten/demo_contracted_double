from fastapi import FastAPI
from pydantic import BaseSettings
import httpx

from ..model.result import Result


class Settings(BaseSettings):
    api2_port: int = 8001

settings = Settings()

app = FastAPI()


@app.get("/add_ten/{value}")
async def root(value: int):
    async with httpx.AsyncClient() as client:
        r = await client.get(f"http://localhost:{settings.api2_port}/sum/10/and/{value}")
    return Result.parse_raw(r.text).result
