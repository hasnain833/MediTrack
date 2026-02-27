from PySide6.QtGui import QColor, QFont

class Theme:
    # Primary Palette (Modern Vibrant Blue)
    ROYAL_BLUE = QColor("#2563EB")
    PRIMARY_TEAL = QColor("#2DD4BF")
    DEEP_NAVY = QColor("#0F172A")
    PRIMARY = QColor("#2563EB")
    PRIMARY_DARK = QColor("#1E40AF")
    PRIMARY_LIGHT = QColor("#60A5FA")
    
    # Sidebar Palette
    SIDEBAR_BG = QColor("#1E293B")
    SIDEBAR_TEXT = QColor("#FFFFFF")
    SIDEBAR_SUBTEXT = QColor("#94A3B8")
    
    # Neutral Palette
    BG_MAIN = QColor("#F3F4F6")
    BG_CARD = QColor("#FFFFFF")
    TEXT_MAIN = QColor("#111827")
    TEXT_SUB = QColor("#6B7280")
    TEXT_LIGHT = QColor("#FFFFFF")
    
    # Dashboard Card Pastels
    CARD_PINK = QColor("#FCE7F3")
    CARD_PURPLE = QColor("#EDE9FE")
    CARD_CYAN = QColor("#E0F2FE")
    CARD_YELLOW = QColor("#FEF9C3")
    
    # Semantic Colors
    SUCCESS = QColor("#10B981")
    ERROR = QColor("#EF4444")
    WARNING = QColor("#F59E0B")
    INFO = QColor("#3B82F6")
    
    # Border & Dividers
    BORDER = QColor("#E5E7EB")
    BORDER_DARK = QColor("#D1D5DB")
    
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
