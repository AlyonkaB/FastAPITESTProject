from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from db.engine import SessionLocal
from db.models import PackagingType

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"message": "Hello Cheeses"}


@app.get("/cheese_types/", response_model=list[schemas.CheeseTypeList])
def read_cheese_types(
        db: Session = Depends(get_db)
):
    return crud.get_all_cheese_type(db)


@app.post("/cheese_types/", response_model=schemas.CheeseTypeList)
def create_cheese_type(
        cheese_type: schemas.CheeseTypeCreate,
        db: Session = Depends(get_db),
):

    db_cheese_type = crud.get_cheese_type_by_name(db=db, name=cheese_type.name)
    if db_cheese_type:
        raise HTTPException(
            status_code=400,
            detail="Such name for CheeseType already exists"
        )

    return crud.create_cheese_type(db=db, cheese_type=cheese_type)


@app.get("/cheese/", response_model=list[schemas.CheeseList])
def read_all_cheese(
        db: Session = Depends(get_db),
        packaging_type: PackagingType | None = None,
        cheese_type: str | None = None
):
    return crud.get_all_cheese(
        db=db,
        packaging_type=packaging_type,
        cheese_type=cheese_type
    )


@app.get("/cheese/{cheese_id}", response_model=schemas.CheeseList)
def read_single_cheese(
        cheese_id: int,
        db: Session = Depends(get_db)
):
    db_cheese = crud.get_cheese(db=db, cheese_id=cheese_id)

    if db_cheese is None:
        raise HTTPException(
            status_code=404,
            detail="Cheese not found"
        )

    return db_cheese


@app.post("/cheese/", response_model=schemas.CheeseList)
def create_cheese(
        cheese: schemas.CheeseCreate,
        db: Session = Depends(get_db),
):
    return crud.create_cheese(db=db, cheese=cheese)
