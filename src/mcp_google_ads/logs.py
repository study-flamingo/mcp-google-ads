import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger("mcp_google_ads")

# Add console printing handler for INFO level and above
class ConsolePrintHandler(logging.Handler):
    def emit(self, record):
        if record.levelno >= logging.INFO:
            print(f"[{record.levelname}] {record.getMessage()}")

console_handler = ConsolePrintHandler()
console_handler.setLevel(logging.INFO)
# logger.addHandler(console_handler)