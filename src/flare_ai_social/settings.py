from pathlib import Path

import structlog
from pydantic_settings import BaseSettings, SettingsConfigDict

logger = structlog.get_logger(__name__)


class Settings(BaseSettings):
    """
    Application settings model that provides configuration for all components.
    """

    # API key for accessing Google's Gemini AI service
    gemini_api_key: str = ""
    # Name of the new tuned model
    tuned_model_name: str = ""
    # Base model to tune upon
    tuning_source_model: str = "models/gemini-1.5-flash-001-tuning"
    # Tuning dataset path
    tuning_dataset_path: Path = (
        Path(__file__).parent.parent / "data" / "training_data.json"
    )
    # Number of epochs to tune for
    tuning_epoch_count: int = 25
    # Batch size
    tuning_batch_size: int = 4
    # Learning rate
    tuning_learning_rate: float = 0.001

    # X/Twitter API credentials (all required for the TwitterBot to function)
    x_bearer_token: str = "AAAAAAAAAAAAAAAAAAAAABVIzwEAAAAASt9qNdPvyVJxY7A9RsO4TWQNQUA%3D7jYSSi0ktd6CZdahBoF0MIzgaBBupMZ8Rx5IpKSD3ioapE2AIp"
    # Required: Twitter API consumer key
    x_api_key: str = "V5Ler0B7qWvmjjfobEGSHqEHe"
    # Required: Twitter API consumer secret
    x_api_key_secret: str = "p3vlwpejUjd0hsgra0AZtVfy9mPLNF8TpigVlPJYDrL9dPmnbp"
    # Required: Twitter API access token
    x_access_token: str = "1745462816327569409-qol4c1VJjfxqhzg6qqJvcZ3HfdIHLI"
    # Required: Twitter API access token secret
    x_access_token_secret: str = "GC4s5albMnvgz8xIue7irGiv4o7ocnkmOI8yBwzsN1YUi"

    # RapidAPI configuration for X/Twitter search (required for the TwitterBot)
    rapidapi_key: str = "aa051db4d4msh65e6144a9545a71p1d8f6bjsn6e687084f61f"
    rapidapi_host: str = "twitter241.p.rapidapi.com"

    # Twitter accounts to monitor (comma-separated list with @ symbols)
    twitter_accounts_to_monitor: str = "@HugoPhilion,@flarenetworks,@Danrocky,$FLR,Flare,$XRP,XRPL"

    # Twitter monitoring interval in seconds
    twitter_polling_interval: int = 60

    # Telegram Bot settings
    # Required for Telegram bot
    telegram_api_token: str = "7299139713:AAEJyYMjdwu5SWeDv2SqF2D7FypirfIC6Cg"
    telegram_allowed_users: str = (
        ""  # Comma-separated list of allowed user IDs (optional)
    )
    telegram_polling_interval: int = 5  # Seconds between checking for updates

    financialmodeling_api_key: str = "pzs0p64Iq4AHbpHq1vNrmRufCpzMrSOc"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

    @property
    def accounts_to_monitor(self) -> list[str]:
        """Parse the comma-separated list of Twitter accounts to monitor."""
        if not self.twitter_accounts_to_monitor:
            return ["@HugoPhilion,@flarenetworks,@Danrocky"]
        return [
            account.strip() for account in self.twitter_accounts_to_monitor.split(",")
        ]

    @property
    def telegram_allowed_user_ids(self) -> list[int]:
        """Parse the comma-separated list of allowed Telegram user IDs."""
        if not self.telegram_allowed_users:
            return []
        try:
            return [
                int(user_id.strip())
                for user_id in self.telegram_allowed_users.split(",")
                if user_id.strip()
            ]
        except ValueError:
            logger.exception(
                "Invalid Telegram user IDs in configuration. User IDs must be integers."
            )
            return []


# Create a global settings instance
settings = Settings()
logger.debug(
    "settings",
    settings=settings.model_dump(
        exclude={"x_api_key_secret",
                 "x_access_token_secret", "telegram_api_token"}
    ),
)
