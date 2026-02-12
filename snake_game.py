import tkinter as tk
from tkinter import messagebox

from config import (
    COLORS,
    DEFAULT_CELL_SIZE,
    DEFAULT_SPEED_MS,
    DEFAULT_WINDOW_SIZE,
    MIN_CELL_SIZE,
    ROWS,
    COLS,
    TITLE,
)
from logic import SnakeLogic
from renderer import SnakeRenderer
from ui import build_canvas_and_status, build_menu, get_help_text


class SnakeGame:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title(TITLE)
        self.root.geometry(f"{DEFAULT_WINDOW_SIZE[0]}x{DEFAULT_WINDOW_SIZE[1]}")
        self.root.minsize(320, 360)
        self.root.resizable(True, True)
        self.root.report_callback_exception = self._handle_callback_exception

        self.speed_ms = DEFAULT_SPEED_MS
        self.after_id = None

        self.canvas, self.status_var, self.status_label = build_canvas_and_status(
            self.root, COLORS["background"]
        )
        self.logic = SnakeLogic(ROWS, COLS)
        self.renderer = SnakeRenderer(
            self.canvas, ROWS, COLS, COLORS, DEFAULT_CELL_SIZE
        )
        build_menu(self.root, self._menu_callbacks(), self._safe)
        self._bind_events()
        self.new_game()

    def _menu_callbacks(self) -> dict[str, object]:
        return {
            "new_game": self.new_game,
            "pause_game": self.pause_game,
            "resume_game": self.resume_game,
            "exit": self.root.destroy,
            "set_speed": self.set_speed,
            "set_window_size": self.set_window_size,
            "show_help": self.show_help,
        }

    def _bind_events(self) -> None:
        self.root.bind("<KeyPress>", self._safe(self._on_key_press))
        self.root.bind("<Escape>", lambda _e: self.root.destroy())
        self.root.bind("<space>", self._safe(lambda _e: self.toggle_pause()))
        self.canvas.bind("<Configure>", self._safe(self._on_canvas_resize))
        self.root.bind("<r>", self._safe(lambda _e: self.new_game()))
        self.root.bind("<R>", self._safe(lambda _e: self.new_game()))

    def _handle_callback_exception(self, exc, val, tb) -> None:
        messagebox.showerror("Ошибка", f"{exc.__name__}: {val}")
        self.status_var.set("Ошибка обработана. Приложение продолжает работу.")
        self.logic.state.is_paused = True

    def _safe(self, func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as exc:
                messagebox.showerror("Ошибка", str(exc))
                self.status_var.set("Ошибка обработана. Приложение продолжает работу.")
                self.logic.state.is_paused = True

        return wrapper

    def set_window_size(self, width: int, height: int) -> None:
        self.root.geometry(f"{width}x{height}")

    def set_speed(self, speed_ms: int) -> None:
        self.speed_ms = speed_ms
        self.status_var.set(f"Скорость: {speed_ms} мс")

    def toggle_pause(self) -> None:
        if self.logic.state.is_paused:
            self.resume_game()
        else:
            self.pause_game()

    def pause_game(self) -> None:
        self.logic.state.is_paused = True
        self.status_var.set(f"Пауза | Счет: {self.logic.state.score}")

    def resume_game(self) -> None:
        if not self.logic.state.is_running:
            return
        self.logic.state.is_paused = False
        self.status_var.set(f"Игра | Счет: {self.logic.state.score}")

    def new_game(self) -> None:
        if self.after_id is not None:
            self.root.after_cancel(self.after_id)
        self.logic.reset()
        self._draw()
        self.status_var.set("Игра | Счет: 0")
        self._schedule_tick()

    def _schedule_tick(self) -> None:
        if self.logic.state.is_running:
            self.after_id = self.root.after(self.speed_ms, self._safe(self._tick))

    def _tick(self) -> None:
        state = self.logic.state
        if state.is_paused or not state.is_running:
            self._schedule_tick()
            return
        result = self.logic.step()
        if result in {"game_over", "win"}:
            self._game_over(win=result == "win")
            return
        self._draw()
        self.status_var.set(f"Игра | Счет: {state.score}")
        self._schedule_tick()

    def _game_over(self, win: bool = False) -> None:
        message = "Победа! Поле заполнено." if win else "Игра окончена."
        self.status_var.set(f"{message} Счет: {self.logic.state.score}")
        messagebox.showinfo("Игра окончена", f"{message}\nСчет: {self.logic.state.score}")
        self._draw()

    def _on_key_press(self, event) -> None:
        key = event.keysym
        mapping = {
            "Up": "Up",
            "Down": "Down",
            "Left": "Left",
            "Right": "Right",
            "w": "Up",
            "W": "Up",
            "s": "Down",
            "S": "Down",
            "a": "Left",
            "A": "Left",
            "d": "Right",
            "D": "Right",
        }
        if key not in mapping:
            return
        self.logic.set_direction(mapping[key])

    def _on_canvas_resize(self, event) -> None:
        width = max(event.width, 1)
        height = max(event.height, 1)
        self.renderer.resize(width, height, MIN_CELL_SIZE)
        self._draw()

    def _draw(self) -> None:
        state = self.logic.state
        overlay_text = None
        if state.is_paused and state.is_running:
            overlay_text = "Пауза"
        if not state.is_running:
            overlay_text = "Игра окончена"
        self.renderer.draw(state, overlay_text=overlay_text)

    def show_help(self) -> None:
        messagebox.showinfo("Управление", get_help_text())
