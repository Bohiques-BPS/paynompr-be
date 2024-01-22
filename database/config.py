from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase

# "postgresql+psycopg2://postgres:nblIF4Wop2eGfYYJ@db.ltyhskwmttkrernknvvr.supabase.co:5432/postgres"

DATABASE_URL = URL.create(
    drivername="postgresql+psycopg2",
    username="postgres",
    password="nblIF4Wop2eGfYYJ",
    host="db.ltyhskwmttkrernknvvr.supabase.co",
    database="postgres",
    port=5432,
)


engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = Session()


class Base(DeclarativeBase):
    pass


def init_db():
    Base.metadata.create_all(bind=engine)
