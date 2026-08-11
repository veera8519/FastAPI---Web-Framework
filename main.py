
from fastapi import FastAPI,HTTPException,status

from models import Product

app=FastAPI()

@app.get("/")
def greet():
    return ("welcome to code")

products=[
    Product(id=1,name="Phone",description="budget phone",price=99,quantity=2),
    Product(id=2,name="laptop",description="budget laptop",price=100, quantity=3),
    Product(id=3,name="car",description="budget car",price=99,quantity=4),
    Product(id=4,name="Tablet",description="portable tablet for work and entertainment",price=249,quantity=8),
    Product(id=5,name="Headphones",description="wireless noise-cancelling headphones",price=79,quantity=15),
    Product(id=6,name="Keyboard",description="compact mechanical keyboard",price=59,quantity=12),
    Product(id=7,name="Monitor",description="24-inch full HD monitor",price=179,quantity=6),
    Product(id=8,name="Smartwatch",description="fitness smartwatch with heart-rate tracking",price=129,quantity=10),
    Product(id=9,name="Camera",description="digital camera for everyday photography",price=399,quantity=5),
    Product(id=10,name="Backpack",description="water-resistant laptop backpack",price=45,quantity=20)
]


@app.get("/product")
def get_all_products():
    return products

@app.get("/product/{id}")
def get_product_by_id(id: int):
    for product in products:
        if product.id == id:
            return product

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

@app.post("/product")
def add_product(product:Product):
    products.append(product)
    return product

@app.put("/product")
def update_product(id:int,product:Product):
    for i in range(len(products)):
        if products[i].id == id:
            products[i] = product
            return product

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

@app.delete("/product")
def delete_product(id: int):
    for i, product in enumerate(products):
        if product.id == id:
            return products.pop(i)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")