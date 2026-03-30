import asyncio
import sys

# Only apply fix on Windows
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from fastapi import FastAPI
from agents.controller import run_agent

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Shopping AI Agent is running 🚀"}