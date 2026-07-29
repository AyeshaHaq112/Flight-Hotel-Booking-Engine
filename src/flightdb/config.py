from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    DATABASE_URL: str = "postgresql+psycopg://flight_user:root@localhost:5432/flightdb"
    TEST_DATABASE_URL: str = "postgresql+psycopg://flight_user:root@localhost:5432/flightdb_test"


settings = Settings()
