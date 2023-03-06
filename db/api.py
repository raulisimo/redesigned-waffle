from fastapi import APIRouter

from app.db.database import insert_sicav, get_num_docs, get_all_sicavs, truncate_collection

router = APIRouter()


@router.post("/sicavs", tags=["Insert One"])
async def add_sicav(sicav: dict):
    # Insert the Sicav document into the MongoDB collection
    result = await insert_sicav(sicav)
    return {"message": result}


@router.get("/sicavs", tags=["Get All"])
async def get_sicavs():
    sicavs = await get_all_sicavs()
    return {"sicavs": sicavs}


@router.get("/count-docs", tags=["Count Sicavs"])
async def count_docs():
    number_docs = await get_num_docs()
    return {"num_docs": number_docs}


@router.get("/truncate-collection", tags=["Delete All"])
async def remove_all():
    await truncate_collection()
