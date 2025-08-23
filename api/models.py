from sqlalchemy import Column, Integer, String, Date, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class DomFile(Base):
    __tablename__ = "dom_files"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    url = Column(String, nullable=False)
    publication_month = Column(Integer, nullable=False)
    publication_year = Column(Integer, nullable=False)
    uploaded_at = Column(Date, server_default=func.current_date())