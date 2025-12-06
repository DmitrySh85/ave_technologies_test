from fastapi import FastAPI

from phones.router import router as phones_router

app = FastAPI(
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json'
)

app.include_router(phones_router)