from pydantic import BaseSettings


class Settings(BaseSettings):
    path: int
    database_username: str = "postgres"
    secret_key: str = "2478r3iwwfwhf27"


settings = Settings()