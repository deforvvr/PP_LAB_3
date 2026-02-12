from __future__ import annotations

import random
from dataclasses import dataclass, field

Position = tuple[int, int]
Direction = str


@dataclass
class GameState:
    snake: list[Position] = field(default_factory=list)
    food: Position = (0, 0)
    direction: Direction = "Right"
    next_direction: Direction = "Right"
    score: int = 0
    is_paused: bool = False
    is_running: bool = False


class SnakeLogic:
    def __init__(self, rows: int, cols: int, rng: random.Random | None = None) -> None:
        self.rows = rows
        self.cols = cols
        self.rng = rng or random
        self.state = GameState()
        self.reset()

    def reset(self) -> None:
        mid_row = self.rows // 2
        mid_col = self.cols // 2
        self.state.snake = [
            (mid_row, mid_col - 1),
            (mid_row, mid_col),
            (mid_row, mid_col + 1),
        ]
        self.state.food = (0, 0)
        self.state.direction = "Right"
        self.state.next_direction = "Right"
        self.state.score = 0
        self.state.is_paused = False
        self.state.is_running = True
        self._spawn_food()

    def set_direction(self, new_dir: Direction) -> None:
        if self._is_opposite(new_dir, self.state.direction):
            return
        self.state.next_direction = new_dir

    def step(self) -> str:
        self.state.direction = self.state.next_direction
        head_r, head_c = self.state.snake[-1]
        delta_r, delta_c = self._dir_to_delta(self.state.direction)
        new_head = (head_r + delta_r, head_c + delta_c)

        if self._is_collision(new_head):
            self.state.is_running = False
            self.state.is_paused = True
            return "game_over"

        self.state.snake.append(new_head)
        if new_head == self.state.food:
            self.state.score += 1
            if not self._spawn_food():
                self.state.is_running = False
                self.state.is_paused = True
                return "win"
            return "ate"

        self.state.snake.pop(0)
        return "moved"

    def _dir_to_delta(self, direction: Direction) -> tuple[int, int]:
        return {
            "Up": (-1, 0),
            "Down": (1, 0),
            "Left": (0, -1),
            "Right": (0, 1),
        }[direction]

    def _is_collision(self, pos: Position) -> bool:
        r, c = pos
        if r < 0 or c < 0 or r >= self.rows or c >= self.cols:
            return True
        return pos in self.state.snake

    def _spawn_food(self) -> bool:
        free_cells = [
            (r, c)
            for r in range(self.rows)
            for c in range(self.cols)
            if (r, c) not in self.state.snake
        ]
        if not free_cells:
            return False
        self.state.food = self.rng.choice(free_cells)
        return True

    def _is_opposite(self, new_dir: Direction, current_dir: Direction) -> bool:
        opposites = {
            ("Up", "Down"),
            ("Down", "Up"),
            ("Left", "Right"),
            ("Right", "Left"),
        }
        return (new_dir, current_dir) in opposites
