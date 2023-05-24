#!/usr/bin/python3
"""Career recommendation entry point."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.v1.migrates import *

app = FastAPI(
    title="Career recommendation system",
    description="""
    A technology-enabled tool designed to assist individuals in
    making informed decisions about their career path
    """,
    version="v1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["set-cookie"],
)


@app.get("/")
async def main():
    """Career recommendation entry point."""
    return {
        "message": "Welcome to the Career recommendation system"
    }