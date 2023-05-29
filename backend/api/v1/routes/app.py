#!/usr/bin/python3
"""Career recommendation entry point."""
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from backend.api.settings import TEMPLATES, BASE_PATH
from backend.api.v1.migrates import *
from .user_routes import user_routers
from .career_routes import career_router
from .course_routes import course_router

app = FastAPI(
    title="Career recommendation system",
    description="""
    A technology-enabled tool designed to assist individuals in
    making informed decisions about their career path
    """,
    version="v1.0"
)

app.mount(str(BASE_PATH / "/static"), StaticFiles(
    directory=str(BASE_PATH / "static")
), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["set-cookie"],
)


@app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    """Career recommendation entry point."""
    return TEMPLATES.TemplateResponse(
        "index.html",
        {"request": request},
    )

app.include_router(user_routers)
app.include_router(career_router)
app.include_router(course_router)
