from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str
    app_secret: str
    github_client_id: str
    github_client_secret: str
    github_callback_url: str
    cors_origins: str = 'http://localhost:3000'

    model_config = SettingsConfigDict(
      env_file=".env",
      env_file_encoding="utf-8",
      case_sensitive=False,
    )

settings = Settings() # type: ignore[call-arg]