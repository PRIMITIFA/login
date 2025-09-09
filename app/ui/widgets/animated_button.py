from PyQt6.QtWidgets import QPushButton, QGraphicsDropShadowEffect, QLabel, QHBoxLayout
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QSize, pyqtProperty
from PyQt6.QtGui import QColor

class AnimatedButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setup_ui()
        
        # Loading state
        self.is_loading = False
        self.original_text = text
        
        # Connect signals
        self.pressed.connect(self.on_pressed)
        self.released.connect(self.on_released)
    
    def setup_ui(self):
        # Set button style
        self.setStyleSheet("""
            QPushButton {
                background-color: #3a86ff;
                color: white;
                border: none;
                border-radius: 25px;
                font-size: 16px;
                font-weight: bold;
                padding: 10px 20px;
            }
            
            QPushButton:hover {
                background-color: #4a96ff;
            }
            
            QPushButton:pressed {
                background-color: #2a76ef;
            }
            
            QPushButton:disabled {
                background-color: #555555;
                color: #aaaaaa;
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
    
    def start_loading(self):
        """
        Show loading state
        """
        self.is_loading = True
        self.setEnabled(False)
        self.setText("Loading...")
    
    def stop_loading(self):
        """
        Hide loading state
        """
        self.is_loading = False
        self.setEnabled(True)
        self.setText(self.original_text)
    
    # Shadow strength property for animation
    def get_shadow_strength(self):
        return self._shadow_strength
    
    def set_shadow_strength(self, value):
        self._shadow_strength = value
        shadow = self.graphicsEffect()
        if shadow:
            shadow.setBlurRadius(15 + value / 10)
            shadow.setColor(QColor(58, 134, 255, 80 + int(value / 2)))
    
    shadow_strength = pyqtProperty(float, get_shadow_strength, set_shadow_strength)