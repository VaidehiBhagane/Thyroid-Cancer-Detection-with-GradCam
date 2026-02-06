import logging
import os

def configure_logging():
    # --------------------------------------------------
    # Configure Logging
    # --------------------------------------------------
    if not os.path.exists('logs'):
        os.makedirs('logs')

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/app.log'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

# Create a default logger instance for imports if needed, 
# although calling configure_logging() is preferred in the main entry point.
# But `main.py` used `logger = logging.getLogger(__name__)` at module level.
# To keep behavior similar:
logger = logging.getLogger(__name__)
