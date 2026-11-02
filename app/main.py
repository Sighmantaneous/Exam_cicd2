from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.database import engine, get_db
from app.models import EquipmentDB
from app.schemas import EquipCreate, EquipRead
from app.models import Base

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Equipment loan service")

@app.get("/health")
def health():
    return{"status": "ok"}


@app.post("/api/equipment", response_model=EquipRead, status_code=status.HTTP_201_CREATED)
def add_loan(new_loan: EquipCreate, db: Session=Depends(get_db)):
    db_equip = EquipmentDB(**new_loan.model_dump())
    db.add(db_equip)
    try:
        db.commit()
        db.refresh(db_equip)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Loan already exists",
        )
    return db_equip

@app.get("/api/equipment{id}",response_model=EquipRead, status_code=status.HTTP_200_OK)
def get_loan(id: int, db:Session=Depends(get_db)):
    db_loan = db.get(EquipmentDB,id)
    if db_loan is None:
        raise HTTPException(
            status_code=status.HTTP_404,
            detail="Loan not found"
        )
    return db_loan

@app.delete("/api/equipment/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_loan(id: int, db: Session=Depends(get_db)):
    db_loan = db.get(EquipmentDB,id)
    if db_loan is None:
        raise HTTPException(
            status_code=status.HTTP_404,
            detail="Loan not found"
        )
    db.delete(db_loan)
    db.commit()
    return 0
    

