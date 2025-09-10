from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from decimal import Decimal

from .config import settings
from .database import engine
from .models import Base
from . import crud, schemas
from .deps import get_db

app = FastAPI(title="Book Order API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS if settings.ALLOWED_ORIGINS != ["*"] else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Auto create tables on first run (for simple setups)
Base.metadata.create_all(bind=engine)

# Built-in book list (can be moved to DB later)
BOOK_PRICES = {
    "python人工智慧": Decimal("450.00"),
    "python基礎學習課程": Decimal("300.00"),
}

@app.get("/healthz")
def healthz():
    return {"ok": True}

@app.get("/books")
def list_books():
    return BOOK_PRICES

@app.get("/orders", response_model=list[schemas.OrderRead])
def list_orders(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    return crud.list_orders(db, skip=skip, limit=limit)

@app.post("/orders", response_model=schemas.OrderRead, status_code=201)
def create_order(payload: schemas.OrderCreate, db: Session = Depends(get_db)):
    if payload.book_title in BOOK_PRICES:
        payload.unit_price = BOOK_PRICES[payload.book_title]
    return crud.create_order(db, payload)

@app.patch("/orders/{order_id}", response_model=schemas.OrderRead)
def update_order(order_id: int, payload: schemas.OrderUpdate, db: Session = Depends(get_db)):
    obj = crud.update_order(db, order_id, payload)
    if not obj:
        raise HTTPException(status_code=404, detail="Order not found")
    return obj

@app.delete("/orders/{order_id}", status_code=204)
def delete_order(order_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_order(db, order_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Order not found")
    return
