from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    project_id: str | None = None

    otel_exporter_otlp_endpoint: str | None = None
    # WARNING: 本番環境ではセキュリティ設定を検討する必要があります
    otel_exporter_otlp_insecure: bool = False

    service_name: str = "fastapi-todo-service"
    log_level: str = "INFO"
    environment: str = "dev"
    api_host: str = "localhost"
    api_port: int = 8000

    @property
    def api_base_url(self) -> str:
        return f"http://{self.api_host}:{self.api_port}"

    def is_production(self) -> bool:
        return (
            self.environment.lower() == "prod"
            or self.environment.lower() == "production"
        )

    class Config:
        env_file = ".env"


settings = Settings()
