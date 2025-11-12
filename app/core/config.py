from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres:postgres@db:5432/qadb"
    DATABASE_TEST_URL: str = "postgresql://postgres:postgres@db_test:5432/qadb_test"

    model_config = ConfigDict(env_file=".env")

settings = Settings()