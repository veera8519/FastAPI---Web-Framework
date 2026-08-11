
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database import engine, get_db
import database_models
from models import Product, ProductCreate, ProductUpdate

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

database_models.Base.metadata.create_all(bind=engine)


@app.get("/")
def greet():
    return ("welcome to code")

@app.get("/products", response_model=list[Product])
def get_all_products(db: Session = Depends(get_db)):
    return db.query(database_models.Product).all()


@app.get("/products/{id}", response_model=Product)
def get_product_by_id(id: int, db: Session = Depends(get_db)):
    product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if product:
        return product

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

@app.post("/products", response_model=Product, status_code=status.HTTP_201_CREATED)
def add_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = database_models.Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.put("/products/{id}", response_model=Product)
def update_product(id: int, product: ProductUpdate, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        for field, value in product.model_dump().items():
            setattr(db_product, field, value)
        db.commit()
        db.refresh(db_product)
        return db_product

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

@app.delete("/products/{id}", response_model=Product)
def delete_product(id: int, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return db_product

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")