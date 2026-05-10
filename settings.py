import os
from dotenv import load_dotenv

load_dotenv(override=True)


class Settings:

    def __init__(self) -> None:
        self.cors_origins: list[str] = os.getenv(
            "CORS_ORIGINS", "http://localhost:5173"
        ).split(",")
        self.mcp_server_url: str = os.getenv(
            "MCP_SERVER_URL", "http://localhost:8001/sse"
        )


settings = Settings()
