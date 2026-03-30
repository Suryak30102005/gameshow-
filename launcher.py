from __future__ import annotations

import subprocess
import sys
import threading
import time
import tkinter as tk
from dataclasses import dataclass
from tkinter import messagebox

from shared import GAME_PATHS, GameMode

try:
    import speech_recognition as sr
except Exception:
    sr = None


@dataclass
class GameCard:
    mode: GameMode
    label: str
    phrase: tuple[str, ...]


CARDS = [
    GameCard(GameMode.FLAPPY, "Flappy Bird", ("flappy", "flappy bird")),
    GameCard(GameMode.MARIO, "Super Mario", ("mario", "super mario")),
    GameCard(GameMode.SNAKE, "OG Snake", ("snake", "og snake")),
    GameCard(GameMode.PACMAN, "Pac-Man", ("pacman", "pac man")),
]


class FacePlayLauncher(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("FacePlay Launcher")
        self.geometry("680x380")
        self.current_idx = 0
        self.game_proc: subprocess.Popen[str] | None = None
        self.controller_proc: subprocess.Popen[str] | None = None
        self.voice_enabled = tk.BooleanVar(value=sr is not None)
        self.status = tk.StringVar(value="Ready. Select a game and launch.")
        self._build_ui()
        self._refresh_cards()
        self._start_voice_thread_if_enabled()

    def _build_ui(self) -> None:
        title = tk.Label(self, text="FacePlay", font=("Segoe UI", 26, "bold"))
        title.pack(pady=12)

        self.card_frame = tk.Frame(self)
        self.card_frame.pack(fill="x", padx=14)
        self.card_labels: list[tk.Label] = []
        for _ in CARDS:
            lbl = tk.Label(self.card_frame, text="", width=15, height=5, relief="ridge", font=("Segoe UI", 12))
            lbl.pack(side="left", expand=True, fill="both", padx=6)
            self.card_labels.append(lbl)

        controls = tk.Frame(self)
        controls.pack(pady=10)
        tk.Button(controls, text="←", command=lambda: self.shift(-1), width=6).pack(side="left", padx=4)
        tk.Button(controls, text="→", command=lambda: self.shift(1), width=6).pack(side="left", padx=4)
        tk.Button(controls, text="Launch", command=self.launch_selected, width=10).pack(side="left", padx=6)

        tk.Checkbutton(self, text="Enable voice selection", variable=self.voice_enabled, command=self._start_voice_thread_if_enabled).pack()
        tk.Label(self, textvariable=self.status).pack(pady=10)

    def shift(self, delta: int) -> None:
        self.current_idx = (self.current_idx + delta) % len(CARDS)
        self._refresh_cards()

    def _refresh_cards(self) -> None:
        for i, card in enumerate(CARDS):
            active = i == self.current_idx
            self.card_labels[i]["text"] = card.label
            self.card_labels[i]["bg"] = "#70c7ff" if active else "#ececec"

    def launch_selected(self) -> None:
        if self.game_proc and self.game_proc.poll() is None:
            messagebox.showinfo("FacePlay", "A game is already running.")
            return
        selected = CARDS[self.current_idx].mode
        self.status.set(f"Launching {selected.value}...")

        self.controller_proc = subprocess.Popen([sys.executable, "main.py", "--mode", selected.value])
        self.game_proc = subprocess.Popen([sys.executable, GAME_PATHS[selected]])
        threading.Thread(target=self._monitor_game, daemon=True).start()

    def _monitor_game(self) -> None:
        if not self.game_proc:
            return
        self.game_proc.wait()
        if self.controller_proc and self.controller_proc.poll() is None:
            self.controller_proc.terminate()
        self.status.set("Game closed. Back to launcher.")

    def _start_voice_thread_if_enabled(self) -> None:
        if not self.voice_enabled.get() or sr is None:
            return
        threading.Thread(target=self._voice_loop, daemon=True).start()

    def _voice_loop(self) -> None:
        recog = sr.Recognizer()
        mic = sr.Microphone()
        while self.voice_enabled.get():
            try:
                with mic as source:
                    audio = recog.listen(source, timeout=2, phrase_time_limit=2)
                text = recog.recognize_google(audio).lower()
            except Exception:
                continue

            for i, card in enumerate(CARDS):
                if any(p in text for p in card.phrase):
                    self.current_idx = i
                    self._refresh_cards()
                    self.status.set(f"Voice selected: {card.label}")
                    break
            if "select" in text or "go" in text:
                self.after(0, self.launch_selected)
            time.sleep(0.2)


if __name__ == "__main__":
    FacePlayLauncher().mainloop()
