import os
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
                             QPushButton, QFrame, QSpacerItem, QSizePolicy)
from PyQt6.QtCore import Qt, pyqtSignal, QSize, QTimer
from PyQt6.QtGui import QPixmap

from app.ui.widgets.animated_button import AnimatedButton
from app.ui.widgets.animated_line_edit import AnimatedLineEdit

import logging

logger = logging.getLogger(__name__)

class ForgotPasswordScreen(QWidget):
    # Navigation signals
    navigate_to_login = pyqtSignal()
    
    def __init__(self, supabase_service):
        super().__init__()
        self.supabase_service = supabase_service
        
        # Connect to auth error signal
        self.supabase_service.auth_error.connect(self.on_auth_error)
        
        # Setup UI
        self.setup_ui()
        logger.info("ForgotPasswordScreen initialized")
    
    def setup_ui(self):
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create content frame
        content_frame = QFrame()
        content_frame.setObjectName("forgotPasswordContentFrame")
        content_frame.setStyleSheet('''
            #forgotPasswordContentFrame {
                background-color: transparent;
                border-radius: 15px;
                border: none;
            }
        ''')
        
        # Content layout
        content_layout = QVBoxLayout(content_frame)
        content_layout.setContentsMargins(40, 40, 40, 40)
        content_layout.setSpacing(20)
        
        # Title
        title_label = QLabel("Forgot Password")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet('''
            font-size: 24px;
            font-weight: bold;
            color: #ffffff;
            margin-bottom: 15px;
        ''')
        
        # Form layout
        form_layout = QVBoxLayout()
        form_layout.setSpacing(15)
        
        # Email field
        self.email_edit = AnimatedLineEdit()
        self.email_edit.setPlaceholderText("Enter your email")
        self.email_edit.setMinimumHeight(50)
        self.email_edit.setStyleSheet('''
            QLineEdit {
                background-color: #252525;
                border: 2px solid #333333;
                border-radius: 10px;
                padding: 10px 20px;
                color: #ffffff;
                font-size: 15px;
            }
            QLineEdit:focus {
                border: 2px solid #3a86ff;
                background-color: #2a2a2a;
            }
        ''')
        
        # Send recovery email button
        self.send_button = AnimatedButton("Send Recovery Email")
        self.send_button.setMinimumHeight(50)
        self.send_button.setStyleSheet('''
            QPushButton {
                background-color: #3a86ff;
                color: white;
                border-radius: 10px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2a76ef;
            }
            QPushButton:pressed {
                background-color: #1a66df;
            }
        ''')
        self.send_button.clicked.connect(self.on_send_clicked)
        
        # Back to login link
        back_layout = QHBoxLayout()
        back_layout.setContentsMargins(0, 25, 0, 0)
        
        self.back_link = QLabel("Back to Login")
        self.back_link.setStyleSheet('''
            color: #3a86ff;
            font-size: 15px;
            font-weight: bold;
            text-decoration: none;
        ''')
        self.back_link.setCursor(Qt.CursorShape.PointingHandCursor)
        self.back_link.mousePressEvent = self.on_back_clicked
        
        back_layout.addStretch()
        back_layout.addWidget(self.back_link)
        back_layout.addStretch()
        
        # Error/Success message
        self.message_label = QLabel()
        self.message_label.setStyleSheet('''
            font-size: 15px;
            font-weight: bold;
            min-height: 25px;
            padding: 5px;
            border-radius: 5px;
        ''')
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.message_label.setVisible(False)
        
        # Add widgets to form layout
        form_layout.addWidget(self.email_edit)
        form_layout.addWidget(self.send_button)
        form_layout.addWidget(self.message_label)
        form_layout.addLayout(back_layout)
        
        # Add widgets to content layout
        content_layout.addWidget(title_label)
        content_layout.addLayout(form_layout)
        
        # Add content frame to main layout
        main_layout.addWidget(content_frame)
        
        # Set layout
        self.setLayout(main_layout)
        
        # Set stylesheet
        self.setStyleSheet('''
            QWidget {
                background-color: transparent;
                color: #ffffff;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
        ''')
    
    def on_send_clicked(self):
        email = self.email_edit.text()
        if not email:
            self.show_message("Please enter your email", is_error=True)
            return
        
        logger.info(f"Sending password recovery email to: {email}")
        self.send_button.start_loading()
        success = self.supabase_service.send_password_reset_email(email)
        self.on_recovery_sent(success)

    def on_recovery_sent(self, success):
        self.send_button.stop_loading()
        if success:
            logger.info("Password recovery email sent successfully.")
            self.show_message("Password recovery email sent!", is_error=False)
        else:
            logger.error("Failed to send password recovery email.")
            self.show_message("Failed to send recovery email.", is_error=True)

    def on_back_clicked(self, event):
        logger.info("Navigating back to login screen.")
        self.navigate_to_login.emit()
    
    def on_auth_error(self, error_message):
        logger.error(f"Authentication error: {error_message}")
        self.show_message(error_message, is_error=True)
    
    def show_message(self, message, is_error=False):
        self.message_label.setText(message)
        if is_error:
            logger.error(f"Displaying error message: {message}")
            self.message_label.setStyleSheet('''
                color: #ff3333;
                background-color: transparent;
                font-size: 15px;
                font-weight: bold;
                min-height: 25px;
                padding: 5px;
                border-radius: 5px;
            ''')
        else:
            logger.info(f"Displaying success message: {message}")
            self.message_label.setStyleSheet('''
                color: #2ecc71;
                background-color: transparent;
                font-size: 15px;
                font-weight: bold;
                min-height: 25px;
                padding: 5px;
                border-radius: 5px;
            ''')
        self.message_label.setVisible(True)
        QTimer.singleShot(5000, lambda: self.message_label.setVisible(False))