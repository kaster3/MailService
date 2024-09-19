import uvicorn
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel


class RunConfig:
    app: str = "main:main_app"
    host: str = "0.0.0.0"
    port: int = 8001
    reload: bool = True

    def run_app(self):
        uvicorn.run(
            self.app,
            host=self.host,
            port=self.port,
            reload=self.reload,
        )


class EmailConfig(BaseModel):
    from_email: str
    smtp_server: str
    smtp_port: int  # 465 SSL, 587 TLS
    smtp_password: str


class TopicNames(BaseModel):
    logged_in_notification: str
    email_callback_topic: str = "callback_email_topic"
    verify_email: str = "verify_email_topic"


class BrokerConfig(BaseModel):
    url: str
    topics: TopicNames


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env.template", ".env"),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="FASTAPI__"
    )
    email: EmailConfig
    broker_config: BrokerConfig


def get_settings() -> Settings:
    print("settings")
    return Settings()
