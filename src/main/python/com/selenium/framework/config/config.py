"""
Test Configuration Module
Contains all configuration settings for SwagLabs test automation.
"""
import os
from pathlib import Path
from typing import Dict, Any


class Config:
    """Base configuration class with common settings."""

    # Project paths
    BASE_DIR = Path(__file__).parent
    TEST_DATA_DIR = BASE_DIR / "test_data"
    REPORTS_DIR = BASE_DIR / "reports"
    SCREENSHOTS_DIR = BASE_DIR / "screenshots"

    # Application URLs
    BASE_URL = "https://www.saucedemo.com/"

    # Test credentials
    DEFAULT_USERNAME = "standard_user"
    DEFAULT_PASSWORD = "secret_sauce"

    # Additional test users
    TEST_USERS = {
        "standard": {
            "username": "standard_user",
            "password": "secret_sauce"
        },
        "locked_out": {
            "username": "locked_out_user",
            "password": "secret_sauce"
        },
        "problem": {
            "username": "problem_user",
            "password": "secret_sauce"
        },
        "performance_glitch": {
            "username": "performance_glitch_user",
            "password": "secret_sauce"
        }
    }

    # WebDriver settings
    BROWSER = os.getenv("BROWSER", "chrome")  # chrome, firefox, edge
    HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
    IMPLICIT_WAIT = 10  # seconds
    EXPLICIT_WAIT = 20  # seconds
    PAGE_LOAD_TIMEOUT = 30  # seconds
    

    # Screenshot settings
    SCREENSHOT_ON_FAILURE = True
    SCREENSHOT_FORMAT = "png"

    # Logging settings
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = REPORTS_DIR / "test_execution.log"

    # Retry settings
    MAX_RETRY_ATTEMPTS = 3
    RETRY_DELAY = 2  # seconds

    @classmethod
    def get_user_credentials(cls, user_type: str = "standard") -> Dict[str, str]:
        """
        Get credentials for a specific user type.

        Args:
            user_type: Type of user (standard, locked_out, problem, performance_glitch)

        Returns:
            Dictionary containing username and password
        """
        return cls.TEST_USERS.get(user_type, cls.TEST_USERS["standard"])

    @classmethod
    def ensure_directories(cls) -> None:
        """Create necessary directories if they don't exist."""
        for directory in [cls.TEST_DATA_DIR, cls.REPORTS_DIR, cls.SCREENSHOTS_DIR]:
            directory.mkdir(parents=True, exist_ok=True)


class DevelopmentConfig(Config):
    """Configuration for development environment."""
    DEBUG = True
    LOG_LEVEL = "DEBUG"


class StagingConfig(Config):
    """Configuration for staging environment."""
    BASE_URL = os.getenv("STAGING_URL", "https://staging.saucedemo.com/")
    DEBUG = False


class ProductionConfig(Config):
    """Configuration for production environment."""
    BASE_URL = os.getenv("PROD_URL", "https://www.saucedemo.com/")
    DEBUG = False
    SCREENSHOT_ON_FAILURE = True


# Environment configuration mapping
config_by_name = {
    "development": DevelopmentConfig,
    "staging": StagingConfig,
    "production": ProductionConfig,
    "default": Config
}

# Get current environment from environment variable
current_env = os.getenv("TEST_ENV", "default")
config = config_by_name.get(current_env, Config)

# Ensure required directories exist
config.ensure_directories()
