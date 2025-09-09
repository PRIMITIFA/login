from PyQt6.QtWidgets import QLineEdit, QGraphicsDropShadowEffect
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtProperty
from PyQt6.QtGui import QColor

class AnimatedLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
        # Focus state
        self.is_focused = False
        
        # Connect signals
        self.textChanged.connect(self.on_text_changed)
    
    def setup_ui(self):
        # Set line edit style
        self.setStyleSheet("""
            QLineEdit {
                background-color: transparent;
                color: white;
                border: 2px solid #444444;
                border-radius: 10px;
                padding: 10px 15px;
                font-size: 16px;
            }
            
            QLineEdit:focus {
                border: 2px solid #3a86ff;
            }
        """)
        
        # Add drop shadow effect
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(10)
        shadow.setColor(QColor(0, 0, 0, 50))
        shadow.setOffset(0, 2)
        self.setGraphicsEffect(shadow)
        
        # Create focus animation
        self._border_color = QColor(68, 68, 68)  # #444444
        self.border_animation = QPropertyAnimation(self, b"border_color")
        self.border_animation.setDuration(200)
        self.border_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
    
    def focusInEvent(self, event):
        """
        Handle focus in event
        """
        self.is_focused = True
        self.border_animation.setStartValue(self._border_color)
        self.border_animation.setEndValue(QColor(58, 134, 255))  # #3a86ff
        self.border_animation.start()
        super().focusInEvent(event)
    
    def focusOutEvent(self, event):
        """
        Handle focus out event
        """
        self.is_focused = False
        self.border_animation.setStartValue(self._border_color)
        self.border_animation.setEndValue(QColor(68, 68, 68))  # #444444
        self.border_animation.start()
        super().focusOutEvent(event)
    
    def on_text_changed(self, text):
        """
        Handle text changed event
        """
        # Update border color based on content
        if text and not self.is_focused:
            self.border_animation.setStartValue(self._border_color)
            self.border_animation.setEndValue(QColor(85, 85, 85))  # #555555
            self.border_animation.start()
        elif not text and not self.is_focused:
            self.border_animation.setStartValue(self._border_color)
            self.border_animation.setEndValue(QColor(68, 68, 68))  # #444444
            self.border_animation.start()
    
    # Border color property for animation
    def get_border_color(self):
        return self._border_color
    
    def set_border_color(self, color):
        self._border_color = color
        self.setStyleSheet(f"""
            QLineEdit {{
                background-color: transparent;
                color: white;
                border: 2px solid {color.name()};
                border-radius: 10px;
                padding: 10px 15px;
                font-size: 16px;
            }}
            
            QLineEdit:focus {{
                border: 2px solid #3a86ff;
            }}
        """)
    
    border_color = pyqtProperty(QColor, get_border_color, set_border_color)