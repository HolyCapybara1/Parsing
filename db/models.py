from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import DeclarativeBase, relationship
from datetime import datetime


class Base(DeclarativeBase):
    pass


class Source(Base):
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)   # DNS, Ситилинк, Regard
    base_url = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    products = relationship("Product", back_populates="source")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    brand = Column(String)
    category = Column(String, nullable=False)
    url = Column(String)
    source_id = Column(Integer, ForeignKey("sources.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    source = relationship("Source", back_populates="products")
    prices = relationship("Price", back_populates="product")
    cluster = relationship("MLCluster", back_populates="product", uselist=False)


class Price(Base):
    __tablename__ = "prices"

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    price = Column(Float, nullable=False)
    rating = Column(Float)
    reviews_count = Column(Integer)
    collected_at = Column(DateTime, default=datetime.utcnow)
    collection_id = Column(Integer, ForeignKey("collections.id"))

    product = relationship("Product", back_populates="prices")


class Collection(Base):
    __tablename__ = "collections"

    id = Column(Integer, primary_key=True)
    started_at = Column(DateTime, default=datetime.utcnow)
    finished_at = Column(DateTime)
    status = Column(String)   # running | success | error
    total_records = Column(Integer, default=0)


class MLCluster(Base):
    __tablename__ = "ml_clusters"

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"), unique=True)
    segment = Column(String)  # Бюджетный | Средний | Премиум
    confidence = Column(Float)
    model_version = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    product = relationship("Product", back_populates="cluster")
