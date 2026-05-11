from agents import Agent
from pathlib import Path


class GraduateAgent:
    MODEL = "gpt-4o-mini"

    def __init__(self) -> None:
        self.instructions: str = (Path(__file__).parent / "prompt.txt").read_text()

    def create_agent(self, mcp_servers):
        return Agent(
            name="graduate-agent",
            instructions=self.instructions,
            model=self.MODEL,
            mcp_servers=mcp_servers,
        )
