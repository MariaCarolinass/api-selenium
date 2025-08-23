from sqlalchemy.orm import Session
from . import models

def create_dom_file(db: Session, title: str, url: str, month: int, year: int):
    dom_file = models.DomFile(
        title=title,
        url=url,
        publication_month=month,
        publication_year=year
    )
    db.add(dom_file)
    db.commit()
    db.refresh(dom_file)
    return dom_file

def get_dom_files(db: Session, month: int = None, year: int = None):
    query = db.query(models.DomFile)
    if month:
        query = query.filter(models.DomFile.publication_month == month)
    if year:
        query = query.filter(models.DomFile.publication_year == year)
    return query.order_by(models.DomFile.uploaded_at.desc()).all()

def delete_files(db: Session, month: int = None, year: int = None):
    query = db.query(models.DomFile)
    if month:
        query = query.filter(models.DomFile.publication_month == month)
    if year:
        query = query.filter(models.DomFile.publication_year == year)
    query.delete(synchronize_session=False)
    db.commit()