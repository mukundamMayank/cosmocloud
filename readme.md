1) Functionalities:
	
	a) Products can be viewed by /products/ route
	b) Orders can be placed using /newOrder/ route. You need to provide product name & quantity inorder to book the products
	c) Orders can be viewed in 2 ways mainly in groups by providing limit & offset to /orders/ route & secondly by order_id using
	   /orders/{order_id}
	d) /products/update/{product_id} route is defined to update the product properties for a particular product. It calls update_product method, this method is called by /newOrder/ route also to update the stock left for the product while placing the order.

2) How to run:
	a) Run db_insert.py & new values will be pushed to products collection of cosmocloud db, each time 10 new products gets created, atleast id is different.
	b) Make sure you have mongo installation done. Open terminal write mongo it will login to the mongo instance. In order to check collection data in database follow below steps:
		- use <name of the  database (cosmocloud in our case)>
		- db (to check the db you are currently using)
		- show collections (list all collections)
		- db.<collections_name (products & order in our case)>.find()
	c) server.py contains the api logic run it using 'uvicorn <name of the python file (server for our case)>:app --reload'. It will run on the ip & port you have specified in server.py file,  I have done it on localhost:8000.
	d) To test routes:
		- /products/ -> 'http://localhost:8000/products/'
		- /newOrder/ ->  run client.py where this api is called along with the json required 
		- /orders/ -> 'http://localhost:8000/orders/?limit=10&offset=0' this displays first 10 orders startig from 0
		- /orders/{order_id} -> 'http://localhost:8000/orders/?limit=<x>&offset=<y>' by default limit is set to 10 & offset is 0

	all of them to be run on browser except for /newOrder/ which is to be run bt running client.py in another terminal after server.py


***Note for Reviewers***
It is important to note that i have not used product_id to take orders as a user who is ordering might not be interested id rather than name. But a developer while updating deatils is more interested in product_id so I have fetched that & passed it to the method update_product. This is we are not only introducing separation of concern but also saving ourselves from infinfte loop issue, that might occure due to circular reference.

Please change the Mongo URI & replace it with your own string you will find that out once you run mongo on terminal.
