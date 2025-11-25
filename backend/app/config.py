# from pydantic_settings import BaseSettings

# class Settings(BaseSettings):
#     DB_USER: str
#     DB_PASSWORD: str
#     DB_HOST: str
#     DB_PORT: int
#     DB_NAME: str
#     DB_DRIVER: str

#     class Config:
#         env_file = ".env"

# settings = Settings()


from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_DRIVER: str
    DB_ODBC_DRIVER: str   # <-- ADD THIS LINE

    class Config:
        env_file = ".env"

settings = Settings()
