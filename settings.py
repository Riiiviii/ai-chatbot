import os
from dotenv import load_dotenv

load_dotenv()


class Settings:

    def __init__(self) -> None:
        self.cors_origins: list[str] = list(
            map(str.strip, self._required("CORS_ORIGINS").split(","))
        )
        self.mcp_server_url: str = self._required("MCP_SERVER_URL")

    def _required(self, key: str) -> str:
        value = os.getenv(key)
        if value is None:
            raise RuntimeError(f"{key} is required")
        return value


settings = Settings()
