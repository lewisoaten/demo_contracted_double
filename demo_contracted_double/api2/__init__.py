from fastapi import FastAPI

from ..model.result import Result

app = FastAPI()


@app.get("/sum/{first}/and/{second}", response_model=Result)
async def sum(first: int, second: int):
    return Result(
        first=first,
        second=second,
        result=first+second,
    )
