from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config.settings import DATABASE_PATH
from database.models import Base


# --------------------------------------------------
# DATABASE URL
# --------------------------------------------------

DATABASE_URL = (
    f"sqlite:///{DATABASE_PATH}"
)


# --------------------------------------------------
# DATABASE ENGINE
# --------------------------------------------------

engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False
    }
)


# --------------------------------------------------
# SESSION
# --------------------------------------------------

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)


# --------------------------------------------------
# CREATE TABLES
# --------------------------------------------------

def initialize_database():

    Base.metadata.create_all(
        bind=engine
    )

    print(
        "\nDatabase initialized successfully."
    )

    print(
        f"Database location:\n{DATABASE_PATH}"
    )


# --------------------------------------------------
# GET DATABASE SESSION
# --------------------------------------------------

def get_session():

    return SessionLocal()


# --------------------------------------------------
# TEST
# --------------------------------------------------

if __name__ == "__main__":

    initialize_database()

    session = get_session()

    print(
        "Database connection successful."
    )

    session.close()