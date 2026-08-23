from sqlalchemy import create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column


class Base(DeclarativeBase):
    pass


class Product(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    max_temperature: Mapped[float]
    density: Mapped[float]
    application: Mapped[str]


def create_sample_db(db_path: str='./test_004/product.db') -> None:
    """
    サンプルデータを sqlite に格納する関数。
    """

    engine = create_engine(f'sqlite:///{db_path}', echo=True)

    # テーブル作成
    Base.metadata.create_all(engine)

    # データ登録
    products = [
        Product(
            name='製品A',
            max_temperature=120,
            density=1.1,
            application='食品包装',
        ),
        Product(
            name='製品B',
            max_temperature=180,
            density=1.3,
            application='自動車部品',
        ),
        Product(
            name='製品C',
            max_temperature=150,
            density=0.9,
            application='食品容器',
        ),
        Product(
            name='製品D',
            max_temperature=200,
            density=1.5,
            application='化学プラント',
        ),
    ]

    with Session(engine) as session:
        session.add_all(products)
        session.commit()


def search_products(
    db_path: str='./test_004/product.db',
    *,
    max_temperature: float | None = None,
    density: float | None = None,
    application: str | None = None,
) -> list[dict]:
    """
    製品データベースを検索する。

    Args:
        max_temperature:
            必要な最低耐熱温度。
            指定した値以上の製品を検索する。
            例: 130 を指定すると max_temperature >= 130。

        density:
            許容する最大密度。
            指定した値以下の製品を検索する。
            例: 1.0 を指定すると density <= 1.0。

        application:
            製品の用途。
            指定した場合、その用途と完全一致する製品を検索する。
    """
    
    engine = create_engine(f'sqlite:///{db_path}', echo=False)
    with Session(engine) as session:
        stmt = select(Product)
    
        if max_temperature is not None:
            stmt = stmt.where(Product.max_temperature >= max_temperature)
    
        if density is not None:
            stmt = stmt.where(Product.density <= density)
    
        if application is not None:
            stmt = stmt.where(Product.application == application)

        products = session.scalars(stmt).all()
        return [{
            'id': product.id,
            'name': product.name,
            'max_temperature': product.max_temperature,
            'density': product.density,
            'application': product.application,
        } for product in products]