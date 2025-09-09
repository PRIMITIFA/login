import os
from PyQt6.QtWidgets import QPushButton, QGraphicsDropShadowEffect, QLabel, QHBoxLayout
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QSize, pyqtProperty
from PyQt6.QtGui import QColor, QIcon

class OAuthButton(QPushButton):
    def __init__(self, text, provider, parent=None):
        super().__init__(text, parent)
        self.provider = provider
        self.setup_ui()
        
        # Connect signals
        self.pressed.connect(self.on_pressed)
        self.released.connect(self.on_released)
    
    def setup_ui(self):
        # Set button style based on provider
        if self.provider == "google":
            self.setStyleSheet("""
                QPushButton {
                    background-color: #ffffff;
                    color: #333333;
                    border: none;
                    border-radius: 25px;
                    font-size: 16px;
                    font-weight: bold;
                    padding: 10px 20px;
                    text-align: left;
                    padding-left: 50px;
                }
                
                QPushButton:hover {
                    background-color: #f0f0f0;
                }
                
                QPushButton:pressed {
                    background-color: #e0e0e0;
                }
            """)
        elif self.provider == "github":
            self.setStyleSheet("""
                QPushButton {
                    background-color: #24292e;
                    color: white;
                    border: none;
                    border-radius: 25px;
                    font-size: 16px;
                    font-weight: bold;
                    padding: 10px 20px;
                    text-align: left;
                    padding-left: 50px;
                }
                
                QPushButton:hover {
                    background-color: #2f363d;
                }
                
                QPushButton:pressed {
                    background-color: #1a1f23;
                }
            """)
        else:
            self.setStyleSheet("""
                QPushButton {
                    background-color: #555555;
                    color: white;
                    border: none;
                    border-radius: 25px;
                    font-size: 16px;
                    font-weight: bold;
                    padding: 10px 20px;
                    text-align: left;
                    padding-left: 50px;
                }
                
                QPushButton:hover {
                    background-color: #666666;
                }
                
                QPushButton:pressed {
                    background-color: #444444;
                }
            """)
        
        # Add drop shadow effect
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(0, 5)
        self.setGraphicsEffect(shadow)
        
        # Create hover animation
        self._shadow_strength = 0
        self.shadow_animation = QPropertyAnimation(self, b"shadow_strength")
        self.shadow_animation.setDuration(200)
        self.shadow_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        # Add provider icon
        self.update_icon()
    
    def update_icon(self):
        """
        Add provider icon to button
        """
        # Get icon path
        icon_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), 
                               'app', 'assets', 'icons', f"{self.provider}.svg")
        
        # If icon exists, set it
        if os.path.exists(icon_path):
            self.setIcon(QIcon(icon_path))
            self.setIconSize(QSize(24, 24))
    
    def enterEvent(self, event):
        """
        Handle mouse enter event
        """
        self.shadow_animation.setStartValue(self._shadow_strength)
        self.shadow_animation.setEndValue(100)
        self.shadow_animation.start()
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        """
        Handle mouse leave event
        """
        self.shadow_animation.setStartValue(self._shadow_strength)
        self.shadow_animation.setEndValue(0)
        self.shadow_animation.start()
        super().leaveEvent(event)
    
    def on_pressed(self):
        """
        Handle button press
        """
        # Scale down animation
        self.scale_animation = QPropertyAnimation(self, b"size")
        self.scale_animation.setDuration(100)
        self.scale_animation.setStartValue(self.size())
        self.scale_animation.setEndValue(QSize(int(self.width() * 0.95), int(self.height() * 0.95)))
        self.scale_animation.setEasingCurve(QEasingCurve.Type.OutQuad)
        self.scale_animation.start()
    
    def on_released(self):
        """
        Handle button release
        """
        # Scale up animation
        self.scale_animation = QPropertyAnimation(self, b"size")
        self.scale_animation.setDuration(100)
        self.scale_animation.setStartValue(self.size())
        self.scale_animation.setEndValue(QSize(int(self.width() / 0.95), int(self.height() / 0.95)))
        self.scale_animation.setEasingCurve(QEasingCurve.Type.OutQuad)
        self.scale_animation.start()
    
    # Shadow strength property for animation
    def get_shadow_strength(self):
        return self._shadow_strength
    
    def set_shadow_strength(self, value):
        self._shadow_strength = value
        shadow = self.graphicsEffect()
        if shadow:
            shadow.setBlurRadius(15 + value / 10)
            
            # Set shadow color based on provider
            if self.provider == "google":
                shadow.setColor(QColor(66, 133, 244, 80 + int(value / 2)))
            elif self.provider == "github":
                shadow.setColor(QColor(36, 41, 46, 80 + int(value / 2)))
            else:
                shadow.setColor(QColor(85, 85, 85, 80 + int(value / 2)))
    
    shadow_strength = pyqtProperty(float, get_shadow_strength, set_shadow_strength)