"""ゲーム結果画面ウィジェット"""
from __future__ import annotations

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt, Signal


class ResultScreen(QWidget):
    """ゲームクリア / ゲームオーバー画面"""

    restart_requested = Signal()

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setSpacing(24)
        layout.setContentsMargins(60, 60, 60, 60)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self._result_lbl = QLabel()
        self._result_lbl.setObjectName("title")
        self._result_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self._result_lbl)

        self._message_lbl = QLabel()
        self._message_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self._message_lbl)

        restart_btn = QPushButton("もう一度プレイ")
        restart_btn.clicked.connect(self.restart_requested.emit)
        layout.addWidget(restart_btn, alignment=Qt.AlignmentFlag.AlignHCenter)

    def show_clear(self) -> None:
        self._result_lbl.setText("🎉 ゲームクリア！")
        self._message_lbl.setText("ボスを倒してダンジョンを制覇した！\nおめでとうございます！")

    def show_game_over(self) -> None:
        self._result_lbl.setText("💀 ゲームオーバー")
        self._message_lbl.setText("HPが0になってしまった...\nまた挑戦しよう！")
