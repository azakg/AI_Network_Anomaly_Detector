from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "AI Network Anomaly Detector"
    app_env: str = "dev"
    app_host: str = "0.0.0.0"
    app_port: int = 8000

    postgres_host: str = "postgres"
    postgres_port: int = 5432
    postgres_db: str = "anomalydb"
    postgres_user: str = "anomaly"
    postgres_password: str = "anomaly123"

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
