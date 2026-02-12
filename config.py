TITLE = "Змейка"

ROWS = 20
COLS = 20

DEFAULT_CELL_SIZE = 25
MIN_CELL_SIZE = 8
DEFAULT_SPEED_MS = 120

DEFAULT_WINDOW_SIZE = (600, 650)
WINDOW_SIZES = [
    (400, 450),
    (600, 650),
    (800, 850),
]

SPEED_OPTIONS = [
    ("Медленно", 200),
    ("Нормально", 120),
    ("Быстро", 80),
]

HELP_TEXT = (
    "Стрелки или WASD - движение\n"
    "Пробел - пауза/продолжить\n"
    "Esc - выход"
)

COLORS = {
    "background": "#111111",
    "food": "#e74c3c",
    "snake_body": "#2ecc71",
    "snake_head": "#27ae60",
    "snake_outline": "#0e0e0e",
    "overlay_bg": "#000000",
    "overlay_text": "#ffffff",
}

OVERLAY_STIPPLE = "gray50"
OVERLAY_FONT = ("Segoe UI", 24, "bold")
