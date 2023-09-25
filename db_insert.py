from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
import uvicorn
from random import randint


app = FastAPI()

MONGO_URI = "mongodb://127.0.0.1:27017"
client = AsyncIOMotorClient(MONGO_URI)
db = client["cosmocloud"]
product_collection = db["products"]

def generate_dummy_product(i):

	product_name = f"Product-{i}"
	product_price = round(randint(10, 500), 2)
	product_quantity = randint(1, 100)
	return {
		"name": product_name,
		"price": product_price,
		"available_quantity": product_quantity,
		}


for i in range(10, 21):
	dummy_product = generate_dummy_product(i)
	product_collection.insert_one(dummy_product)



if __name__ == "__main__":
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
    