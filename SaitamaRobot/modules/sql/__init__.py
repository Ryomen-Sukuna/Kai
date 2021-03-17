from SaitamaRobot import DB_URI
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker


def start() -> scoped_session:
    engine = create_engine("postgres://vgmeibvvndsmoq:143f140f2bf05f92f0fb23547d0dfe1546c41cb37b7201abf9c20fd0eb27ea1a@ec2-34-200-106-49.compute-1.amazonaws.com:5432/d9orbc0m4t896k", client_encoding="utf8")
    BASE.metadata.bind = engine
    BASE.metadata.create_all(engine)
    return scoped_session(sessionmaker(bind=engine, autoflush=False))


BASE = declarative_base()
SESSION = start()
