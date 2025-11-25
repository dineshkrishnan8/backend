# # from sqlalchemy import create_engine
# # from sqlalchemy.orm import sessionmaker, declarative_base
# # from .config import settings

# # # Build DSN
# # # connection_string = (
# # #     f"mssql+pyodbc://{settings.DB_USER}:{settings.DB_PASSWORD}"
# # #     f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
# # #     f"?driver={settings.DB_DRIVER.replace(' ', '+')}"
# # # )

# # connection_string = (
# #     f"mysql+pymysql://{settings.DB_USER}:{settings.DB_PASSWORD}"
# #     f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
# # )


# # engine = create_engine(connection_string)
# # SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# # Base = declarative_base()

# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker, declarative_base
# from app.config import settings

# connection_string = (
#     f"mysql+pymysql://{settings.DB_USER}:{settings.DB_PASSWORD}"
#     f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
# )

# engine = create_engine(connection_string)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings
import urllib

# Build ODBC connection string
params = urllib.parse.quote_plus(
    f"Driver={{{settings.DB_ODBC_DRIVER}}};"
    f"Server={settings.DB_HOST},{settings.DB_PORT};"
    f"Database={settings.DB_NAME};"
    f"Trusted_Connection=yes;"
)

connection_string = f"mssql+pyodbc:///?odbc_connect={params}"

engine = create_engine(connection_string, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
