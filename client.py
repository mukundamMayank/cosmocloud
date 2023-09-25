import json
import requests

order_data = {
    "items": [
        {
            "name": "Product-16",
            "boughtQuantity": 5
        }
    ],
    "user_address": {
        "city": "Mumbai",
        "country": "India",
        "zip_code": "401107"
    }
}


order_json = json.dumps(order_data)


url = "http://localhost:8000/newOrder/"


headers = {"Content-Type": "application/json"}


response = requests.post(url, data=order_json, headers=headers)

if response.status_code == 200:
    print("Order created successfully")
    created_order = json.loads(response.text)
    print("Created Order:")
    print(json.dumps(created_order, indent=4))
else:
    print("Failed to create order")
    print("Response Status Code:", response.status_code)
    print("Response Body:", response.text)
