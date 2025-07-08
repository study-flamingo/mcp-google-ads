"""Google Ads MCP Server: Main entry"""
from .server import mcp
import logging

logger = logging.getLogger("mcp_google_ads")
logging.basicConfig(level=logging.DEBUG)



def main() -> None:
    try:
        mcp.run()
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        logger.critical(f"❌ Fatal error: {e}")


if __name__ == "__main__":
    main()
