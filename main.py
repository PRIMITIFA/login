import sys
import os
import logging
from dotenv import load_dotenv
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFontDatabase

from app.ui.main_window import MainWindow
from app.utils.config import load_config
from app.utils.logging_config import setup_logging

def main():
    # Set up logging
    setup_logging()
    logger = logging.getLogger('cs2_tool_logger')
    logger.info('Application starting...')
    
    # Load environment variables
    load_dotenv()
    logger.info('Environment variables loaded.')
    
    # Initialize application
    app = QApplication(sys.argv)
    logger.info('QApplication initialized.')
    
    # Load fonts
    fonts_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app', 'assets', 'fonts')
    if os.path.exists(fonts_dir):
        for font_file in os.listdir(fonts_dir):
            if font_file.endswith('.ttf'):
                QFontDatabase.addApplicationFont(os.path.join(fonts_dir, font_file))
        logger.info('Fonts loaded.')
    
    # Load configuration
    config = load_config()
    logger.info('Configuration loaded.')
    
    # Create and show main window
    window = MainWindow(config)
    window.show()
    logger.info('Main window shown.')
    
    # Start application event loop
    sys.exit(app.exec())

if __name__ == "__main__":
    main()