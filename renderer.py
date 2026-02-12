from __future__ import annotations

import tkinter as tk

from config import OVERLAY_FONT, OVERLAY_STIPPLE
from logic import GameState, Position


class SnakeRenderer:
    def __init__(
        self,
        canvas: tk.Canvas,
        rows: int,
        cols: int,
        colors: dict[str, str],
        default_cell_size: int,
    ) -> None:
        self.canvas = canvas
        self.rows = rows
        self.cols = cols
        self.colors = colors
        self.cell_size = default_cell_size

    def resize(self, width: int, height: int, min_cell_size: int) -> int:
        cell = min(width // self.cols, height // self.rows)
        self.cell_size = max(cell, min_cell_size)
        return self.cell_size

    def draw(self, state: GameState, overlay_text: str | None = None) -> None:
        self.canvas.delete("all")
        self._draw_grid()
        self._draw_food(state.food)
        self._draw_snake(state.snake)
        if overlay_text:
            self._draw_overlay(overlay_text)

    def _draw_grid(self) -> None:
        w = self.cell_size * self.cols
        h = self.cell_size * self.rows
        self.canvas.config(scrollregion=(0, 0, w, h))

    def _draw_food(self, pos: Position) -> None:
        x1, y1, x2, y2 = self._cell_bounds(pos)
        self.canvas.create_rectangle(
            x1, y1, x2, y2, fill=self.colors["food"], outline=self.colors["food"]
        )

    def _draw_snake(self, snake: list[Position]) -> None:
        for index, pos in enumerate(snake):
            x1, y1, x2, y2 = self._cell_bounds(pos)
            is_head = index == len(snake) - 1
            color = self.colors["snake_head"] if is_head else self.colors["snake_body"]
            self.canvas.create_rectangle(
                x1,
                y1,
                x2,
                y2,
                fill=color,
                outline=self.colors["snake_outline"],
            )

    def _draw_overlay(self, text: str) -> None:
        w = self.cell_size * self.cols
        h = self.cell_size * self.rows
        self.canvas.create_rectangle(
            0,
            0,
            w,
            h,
            fill=self.colors["overlay_bg"],
            stipple=OVERLAY_STIPPLE,
            outline="",
        )
        self.canvas.create_text(
            w // 2,
            h // 2,
            text=text,
            fill=self.colors["overlay_text"],
            font=OVERLAY_FONT,
        )

    def _cell_bounds(self, pos: Position) -> tuple[int, int, int, int]:
        r, c = pos
        x1 = c * self.cell_size
        y1 = r * self.cell_size
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size
        return x1, y1, x2, y2
