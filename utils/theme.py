from PySide6.QtGui import QColor, QFont

class Theme:
    # Primary Palette (Modern Teal & Slate)
    PRIMARY = QColor("#2C7878")
    PRIMARY_DARK = QColor("#1E5F5F")
    PRIMARY_LIGHT = QColor("#4A9A9A")
    
    # Neutral Palette
    BG_MAIN = QColor("#F8FAFC")
    BG_CARD = QColor("#FFFFFF")
    TEXT_MAIN = QColor("#1E293B")
    TEXT_SUB = QColor("#64748B")
    TEXT_LIGHT = QColor("#FFFFFF")
    
    # Semantic Colors
    SUCCESS = QColor("#10B981")
    ERROR = QColor("#EF4444")
    WARNING = QColor("#F59E0B")
    INFO = QColor("#3B82F6")
    
    # Border & Dividers
    BORDER = QColor("#E2E8F0")
    BORDER_DARK = QColor("#CBD5E1")
    
    # Glassmorphism Tokens
    GLASS_BG = "rgba(255, 255, 255, 0.7)"
    GLASS_BORDER = "rgba(255, 255, 255, 0.4)"
    
    # Typography
    FONT_FAMILY = "Inter"
    
    @staticmethod
    def get_font(size=14, weight=QFont.Normal):
        font = QFont(Theme.FONT_FAMILY, size, weight)
        # Use a fallback if Inter is not available
        if not font.exactMatch():
            font.setFamily("Segoe UI")
        return font

    @staticmethod
    def apply_card_style(widget):
        widget.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border: 1px solid {Theme.BORDER.name()};
                border-radius: 12px;
            }}
        """)
