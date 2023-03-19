from fastapi import APIRouter

from app.db.database import insert_sicav, sort_by_creation_date
from app.sicavs.scraper import SicavScraper

router = APIRouter()


@router.get("/search/")
async def search():
    data = SicavScraper().scrape_data()
    status, message = (True, "Success") if data else (False, "There are no results")
    if data:
        for sicav in data:
            # Insert the Sicav document into the MongoDB collection
            result = await insert_sicav(sicav)

    return {"status": status, "message": message}


@router.get("/sort-by-date/")
async def sort_by_date():
    result = await sort_by_creation_date()

    return {"sicavs": result}
