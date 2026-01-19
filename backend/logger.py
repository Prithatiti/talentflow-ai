# backend/logger.py

import logging
import sys

# Configure the Logging System
def setup_logging():
    # format: Time [Level] Filename: Message
    log_format = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=[
            # Write to file (with utf-8 to handle special chars/emojis in AI text)
            logging.FileHandler("server_logs.log", encoding='utf-8'),
            # Print to Console
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Create a specific logger for our app
    logger = logging.getLogger("TalentflowAI")
    return logger

# Initialize one instance to be imported elsewhere
logger = setup_logging()