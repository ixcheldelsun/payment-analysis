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
    
    SWAGGER_TEMPLATE: dict = {
            "swagger": "2.0",
            "info": {
                "title": "Payments API",
                "description": "Payments APi focused on the creation and retrieval of payments and users in the DB, as the analysis of the payments of a specific user.",
                "contact": {
                    "responsibleDeveloper": "Ixchel Garcia :)",
                    "email": "ixcheldelsolga@gmail.com",
                },
                "version": "1.0.0"
            },
            "schemes": [
                "http",
            ]
        }

    

settings = Config()