import os
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
                             QPushButton, QFrame, QSpacerItem, QSizePolicy)
from PyQt6.QtCore import Qt, pyqtSignal, QSize, QTimer
from PyQt6.QtGui import QIcon, QPixmap

from app.ui.widgets.animated_button import AnimatedButton
from app.ui.widgets.animated_line_edit import AnimatedLineEdit

import logging

logger = logging.getLogger(__name__)

class RegisterScreen(QWidget):
    # Navigation signals
    navigate_to_login = pyqtSignal()
    
    def __init__(self, supabase_service):
        super().__init__()
        self.supabase_service = supabase_service
        
        # Connect to auth error signal
        self.supabase_service.auth_error.connect(self.on_auth_error)
        
        # Setup UI
        self.setup_ui()
        logger.info("RegisterScreen initialized")
    
    def setup_ui(self):
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create content frame
        content_frame = QFrame()
        content_frame.setObjectName("registerContentFrame")
        content_frame.setStyleSheet("""
            #registerContentFrame {
                background-color: transparent;
                border-radius: 10px;
            }
        """)
        
        # Content layout
        content_layout = QVBoxLayout(content_frame)
        content_layout.setContentsMargins(40, 40, 40, 40)
        content_layout.setSpacing(20)
        
        # Logo and title
        logo_layout = QHBoxLayout()
        logo_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Logo image if available
        logo_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), 
                               'app', 'assets', 'images', 'logo.png')
        if os.path.exists(logo_path):
            logo_label = QLabel()
            logo_pixmap = QPixmap(logo_path)
            logo_label.setPixmap(logo_pixmap.scaled(QSize(80, 80), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
            logo_layout.addWidget(logo_label)
        
        # Title
        title_label = QLabel("Create Account")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #ffffff;
            margin-top: 10px;
            margin-bottom: 20px;
        """)
        
        # Form layout
        form_layout = QVBoxLayout()
        form_layout.setSpacing(15)
        
        # Username field
        self.username_edit = AnimatedLineEdit()
        self.username_edit.setPlaceholderText("Username")
        self.username_edit.setMinimumHeight(50)
        
        # Email field
        self.email_edit = AnimatedLineEdit()
        self.email_edit.setPlaceholderText("Email")
        self.email_edit.setMinimumHeight(50)
        
        # Password field
        self.password_edit = AnimatedLineEdit()
        self.password_edit.setPlaceholderText("Password")
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_edit.setMinimumHeight(50)
        
        # Confirm password field
        self.confirm_password_edit = AnimatedLineEdit()
        self.confirm_password_edit.setPlaceholderText("Confirm Password")
        self.confirm_password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirm_password_edit.setMinimumHeight(50)
        
        # Register button
        self.register_button = AnimatedButton("Register")
        self.register_button.setMinimumHeight(50)
        self.register_button.clicked.connect(self.on_register_clicked)
        
        # Login link
        login_layout = QHBoxLayout()
        login_layout.setContentsMargins(0, 20, 0, 0)
        
        login_label = QLabel("Already have an account?")
        login_label.setStyleSheet("color: #cccccc; font-size: 14px;")
        
        self.login_link = QLabel("Login")
        self.login_link.setStyleSheet("""
            color: #3a86ff;
            font-size: 14px;
            font-weight: bold;
            text-decoration: none;
            margin-left: 5px;
        """)
        self.login_link.setCursor(Qt.CursorShape.PointingHandCursor)
        self.login_link.mousePressEvent = self.on_login_clicked
        
        login_layout.addStretch()
        login_layout.addWidget(login_label)
        login_layout.addWidget(self.login_link)
        login_layout.addStretch()
        
        # Error message
        self.error_label = QLabel()
        self.error_label.setStyleSheet("""
            color: #ff3333;
            font-size: 14px;
            min-height: 20px;
        """)
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.error_label.setVisible(False)
        
        # Add widgets to form layout
        form_layout.addWidget(self.username_edit)
        form_layout.addWidget(self.email_edit)
        form_layout.addWidget(self.password_edit)
        form_layout.addWidget(self.confirm_password_edit)
        form_layout.addWidget(self.register_button)
        form_layout.addWidget(self.error_label)
        form_layout.addLayout(login_layout)
        
        # Add widgets to content layout
        content_layout.addLayout(logo_layout)
        content_layout.addWidget(title_label)
        content_layout.addLayout(form_layout)
        
        # Add content frame to main layout
        main_layout.addWidget(content_frame)
        
        # Set layout
        self.setLayout(main_layout)
        
        # Set stylesheet
        self.setStyleSheet("""
            QWidget {
                background-color: transparent;
                color: #ffffff;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
        """)
    
    def on_register_clicked(self):
        """
        Handle register button click
        """
        # Get form data
        username = self.username_edit.text()
        email = self.email_edit.text()
        password = self.password_edit.text()
        confirm_password = self.confirm_password_edit.text()
        
        # Validate input
        if not username or not email or not password or not confirm_password:
            self.show_error("Please fill in all fields")
            return
        
        if password != confirm_password:
            self.show_error("Passwords do not match")
            return
        
        # Register with Supabase
        logger.info(f"Attempting to register user: {email}")
        self.register_button.start_loading()
        success = self.supabase_service.sign_up(email, password, username)
        self.register_button.stop_loading()
        
        if not success:
            # Error is handled by on_auth_error
            pass
    
    def on_login_clicked(self, event):
        """
        Handle login link click
        """
        logger.info("Navigating to login screen")
        self.navigate_to_login.emit()
    
    def on_auth_error(self, error_message):
        """
        Handle authentication error
        """
        self.show_error(error_message)
        logger.warning(f"Authentication error: {error_message}")
    
    def show_error(self, message):
        """
        Show error message
        """
        self.error_label.setText(message)
        self.error_label.setVisible(True)
        logger.error(f"Displayed error message: {message}")
        
        # Hide error after 5 seconds
        QTimer.singleShot(5000, lambda: self.error_label.setVisible(False))