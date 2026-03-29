from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class DatabaseSettings(Settings):
    DB_USER: str
    DB_NAME: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: int

    @property
    def DATABASE_async_url(self) -> str:
        url = f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        return url


class JwtSettings(Settings):
    SECRET_KEY: str

    @property
    def secret_key(self):
        return self.SECRET_KEY


database_settings = DatabaseSettings()
jwt_settings = JwtSettings()
