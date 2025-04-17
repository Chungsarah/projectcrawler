from fastapi import FastAPI, Request,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, select,inspect
from sqlalchemy.orm import declarative_base, Session

app = FastAPI()

# 允許前端跨域請求（重要）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
engine = create_engine(
    "mysql+pymysql://root:Ah03Da11La02@localhost:3306/goods",
    echo=True
)
Base = declarative_base()
class etmallProduct(Base):
    __tablename__ = "etmall"
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    price = Column(String(255))
    link = Column(String(255))
class CoupangProduct(Base):
    __tablename__ = "coupang"
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    price = Column(String(255))
    link = Column(String(255))
class momoProduct(Base):
    __tablename__ = "momo"
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    price = Column(String(255))
    link = Column(String(255))
class orangeProduct(Base):
    __tablename__ = "orange"
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    price = Column(String(255))
    link = Column(String(255))
class pchomeProduct(Base):
    __tablename__ = "pchome"
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    price = Column(String(255))
    link = Column(String(255))
class rutenProduct(Base):
    __tablename__ = "ruten"
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    price = Column(String(255))
    link = Column(String(255))



class SearchRequest(BaseModel):
    keyword: str


@app.post("/search")
def search_products(req: SearchRequest):
    keyword = req.keyword
    results = []

    with Session(engine) as session:
        def search(model):
            return session.query(model).filter(model.name.like(f"%{keyword}%")).all()

        tables = [
            (etmallProduct, "etmall"),
            (momoProduct, "momo"),
            (CoupangProduct,"coupang"),
            (pchomeProduct,"pchome"),
            (rutenProduct,"ruten")
            # 加入其他資料表：PchomeProduct, YahooProduct, etc...
        ]

        for model, source in tables:
            products = search(model)
            for p in products:
                results.append({
                    "name": p.name,
                    "price": p.price,
                    "link": p.link,
                    "source": source
                })

    return {"products": results}
