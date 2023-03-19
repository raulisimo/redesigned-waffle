import uvicorn
from fastapi import FastAPI

from app.db.database import client
from app.router.api.endpoints import api_router

app = FastAPI()

app.include_router(api_router)


@app.get("/", tags=["Health check"])
async def health_check():
    # Check if the database connection is working
    if client.server_info():
        return {"name": "CNMV scraping API",
                "type": "scraper",
                "description": "Scrape Sicavs from the CNMV",
                "documentation": "/docs",
                "database_status": "OK"}
    else:
        return {"name": "CNMV scraping API",
                "type": "scraper",
                "description": "Scrape Sicavs from the CNMV",
                "documentation": "/docs",
                "database_status": "ERROR"}


# For debugging
if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8080)
