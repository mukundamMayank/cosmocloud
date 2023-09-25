from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from typing import List, Optional
from datetime import datetime
from bson import ObjectId
import uvicorn
from fastapi.responses import JSONResponse
import requests


app = FastAPI()

MONGO_URI = "mongodb://127.0.0.1:27017"
client = AsyncIOMotorClient(MONGO_URI)
db = client["cosmocloud"]
product_collection = db["products"]
order_collection = db["orders"]

class Product(BaseModel):
	name: str
	price: int
	available_quantity: int

class UserAddress(BaseModel):
    city: str
    country: str
    zip_code: str

class OrderItem(BaseModel):
    name: str
    boughtQuantity: int

class Order(BaseModel):
	timestamp: Optional[datetime]
	items: List[OrderItem]
	user_address: UserAddress
	totalAmount: Optional[int]

@app.get("/products/", response_model=List[Product])
async def list_products():
	products=[]
	async for product in product_collection.find():
		products.append(Product(**product))

	return products

async def update_product(product_id: str, update_prod_data:dict):
	try:
		object_id = ObjectId(product_id)
	except:
		return HTTPException(status_code=400, detail="Invalid ObjectId format")

	product = await product_collection.find_one({"_id":object_id})

	if product is None:
		return HTTPException(status_code=404, detail="Product not found")

	update_operations = {}
	for key, value in update_prod_data.items():
		update_operations[key] = value
	await product_collection.update_one({"_id": object_id}, {"$set": update_operations})

	return {"message": "Product updated successfully"}

@app.patch("/products/update/{product_id}/", response_model=dict)
async def update_product_endpoint(product_id: str, update_prod_data: dict):
	response = update_product(product_id, update_prod_data)

	return response


@app.post("/newOrder/", response_model=Order)
async def create_Order(order: Order):

	totol_amount = 0
	for item in order.items:
		product = await product_collection.find_one({"name":item.name})

		if product:
			product_price = product.get("price", 0.0)
			product_id = str(product["_id"])
			totol_amount+=product_price*item.boughtQuantity



			updated_available_quantity = product.get("available_quantity", 0.0)-item.boughtQuantity

			if updated_available_quantity < 0:
				error_message = {"message": "Order cannot be processed due to less availability"}
				return JSONResponse(content=error_message)

			product_data = {
				"available_quantity": updated_available_quantity
			}

			await update_product(product_id, product_data)


		else:
			return HTTPException(status_code=404, detail=f"Product '{item.product_name}' not found")

	order.totalAmount = totol_amount
	order.timestamp = datetime.now()
	result = await order_collection.insert_one(order.dict())
	return order

@app.get("/orders/", response_model=List[Order])
async def list_orders(limit: str = Query("10"), offset: str= Query("0")):
    orders = []
    limit = int(limit)
    offset = int(offset)

    if limit<0 or offset<0:
    	return HTTPException(status_code=404, detail="invalid limit or offset value")

    async for order in order_collection.find().skip(offset).limit(limit):
        orders.append(Order(**order))
    return orders


@app.get("/orders/{order_id}/", response_model=Order)
async def get_order(order_id: str):
	try:
		object_id = ObjectId(order_id)
	except Exception as e:
		return HTTPException(status_code=400, detail="Invalid ObjectId format")
	order = await order_collection.find_one({"_id": object_id})
	if order is None:
		raise HTTPException(status_code=404, detail="Order not found")
	return Order(**order)



if __name__ == "__main__":
    
    uvicorn.run(app, host="0.0.0.0", port=8000)