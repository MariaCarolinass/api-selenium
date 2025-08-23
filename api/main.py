from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from . import models, database, crud

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Diário Oficial de Natal API")

@app.get("/")
def read_root(db: Session = Depends(database.get_db)):
    files = crud.get_dom_files(db)
    return [{"id": f.id, "title": f.title, "url": f.url,
             "month": f.publication_month, "year": f.publication_year,
             "uploaded_at": f.uploaded_at} for f in files]

@app.get("/files/")
def list_files(month: int = None, year: int = None, db: Session = Depends(database.get_db)):
    files = crud.get_dom_files(db, month=month, year=year)
    return [{"id": f.id, "title": f.title, "url": f.url,
             "month": f.publication_month, "year": f.publication_year,
             "uploaded_at": f.uploaded_at} for f in files]

@app.delete("/files/")
def delete_files(month: int = None, year: int = None, db: Session = Depends(database.get_db)):
    crud.delete_files(db, month=month, year=year)
    return {"message": "Arquivos deletados com sucesso!"}