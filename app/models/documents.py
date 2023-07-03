from sqlalchemy import Column, Integer, String, TIMESTAMP

from app.db.base_class import Base


class BaseDocument:
    id = Column(Integer, primary_key=True)
    start_date = Column(TIMESTAMP, nullable=False)
    exp_date = Column(TIMESTAMP, nullable=False)


class DriverLicense(Base, BaseDocument):
    ...


class Insurance(Base, BaseDocument):
    insurer = Column(String(150), nullable=False)


class Document(Base, BaseDocument):
    title = Column(String(150), nullable=False)
