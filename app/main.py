from fastapi import FastAPI
from app.api.routes import invoice_router

app = FastAPI()

app.include_router(invoice_router)