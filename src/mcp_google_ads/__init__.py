from .server import mcp
import logging

logger = logging.getLogger("mcp_google_ads")


def main() -> None:
    try:
        mcp.run()
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        logger.critical(f"❌ Fatal error: {e}")


__all__ = ["mcp"]