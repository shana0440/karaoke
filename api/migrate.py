from db import Base, engine

def migrate_database():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    migrate_database()
