from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    project_id: str | None = None
    otel_exporter_otlp_endpoint: str | None = None
    log_level: str = "INFO"
    environment: str = "dev"

    def is_production(self) -> bool:
        return (
            self.environment.lower() == "prod"
            or self.environment.lower() == "production"
        )

    class Config:
        env_file = ".env"


settings = Settings()
