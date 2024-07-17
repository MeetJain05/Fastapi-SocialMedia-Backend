from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    password_escape: str

    class Config:
        env_file = ".env"

    
settings = Settings()

def modify_password(password: str):

    encoded_password = password.replace("@", "%40")
    return encoded_password