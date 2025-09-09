import os
from PyQt6.QtWidgets import (QMainWindow, QStackedWidget, QWidget, QHBoxLayout, 
                             QLabel, QPushButton, QVBoxLayout, QFrame)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QSize, QPoint
from PyQt6.QtGui import QIcon, QFont, QMouseEvent

from app.services.supabase_service import SupabaseService
from app.ui.screens.login_screen import LoginScreen
from app.ui.screens.register_screen import RegisterScreen
from app.ui.screens.dashboard_screen import DashboardScreen
from app.ui.screens.forgot_password_screen import ForgotPasswordScreen

class MainWindow(QMainWindow):
    def __init__(self, config):
        super().__init__()
        
        # Initialize services
        self.supabase_service = SupabaseService(config)
        
        # Connect to auth state changes
        self.supabase_service.auth_state_changed.connect(self.on_auth_state_changed)
        
        # Setup UI
        self.setup_ui()
        
        # Apply rounded corners to the window
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
    
    def setup_ui(self):
        # Set window properties
        self.setWindowTitle("CS2 Tool Login")
        self.setMinimumSize(300, 600)  # Smaller size for better fit
        self.setStyleSheet("""
            QMainWindow {
                background-color: transparent;
                color: #ffffff;
            }
        """)
        
        # Set window flags for modern look
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)  # Remove default window frame
        
        # Set window icon if available
        icon_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 
                               'app', 'assets', 'icons', 'app_icon.png')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        # Create main container widget with rounded corners
        self.container = QFrame()
        self.container.setObjectName("mainContainer")
        self.container.setStyleSheet("""
            #mainContainer {
                background-color: #121212;
                border-radius: 15px;
                border: none;
            }
        """)
        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setContentsMargins(0, 0, 0, 0)
        self.container_layout.setSpacing(0)
        self.setCentralWidget(self.container)
        
        # Create custom title bar
        self.create_title_bar()
        
        # Create stacked widget for screen management
        self.stacked_widget = QStackedWidget()
        self.container_layout.addWidget(self.stacked_widget)
        
        # Create screens
        self.login_screen = LoginScreen(self.supabase_service)
        self.register_screen = RegisterScreen(self.supabase_service)
        self.dashboard_screen = DashboardScreen(self.supabase_service)
        self.forgot_password_screen = ForgotPasswordScreen(self.supabase_service)
        
        # Add screens to stacked widget
        self.stacked_widget.addWidget(self.login_screen)
        self.stacked_widget.addWidget(self.register_screen)
        self.stacked_widget.addWidget(self.dashboard_screen)
        self.stacked_widget.addWidget(self.forgot_password_screen)
        
        # Connect navigation signals
        self.login_screen.navigate_to_register.connect(lambda: self.change_screen(1))
        self.login_screen.navigate_to_forgot_password.connect(lambda: self.change_screen(3))
        self.register_screen.navigate_to_login.connect(lambda: self.change_screen(0))
        self.dashboard_screen.navigate_to_login.connect(lambda: self.change_screen(0))
        self.forgot_password_screen.navigate_to_login.connect(lambda: self.change_screen(0))
        
        # Start with login screen
        self.stacked_widget.setCurrentIndex(0)
    
    def change_screen(self, index):
        """
        Change screen with animation
        """
        # Get current and next widget
        current_widget = self.stacked_widget.currentWidget()
        next_widget = self.stacked_widget.widget(index)
        
        if current_widget == next_widget:
            return
        
        # Set next widget opacity to 0
        next_widget.setStyleSheet("background-color: #1a1a1a; opacity: 0;")
        
        # Change to next widget
        self.stacked_widget.setCurrentIndex(index)
        
        # Create fade-in animation
        self.fade_in_animation = QPropertyAnimation(next_widget, b"windowOpacity")
        self.fade_in_animation.setDuration(250)
        self.fade_in_animation.setStartValue(0.0)
        self.fade_in_animation.setEndValue(1.0)
        self.fade_in_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.fade_in_animation.start()
    
    def create_title_bar(self):
        """
        Create custom title bar with window controls
        """
        # Title bar container
        self.title_bar = QFrame()
        self.title_bar.setFixedHeight(40)
        self.title_bar.setStyleSheet("""
            QFrame {
                background-color: #1e1e1e;
                border-top-left-radius: 15px;
                border-top-right-radius: 15px;
                border-bottom: 1px solid #333333;
            }
            QPushButton {
                background-color: transparent;
                color: #cccccc;
                border: none;
                font-size: 16px;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: #333333;
            }
            QPushButton#close_button {
                border-radius: 10px;
            }
            QPushButton#close_button:hover {
                background-color: #e81123;
                color: white;
            }
        """)
        
        # Layout for title bar
        title_layout = QHBoxLayout(self.title_bar)
        title_layout.setContentsMargins(10, 0, 0, 0)
        title_layout.setSpacing(0)
        
        # Window title
        title_label = QLabel("CS2 Tool Login")
        title_label.setStyleSheet("color: #ffffff; font-size: 14px; font-weight: bold;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        
        # Window controls
        btn_minimize = QPushButton("−")
        btn_minimize.setFixedSize(40, 40)
        btn_minimize.clicked.connect(self.showMinimized)
        
        btn_maximize = QPushButton("□")
        btn_maximize.setFixedSize(40, 40)
        btn_maximize.clicked.connect(self.toggle_maximize)
        
        btn_close = QPushButton("×")
        btn_close.setObjectName("close_button")
        btn_close.setFixedSize(40, 40)
        btn_close.clicked.connect(self.close)
        
        # Add widgets to layout
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        title_layout.addWidget(btn_minimize)
        title_layout.addWidget(btn_maximize)
        title_layout.addWidget(btn_close)
        
        # Add title bar to main container
        self.container_layout.addWidget(self.title_bar)
        
        # Variables for window dragging
        self.dragging = False
        self.drag_position = QPoint()
    
    def toggle_maximize(self):
        """
        Toggle between maximized and normal window state
        """
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()
    
    def mousePressEvent(self, event: QMouseEvent):
        """
        Handle mouse press events for window dragging
        """
        if event.button() == Qt.MouseButton.LeftButton and self.title_bar.geometry().contains(event.position().toPoint()):
            self.dragging = True
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()
    
    def mouseMoveEvent(self, event: QMouseEvent):
        """
        Handle mouse move events for window dragging
        """
        if self.dragging and event.buttons() & Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()
    
    def mouseReleaseEvent(self, event: QMouseEvent):
        """
        Handle mouse release events for window dragging
        """
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = False
            event.accept()
    
    def on_auth_state_changed(self, auth_state):
        """
        Handle authentication state changes
        """
        user = auth_state.get('user')
        
        if user:
            # User is authenticated, show dashboard
            self.dashboard_screen.update_user_info()
            self.change_screen(2)
        else:
            # User is not authenticated, show login
            self.change_screen(0)