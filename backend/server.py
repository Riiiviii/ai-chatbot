from mcp.server.fastmcp import FastMCP
from enum import Enum


class ResumeSection(Enum):
    EXPERIENCE = "experience"
    SKILLS = "skills"
    GITHUB = "github"


mcp = FastMCP("resume-mcp-server")


@mcp.tool()
def get_experience():
    """Get personal work experience"""


if __name__ == "__main__":
    mcp.run()
