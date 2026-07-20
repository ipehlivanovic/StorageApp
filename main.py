from fastapi import FastAPI 
from app.database import engine
from app.models import Base
from app.routers import items

# Create all tables or connect to the existing ones
Base.metadata.create_all(bind=engine)

# Start the app
app = FastAPI()

app.include_router(items.router)

# Endpoints
@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/health")
def health_status():
    return {"health_status": "Working"}