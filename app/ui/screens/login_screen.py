import os
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
                             QPushButton, QCheckBox, QFrame, QSpacerItem, QSizePolicy)
from PyQt6.QtCore import Qt, pyqtSignal, QSize, QPropertyAnimation, QEasingCurve, QTimer
from PyQt6.QtGui import QIcon, QPixmap, QColor, QPalette, QFont

from app.ui.widgets.animated_button import AnimatedButton
from app.ui.widgets.oauth_button import OAuthButton
from app.ui.widgets.animated_line_edit import AnimatedLineEdit

import logging

logger = logging.getLogger(__name__)

class LoginScreen(QWidget):
    # Navigation signals
    navigate_to_register = pyqtSignal()
    navigate_to_forgot_password = pyqtSignal()
    
    def __init__(self, supabase_service):
        super().__init__()
        self.supabase_service = supabase_service
        
        # Connect to auth error signal
        self.supabase_service.auth_error.connect(self.on_auth_error)
        
        # Setup UI
        self.setup_ui()
        logger.info("LoginScreen initialized")
    
    def setup_ui(self):
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)  # No margins to remove black space
        main_layout.setSpacing(0)
        
        # Create content frame
        content_frame = QFrame()
        content_frame.setObjectName("loginContentFrame")
        content_frame.setStyleSheet("""
            #loginContentFrame {
                background-color: transparent;
                border-radius: 15px;
                border: none;
            }
        """)
        
        # Content layout
        content_layout = QVBoxLayout(content_frame)
        content_layout.setContentsMargins(40, 40, 40, 40)  # Increased padding for bigger appearance
        content_layout.setSpacing(20)  # More spacing between elements
        
        # Logo and title
        logo_layout = QHBoxLayout()
        logo_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Logo image if available
        logo_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), 
                               'app', 'assets', 'images', 'logo.png')
        if os.path.exists(logo_path):
            logo_label = QLabel()
            logo_pixmap = QPixmap(logo_path)
            logo_label.setPixmap(logo_pixmap.scaled(QSize(80, 80), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))  # Smaller logo
            logo_layout.addWidget(logo_label)
        
        # Title
        title_label = QLabel("CS2 Tool Login")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #ffffff;
            margin-top: 10px;
            margin-bottom: 15px;
            text-transform: uppercase;
            letter-spacing: 1px;
        """)
        
        # Form layout
        form_layout = QVBoxLayout()
        form_layout.setSpacing(15)
        
        # Email field
        self.email_edit = AnimatedLineEdit()
        self.email_edit.setPlaceholderText("Email")
        self.email_edit.setMinimumHeight(50)  # Bigger input field
        self.email_edit.setStyleSheet("""
            QLineEdit {
                background-color: transparent;
                border: 2px solid #333333;
                border-radius: 10px;
                padding: 10px 20px;
                color: #ffffff;
                font-size: 15px;
                margin-bottom: 5px;
            }
            QLineEdit:focus {
                border: 2px solid #3a86ff;
                background-color: #2a2a2a;
            }
        """)
        
        # Password field
        self.password_edit = AnimatedLineEdit()
        self.password_edit.setPlaceholderText("Password")
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_edit.setMinimumHeight(50)  # Bigger input field
        self.password_edit.setStyleSheet("""
            QLineEdit {
                background-color: transparent;
                border: 2px solid #333333;
                border-radius: 10px;
                padding: 10px 20px;
                color: #ffffff;
                font-size: 15px;
                margin-bottom: 5px;
            }
            QLineEdit:focus {
                border: 2px solid #3a86ff;
                background-color: #2a2a2a;
            }
        """)
        
        # Remember me checkbox
        remember_layout = QHBoxLayout()
        self.remember_checkbox = QCheckBox("Remember me")
        self.remember_checkbox.setStyleSheet("""
            QCheckBox {
                color: #cccccc;
                font-size: 15px;
                margin-top: 5px;
                margin-bottom: 5px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border-radius: 5px;
                border: 2px solid #555555;
            }
            QCheckBox::indicator:checked {
                background-color: #3a86ff;
                border: 2px solid #3a86ff;
                image: url(app/assets/icons/checkmark.svg);
            }
            QCheckBox::indicator:hover {
                border: 2px solid #4a96ff;
            }
        """)
        remember_layout.addWidget(self.remember_checkbox)
        remember_layout.addStretch()
        
        self.forgot_password_link = QLabel("Forgot Password?")
        self.forgot_password_link.setStyleSheet("""
            color: #3a86ff;
            font-size: 15px;
            text-decoration: none;
        """)
        self.forgot_password_link.setCursor(Qt.CursorShape.PointingHandCursor)
        self.forgot_password_link.mousePressEvent = self.on_forgot_password_clicked
        remember_layout.addWidget(self.forgot_password_link)
        
        # Login button
        self.login_button = AnimatedButton("LOGIN")
        self.login_button.setMinimumHeight(50)  # Bigger button
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: #3a86ff;
                color: white;
                border-radius: 10px;
                font-size: 16px;
                font-weight: bold;
                letter-spacing: 2px;
                text-transform: uppercase;
            }
            QPushButton:hover {
                background-color: #2a76ef;
            }
            QPushButton:pressed {
                background-color: #1a66df;
            }
        """)
        self.login_button.clicked.connect(self.on_login_clicked)
        
        # Divider
        divider_layout = QHBoxLayout()
        divider_layout.setContentsMargins(0, 20, 0, 20)  # More vertical space
        
        left_line = QFrame()
        left_line.setFrameShape(QFrame.Shape.HLine)
        left_line.setStyleSheet("background-color: #444444; min-height: 2px;")
        
        or_label = QLabel("OR")
        or_label.setStyleSheet("""
            color: #aaaaaa;
            font-size: 16px;
            font-weight: bold;
            margin: 0 15px;
        """)
        
        right_line = QFrame()
        right_line.setFrameShape(QFrame.Shape.HLine)
        right_line.setStyleSheet("background-color: #444444; min-height: 2px;")
        
        divider_layout.addWidget(left_line)
        divider_layout.addStretch()
        divider_layout.addWidget(or_label)
        divider_layout.addStretch()
        divider_layout.addWidget(right_line)
        
        # OAuth layout
        oauth_layout = QVBoxLayout()
        oauth_layout.setSpacing(15)  # Increased spacing
        oauth_layout.setContentsMargins(0, 5, 0, 5)  # Increased margins
        
        self.google_button = OAuthButton("Login with Google", "google")
        self.google_button.setMinimumHeight(50)  # Increased height
        self.google_button.setStyleSheet("""
            QPushButton {
                background-color: #ffffff;
                color: #333333;
                border-radius: 10px;
                font-size: 15px;
                font-weight: bold;
                text-align: left;
                padding-left: 20px;
                padding-top: 5px;
                padding-bottom: 5px;
                border: none;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
            QPushButton:pressed {
                background-color: #202020;
            }
        """)
        self.google_button.clicked.connect(lambda: self.on_oauth_clicked("google"))
        
        # self.github_button = OAuthButton("Login with GitHub", "github")
        # self.github_button.setMinimumHeight(50)  # Increased height
        # self.github_button.setStyleSheet("""
        #     QPushButton {
        #         background-color: #ffffff;
        #         color: #333333;
        #         border-radius: 10px;
        #         font-size: 15px;
        #         font-weight: bold;
        #         text-align: left;
        #         padding-left: 20px;
        #         padding-top: 5px;
        #         padding-bottom: 5px;
        #         border: none;
        #     }
        #     QPushButton:hover {
        #         background-color: #303030;
        #         border: 1px solid #3a86ff;
        #     }
        #     QPushButton:pressed {
        #         background-color: #202020;
        #     }
        # """)
        # self.github_button.clicked.connect(lambda: self.on_oauth_clicked("github"))
        
        oauth_layout.addWidget(self.google_button)
        # oauth_layout.addWidget(self.github_button)
        
        # Register link
        register_layout = QHBoxLayout()
        register_layout.setContentsMargins(0, 25, 0, 0)  # Increased vertical space
        
        register_label = QLabel("Don't have an account?")
        register_label.setStyleSheet("color: #cccccc; font-size: 15px;")
        register_layout.addStretch()
        
        self.register_link = QLabel("Register")
        self.register_link.setStyleSheet("""
            color: #3a86ff;
            font-size: 15px;
            font-weight: bold;
            text-decoration: none;
            margin-left: 8px;
        """)
        self.register_link.setCursor(Qt.CursorShape.PointingHandCursor)
        self.register_link.mousePressEvent = self.on_register_clicked
        register_layout.addStretch()
        
        register_layout.addStretch()
        register_layout.addWidget(register_label)
        register_layout.addWidget(self.register_link)
        register_layout.addStretch()
        
        # Error message
        self.error_label = QLabel()
        self.error_label.setStyleSheet("""
            color: #ff3333;
            font-size: 15px;
            font-weight: bold;
            min-height: 25px;
            padding: 5px;
            background-color: transparent;
            border-radius: 5px;
        """)
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.error_label.setVisible(False)
        
        # Add widgets to form layout
        form_layout.addWidget(self.email_edit)
        form_layout.addWidget(self.password_edit)
        form_layout.addLayout(remember_layout)
        form_layout.addWidget(self.login_button)
        form_layout.addLayout(divider_layout)
        form_layout.addSpacing(5)  # Add spacing before OAuth buttons
        form_layout.addLayout(oauth_layout)
        form_layout.addSpacing(5)  # Add spacing after OAuth buttons
        form_layout.addWidget(self.error_label)
        form_layout.addLayout(register_layout)
        
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
    
    def on_login_clicked(self):
        """
        Handle login button click
        """
        # Get email and password
        email = self.email_edit.text()
        password = self.password_edit.text()
        remember = self.remember_checkbox.isChecked()
        
        # Validate input
        if not email or not password:
            self.show_error("Please enter email and password")
            return
        
        # Sign in with Supabase
        logger.info(f"Attempting to sign in user: {email}")
        self.login_button.start_loading()
        success = self.supabase_service.sign_in(email, password, remember)
        self.login_button.stop_loading()
        
        if not success:
            # Error is handled by on_auth_error
            pass
    
    def on_oauth_clicked(self, provider):
        """
        Handle OAuth button click
        """
        # Get OAuth URL
        logger.info(f"Initiating OAuth login with provider: {provider}")
        auth_url = self.supabase_service.sign_in_with_oauth(provider)
        
        if not auth_url:
            # Error is handled by on_auth_error
            pass
        
        # TODO: Implement WebView for embedded OAuth login
        # For now, we'll use the system browser
    
    def on_register_clicked(self, event):
        """
        Handle register link click
        """
        logger.info("Navigating to register screen")
        self.navigate_to_register.emit()
    
    def on_forgot_password_clicked(self, event):
        """
        Handle forgot password link click
        """
        logger.info("Navigating to forgot password screen")
        self.navigate_to_forgot_password.emit()
    
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