import asyncio
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from fastapi import FastAPI
from agents.controller import run_agent

app = FastAPI()
print("MAIN FILE LOADED")
@app.get("/search")
def search(q: str):
    result = run_agent(q)
    return {"result": result}