from PyQt6.QtGui import QFont, QFontDatabase
from pathlib import Path


class Theme:
    class Colors:
        BG_WHITE = "#FFFFFF"
        PRIMARY = "#f39c12"
        SIDEBAR_BG = "#FFEBD3"
        PAGE_BG = "#F9FAFB"
        CARD_BG = "#E8EAED"
        SEARCH_BG = "#EBEDF0"
        TEXT_DARK = "#1F2937"
        TEXT_MUTED = "#4B5563"
        BADGE_BG = "#F59E0B"
        BADGE_TEXT = "#FFFFFF"
    
    class Fonts:
        FAMILY = "Poppins"
        SMALL = 10
        NORMAL = 12
        MEDIUM = 14
        LARGE = 16
        XLARGE = 20
        
        @staticmethod
        def load_fonts():
            font_dir = Path(__file__).parent.parent / "assets" / "fonts"
            if font_dir.exists():
                for font_file in font_dir.glob("*.ttf"):
                    QFontDatabase.addApplicationFont(str(font_file))

    class BorderRadius:
        SMALL = 12
        MEDIUM = 20
        ROUND = 60
    
    @staticmethod
    def get_font(size=Fonts.NORMAL, bold=False, italic=False):
        """Get a Poppins font with specified size and style"""
        font = QFont(Theme.Fonts.FAMILY, size)
        if bold:
            font.setBold(True)
        if italic:
            font.setItalic(True)
        return font
        