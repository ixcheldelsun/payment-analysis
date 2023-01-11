from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()

class Config(BaseSettings):
    MYSQL_HOST: str
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_DB: str
    MYSQL_PORT: int
    
    MAIL_SERVER: str = "smtp.gmail.com"
    MAIL_PORT: int = 465
    MAIL_USERNAME: str 
    MAIL_PASSWORD: str 
    MAIL_USE_TLS: bool = False
    MAIL_USE_SSL: bool = True
    

settings = Config()