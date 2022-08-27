from pydantic import BaseSettings


class Settings(BaseSettings): # pydantic is not case sensitive
    database_hostname: str # pydantic tries to typecast into specified datatype
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"


settings = Settings()