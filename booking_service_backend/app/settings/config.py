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


class RedisSettings(Settings):
    DB_HOST: str

    @property
    def REDIS_url(self) -> str:
        return f"redis://{self.DB_HOST}:6379/0"


class BotSettings(Settings):
    BOT_TOKEN: str
    BOT_PORT: int
    BOT_HOST: str
    EXTERNAL_REQUEST_PATH: str
    WEBHOOK_PATH: str

    @property
    def TOKEN(self) -> str:
        return self.BOT_TOKEN

    @property
    def PORT(self) -> int:
        return self.BOT_PORT
    
    @property
    def HOST(self) -> str:
        return self.BOT_HOST
    
    @property
    def EXT_REQ_PATH(self) -> str:
        return self.EXTERNAL_REQUEST_PATH

    @property
    def WEBH_PATH(self) -> str:
        return self.WEBHOOK_PATH



class NgrokSettings(Settings):
    NGROK_AUTHTOKEN: str

    @property
    def NGROK_TOKEN(self) -> str:
        return self.NGROK_AUTHTOKEN
    


database_settings = DatabaseSettings()
jwt_settings = JwtSettings()
redis_settings = RedisSettings()
bot_settings = BotSettings()
ngrok_settings = NgrokSettings()
