from sqlalchemy import Table, Column, Integer, ForeignKey, String, Text,create_engine
from sqlalchemy.orm import relationship, declarative_base,Session
engine = create_engine(
    "mysql+pymysql://root:Ah03Da11La02@localhost:3306/goods",
    echo=True
)
Base = declarative_base()
feature_keywords = {
    "降噪": ["降噪", "noise cancelling", "ANC"],
    "音質好": ["好音質", "高音質", "高保真", "HD音質"],
    "藍牙": ["藍芽", "藍牙", "Bluetooth"],
    "耳罩式": ["耳罩", "耳罩式"],
    "耳塞式": ["耳塞", "耳塞式", "入耳"],
    "保固長": ["保固", "12個月", "一年", "18個月"],
    "可打遊戲": ["低延遲", "遊戲", "game", "gaming", "延遲低"],
    "續航強": ["長效", "長續航", "電力持久", "電池耐用"]
}

# 中介表
product_features = Table(
    'product_features', Base.metadata,
    Column('product_id', Integer, ForeignKey('products.id'), primary_key=True),
    Column('feature_id', Integer, ForeignKey('features.id'), primary_key=True)
)

class etmallProduct(Base):
    __tablename__ = 'etmall'
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    # 其他欄位：price, link ...
    
    features = relationship("Feature", secondary=product_features, back_populates="products")

class Feature(Base):
    __tablename__ = 'features'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)

    products = relationship("Product", secondary=product_features, back_populates="features")
with Session(engine) as session:
    def get_or_create_feature(session, name):
        feature = session.query(Feature).filter_by(name=name).first()
        if not feature:
            feature = Feature(name=name)
            session.add(feature)
            session.commit()
        return feature

    def tag_product_features(session, product: etmallProduct, feature_keywords: dict):
        name = product.name
        matched_labels = set()

        for label, keywords in feature_keywords.items():
            for kw in keywords:
                if kw.lower() in name.lower():
                    matched_labels.add(label)
                    break

        for label in matched_labels:
            feature = get_or_create_feature(session, label)
            if feature not in product.features:
                product.features.append(feature)

        session.commit()
    def tag_all_products(session, feature_keywords):
        products = session.query(etmallProduct).all()
        for product in products:
            tag_product_features(session, product, feature_keywords)
tag_all_products(session, feature_keywords)