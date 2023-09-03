from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import config

engine = create_engine(config.DB_URL)
Session = sessionmaker(bind=engine, autoflush=False, autocommit=False)


@contextmanager
def open_session():
    session = Session()
    yield session
    try:
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
