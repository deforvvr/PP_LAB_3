import tkinter as tk

from config import HELP_TEXT, SPEED_OPTIONS, WINDOW_SIZES


def build_menu(root: tk.Tk, callbacks: dict[str, object], safe) -> None:
    menubar = tk.Menu(root)

    game_menu = tk.Menu(menubar, tearoff=False)
    game_menu.add_command(label="Новая игра", command=safe(callbacks["new_game"]))
    game_menu.add_separator()
    game_menu.add_command(label="Пауза", command=safe(callbacks["pause_game"]))
    game_menu.add_command(label="Продолжить", command=safe(callbacks["resume_game"]))
    game_menu.add_separator()
    game_menu.add_command(label="Выход", command=callbacks["exit"])
    menubar.add_cascade(label="Игра", menu=game_menu)

    speed_menu = tk.Menu(menubar, tearoff=False)
    for label, speed_ms in SPEED_OPTIONS:
        speed_menu.add_command(
            label=label, command=safe(lambda value=speed_ms: callbacks["set_speed"](value))
        )
    menubar.add_cascade(label="Скорость", menu=speed_menu)

    window_menu = tk.Menu(menubar, tearoff=False)
    for width, height in WINDOW_SIZES:
        window_menu.add_command(
            label=f"{width}x{height}",
            command=safe(lambda w=width, h=height: callbacks["set_window_size"](w, h)),
        )
    menubar.add_cascade(label="Окно", menu=window_menu)

    help_menu = tk.Menu(menubar, tearoff=False)
    help_menu.add_command(label="Управление", command=safe(callbacks["show_help"]))
    menubar.add_cascade(label="Справка", menu=help_menu)

    root.config(menu=menubar)


def build_canvas_and_status(
    root: tk.Tk, background_color: str
) -> tuple[tk.Canvas, tk.StringVar, tk.Label]:
    canvas = tk.Canvas(root, bg=background_color, highlightthickness=0)
    canvas.pack(fill=tk.BOTH, expand=True)

    status_var = tk.StringVar()
    status_label = tk.Label(root, textvariable=status_var, anchor="w")
    status_label.pack(fill=tk.X)
    return canvas, status_var, status_label


def get_help_text() -> str:
    return HELP_TEXT
