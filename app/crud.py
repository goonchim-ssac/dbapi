from sqlalchemy.orm import Session
import models, schemas

# stock table insert
def create_stock(db : Session, stock : schemas.Stock):
    db_stock = models.Stock(
        ls_cd = stock.ls_cd,
        ls_dt = stock.ls_dt,
        barcode = stock.barcode,
        ex_dt = stock.ex_dt,
        ls_ct = stock.ls_ct
        )
    db.add(db_stock)
    db.commit()
    db.refresh(db_stock)
    return db_stock


# stock table select
def get_stock(db : Session, ls_cd = str):
    return db.query(models.Stock).filter(models.Stock.ls_cd == ls_cd).first()
