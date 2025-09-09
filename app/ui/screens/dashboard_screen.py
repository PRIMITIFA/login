import os
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QSpacerItem, QSizePolicy)
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtGui import QIcon, QPixmap

import logging
from app.ui.widgets.animated_button import AnimatedButton

logger = logging.getLogger(__name__)

class DashboardScreen(QWidget):
    # Navigation signals
    navigate_to_login = pyqtSignal()
    
    def __init__(self, supabase_service):
        super().__init__()
        self.supabase_service = supabase_service
        self.user_role = None
        
        # Setup UI
        self.setup_ui()
        logger.info("DashboardScreen initialized")
    
    def setup_ui(self):
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create content frame
        content_frame = QFrame()
        content_frame.setObjectName("dashboardContentFrame")
        content_frame.setStyleSheet("""
            #dashboardContentFrame {
                background-color: #1a1a1a;
                border-radius: 15px;
                border: 1px solid #333333;
            }
        """)
        
        # Content layout
        content_layout = QVBoxLayout(content_frame)
        content_layout.setContentsMargins(40, 40, 40, 40)
        content_layout.setSpacing(20)
        
        # Header layout
        header_layout = QHBoxLayout()
        
        # Logo image if available
        logo_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), 
                               'app', 'assets', 'images', 'logo.png')
        if os.path.exists(logo_path):
            logo_label = QLabel()
            logo_pixmap = QPixmap(logo_path)
            logo_label.setPixmap(logo_pixmap.scaled(QSize(50, 50), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
            header_layout.addWidget(logo_label)
        
        # Title
        title_label = QLabel("CS2 Tool Dashboard")
        title_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #ffffff;
        """)
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        # Logout button
        self.logout_button = AnimatedButton("LOGOUT")
        self.logout_button.setFixedSize(120, 40)
        self.logout_button.setStyleSheet("""
            QPushButton {
                background-color: #333333;
                color: white;
                border-radius: 6px;
                font-size: 12px;
                font-weight: bold;
                text-transform: uppercase;
                letter-spacing: 1px;
            }
            QPushButton:hover {
                background-color: #444444;
            }
            QPushButton:pressed {
                background-color: #555555;
            }
        """)
        self.logout_button.clicked.connect(self.on_logout_clicked)
        header_layout.addWidget(self.logout_button)
        
        # User info layout
        user_info_layout = QHBoxLayout()
        user_info_layout.setContentsMargins(0, 20, 0, 20)
        
        # User avatar placeholder
        avatar_frame = QFrame()
        avatar_frame.setFixedSize(80, 80)
        avatar_frame.setStyleSheet("""
            background-color: #252525;
            border-radius: 40px;
            border: 2px solid #3a86ff;
        """)
        user_info_layout.addWidget(avatar_frame)
        
        # User details layout
        user_details_layout = QVBoxLayout()
        user_details_layout.setSpacing(5)
        
        # Username
        self.username_label = QLabel("Username")
        self.username_label.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #ffffff;
        """)
        
        # Email
        self.email_label = QLabel("Email")
        self.email_label.setStyleSheet("""
            font-size: 14px;
            color: #cccccc;
        """)
        
        # Role
        self.role_layout = QHBoxLayout()
        self.role_label = QLabel("Role:")
        self.role_label.setStyleSheet("""
            font-size: 14px;
            color: #cccccc;
        """)
        
        self.role_value_label = QLabel("FREE")
        self.role_value_label.setStyleSheet("""
            font-size: 14px;
            font-weight: bold;
            color: #ffffff;
            background-color: transparent;
            border-radius: 4px;
            padding: 3px 10px;
            text-transform: uppercase;
            letter-spacing: 1px;
        """)
        
        self.role_layout.addWidget(self.role_label)
        self.role_layout.addWidget(self.role_value_label)
        self.role_layout.addStretch()
        
        user_details_layout.addWidget(self.username_label)
        user_details_layout.addWidget(self.email_label)
        user_details_layout.addLayout(self.role_layout)
        
        user_info_layout.addLayout(user_details_layout)
        user_info_layout.addStretch()
        
        # Content divider
        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.HLine)
        divider.setStyleSheet("background-color: #333333;")
        
        # Dashboard content
        dashboard_layout = QVBoxLayout()
        
        # FREE content
        self.free_content = QFrame()
        free_layout = QVBoxLayout(self.free_content)
        
        free_title = QLabel("FREE Plan Features")
        free_title.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #ffffff;
            margin-bottom: 10px;
        """)
        
        free_features = QLabel("""
            • Basic CS2 tool features\n
            • Limited access to game statistics\n
            • Standard matchmaking support\n
            • Basic weapon analytics
        """)
        free_features.setStyleSheet("""
            font-size: 16px;
            color: #cccccc;
            margin-bottom: 20px;
        """)
        
        self.upgrade_button = AnimatedButton("UPGRADE TO PRO")
        self.upgrade_button.setMinimumHeight(50)
        self.upgrade_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #ff9500, stop:1 #ff3800);
                color: #ffffff;
                font-weight: bold;
                font-size: 16px;
                border-radius: 8px;
                text-transform: uppercase;
                letter-spacing: 1px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #ffaa00, stop:1 #ff4500);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #ff8000, stop:1 #ff2000);
            }
        """)
        self.upgrade_button.clicked.connect(self.on_upgrade_clicked)
        
        free_layout.addWidget(free_title)
        free_layout.addWidget(free_features)
        free_layout.addWidget(self.upgrade_button)
        
        # PRO content
        self.pro_content = QFrame()
        pro_layout = QVBoxLayout(self.pro_content)
        
        pro_title = QLabel("PRO Plan Features")
        pro_title.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #ffffff;
            margin-bottom: 10px;
        """)
        
        pro_features = QLabel("""
            • Advanced CS2 tool features\n
            • Full access to game statistics\n
            • Premium matchmaking support\n
            • Advanced weapon analytics\n
            • Team performance tracking\n
            • Strategy builder\n
            • Priority updates
        """)
        pro_features.setStyleSheet("""
            font-size: 16px;
            color: #cccccc;
            margin-bottom: 20px;
        """)
        
        pro_status = QLabel("You have access to all PRO features!")
        pro_status.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: #00cc66;
            margin-bottom: 10px;
        """)
        
        pro_layout.addWidget(pro_title)
        pro_layout.addWidget(pro_features)
        pro_layout.addWidget(pro_status)
        
        # Add widgets to dashboard layout
        dashboard_layout.addWidget(self.free_content)
        dashboard_layout.addWidget(self.pro_content)
        
        # Add widgets to content layout
        content_layout.addLayout(header_layout)
        content_layout.addLayout(user_info_layout)
        content_layout.addWidget(divider)
        content_layout.addLayout(dashboard_layout)
        
        # Add content frame to main layout with margins
        main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        main_layout.addWidget(content_frame, 1)
        main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        
        # Set layout
        self.setLayout(main_layout)
        
        # Set stylesheet
        self.setStyleSheet("""
            QWidget {
                background-color: #121212;
                color: #ffffff;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
        """)
        
        # Hide content initially
        self.free_content.hide()
        self.pro_content.hide()
    
    def update_user_info(self):
        """
        Update user information
        """
        # Get current user
        user = self.supabase_service.current_user
        
        if user:
            logger.info(f"Updating user info for: {user.email}")
            # Update username and email
            self.username_label.setText(user.user_metadata.get('username', 'User'))
            self.email_label.setText(user.email)
            
            # Get user role
            self.user_role = self.supabase_service.get_user_role()
            
            # Update role display
            logger.info(f"User role: {self.user_role}")
            if self.user_role == 'PRO':
                self.role_value_label.setText('PRO')
                self.role_value_label.setStyleSheet("""
                    font-size: 14px;
                    font-weight: bold;
                    color: #00cc66;
                    background-color: transparent;
                    border-radius: 10px;
                    padding: 2px 10px;
                """)
                
                # Show PRO content
                self.free_content.hide()
                self.pro_content.show()
            else:
                self.role_value_label.setText('FREE')
                self.role_value_label.setStyleSheet("""
                    font-size: 14px;
                    font-weight: bold;
                    color: #ffaa00;
                    background-color: transparent;
                    border-radius: 10px;
                    padding: 2px 10px;
                """)
                
                # Show FREE content
                self.free_content.show()
                self.pro_content.hide()
    
    def on_logout_clicked(self):
        """
        Handle logout button click
        """
        logger.info("Logout button clicked")
        # Sign out with Supabase
        success = self.supabase_service.sign_out()
        
        if success:
            # Navigate to login screen
            logger.info("Logout successful, navigating to login screen")
            self.navigate_to_login.emit()
    
    def on_upgrade_clicked(self):
        """
        Handle upgrade button click
        """
        logger.info("Upgrade to PRO button clicked")
        # Upgrade to PRO
        success = self.supabase_service.upgrade_to_pro()
        
        if success:
            # Update user info
            logger.info("Upgrade to PRO successful")
            self.update_user_info()