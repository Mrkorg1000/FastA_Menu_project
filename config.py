from pydantic import BaseSettings


class Settings(BaseSettings):
    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_pass: str

    db_host_test: str
    db_port_test: int
    db_name_test: str
    db_user_test: str
    db_pass_test: str

    class Config:
        env_file = ".env"


settings = Settings()
