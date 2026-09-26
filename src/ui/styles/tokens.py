from dataclasses import dataclass

from PyQt6.QtGui import QColor


@dataclass(frozen=True)
class ColorPalette:
    window_bg: QColor
    dark_bg: QColor
    card_bg: QColor
    text_primary: QColor
    text_secondary: QColor
    accent: QColor
    accent_hover: QColor
    accent_light:QColor
    border: QColor
    badge_viva: QColor
    badge_tma: QColor
    success: QColor
    warning: QColor
    error: QColor

@dataclass(frozen=True)
class FontSizes:
    xs: int
    sm: int
    md: int
    lg: int
    xl: int
    xxl: int
    


COLORS = ColorPalette(
    window_bg=QColor("#1e1e2e"),
    dark_bg=QColor("#2e2e2e"),
    card_bg=QColor("#42424E"),
    text_primary=QColor("#cdd6f4"),
    text_secondary=QColor("#9a9da7"),
    accent=QColor("#ee5e0b"),
    accent_light=QColor('#FCD3BB'),
    accent_hover=QColor("#D6550B"),
    border=QColor("#313244"),
    badge_viva=QColor("#f38ba8"),
    badge_tma=QColor("#fab387"),
    success=QColor("#1E5E3A"),
    warning=QColor("#9A5800"),
    error=QColor("#A31D1D")
)


FONT_SIZES = FontSizes(
    xs=11,
    sm=12,
    md=14,
    lg=16,
    xl=20,
    xxl=24,
)