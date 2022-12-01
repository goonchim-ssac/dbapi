import cv2
import os
import re
import numpy as np
import crud, models, schemas
from fastapi import FastAPI, Depends, File, Response, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from datetime import datetime
from database import SessionLocal, engine
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent # /db
IMAGE_DIR = str(BASE_DIR/"image")

# Create table
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/')
def conn_check():
    return {"Database" : "Created"}

# stock DB INPUT ls_cd ,ls_dt, barcode, ex_dt, ls_ct
@app.post("/stock/", response_model=schemas.Stock)
def create_stock(stock : schemas.Stock, db:Session = Depends(get_db)):
    tb_check = crud.get_stock(db, stock.ls_cd)
    if tb_check:
        raise HTTPException(status_code=400, detail="Stock already registered")
    return crud.create_stock(db, stock)


# recapture save
@app.post("/save_badpicture", response_class=HTMLResponse)
def save_badpicture(file:bytes = File()):
    # YYYY-MM-DD
    current_time = str(datetime.today().date())
    image_name = str(datetime.today())
    image_name = re.sub(r'[.|:]', '', image_name)
    # byte image convert cv2 image
    decoded = cv2.imdecode(np.frombuffer(file, np.uint8), cv2.IMREAD_COLOR)
    # IMAGE_DIR check
    if not os.path.isdir(IMAGE_DIR):
        os.mkdir(IMAGE_DIR)
    # DATE_DIR check
    DATE_DIR = os.path.join(IMAGE_DIR, current_time)
    if not os.path.isdir(DATE_DIR):
        os.mkdir(DATE_DIR)
    # make image
    SAVE_DIR = os.path.join(DATE_DIR, image_name)
    cv2.imwrite(f"{SAVE_DIR}.jpg", decoded)
    return Response('Save picture')