import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017/cnmv')

collection = client.cnmv.sicavs


async def get_num_docs():
    num_docs = await collection.count_documents({})
    print(f"Number of documents in 'sicavs' collection: {num_docs}")
    return num_docs


async def get_all_sicavs():
    sicavs = []
    async for document in collection.find():
        document["_id"] = str(document["_id"])
        sicavs.append(document)
    return sicavs


# Function to insert a Sicav
async def insert_sicav(sicav):
    try:
        # Check if the Sicav already exists in the MongoDB collection
        existing_sicav = await collection.find_one({"registry_number": sicav["registry_number"]})
        if existing_sicav:
            # Update the existing Sicav with the new data
            await collection.update_one({"_id": existing_sicav["_id"]}, {"$set": sicav})
            return f'Successfully updated document with _id: {existing_sicav["_id"]}'
        else:
            # Insert the new Sicav into the MongoDB collection
            result = await collection.insert_one(sicav)
            return f'Successfully inserted document with _id: {result.inserted_id}'
    except Exception as e:
        return f'Error inserting/updating sicav: {e}'


async def sort_by_creation_date():
    sicavs = []
    async for sicav in collection.find().sort('registry_date', 1):
        del sicav['_id']
        sicavs.append(dict(sicav))
    return sicavs


async def truncate_collection():
    result = await collection.delete_many({})
    return f"Deleted {result.deleted_count} documents from 'sicavs' collection"
