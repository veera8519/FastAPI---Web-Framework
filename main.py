
from fastapi import FastAPI

from models import Product

app=FastAPI()

@app.get("/")
def greet():
    return ("welcome to code")

products=[
    Product(1,"Phone","budget phone",99,2),
    Product(2,"laptop","budget laptop",100,3),
    Product(3,"car","budget car",99,4)
]


@app.get("/products")
def get_all_products():
    return products