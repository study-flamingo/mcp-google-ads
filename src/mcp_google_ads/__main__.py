"""Google Ads MCP Server: Main entry"""
import sys
from .server import mcp
from .logs import logger

def main() -> None:
    try:
        logger.info("🚀 Starting Google Ads MCP Server...")
        mcp.run()
    except Exception as e:
        logger.critical(f"❌ Application startup failed: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
