"""マップ画面ウィジェット"""
from __future__ import annotations
from typing import TYPE_CHECKING

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QSpacerItem, QSizePolicy,
)
from PySide6.QtCore import Qt, Signal

if TYPE_CHECKING:
    from src.models.game import Game
from src.models.map_node import Node


class MapScreen(QWidget):
    """マップ画面（次のノードを選択する）"""

    # ノード選択シグナル
    node_selected = Signal(object)  # Node

    def __init__(self, game: "Game", parent: QWidget | None = None):
        super().__init__(parent)
        self.game = game
        self._setup_ui()

    # ------------------------------------------------------------------ #
    # UI構築
    # ------------------------------------------------------------------ #

    def _setup_ui(self) -> None:
        self._root = QVBoxLayout(self)
        self._root.setSpacing(16)
        self._root.setContentsMargins(40, 40, 40, 40)
        self._root.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

        self._title_lbl = QLabel("次の行動を選択")
        self._title_lbl.setObjectName("title")
        self._title_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._root.addWidget(self._title_lbl)

        self._status_lbl = QLabel()
        self._status_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._root.addWidget(self._status_lbl)

        self._root.addSpacerItem(QSpacerItem(0, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))

        # ノードボタンを格納するコンテナ（動的に再構築）
        self._btn_container = QVBoxLayout()
        self._btn_container.setSpacing(12)
        self._btn_container.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self._root.addLayout(self._btn_container)

    # ------------------------------------------------------------------ #
    # 表示更新
    # ------------------------------------------------------------------ #

    def refresh(self) -> None:
        """現在のゲーム状態に合わせてノードボタンを再構築する"""
        g = self.game

        # ステータス表示
        self._status_lbl.setText(
            f"❤ HP: {g.player_hp} / {g.player_max_hp}　　"
            f"山札: {len(g.deck)}枚　捨て札: {len(g.discard)}枚"
        )

        # 既存ボタンを削除
        while self._btn_container.count():
            item = self._btn_container.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        next_nodes = g.next_nodes
        if not next_nodes:
            lbl = QLabel("進める場所がありません")
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self._btn_container.addWidget(lbl)
            return

        for node in next_nodes:
            btn = self._make_node_button(node)
            self._btn_container.addWidget(btn, alignment=Qt.AlignmentFlag.AlignHCenter)

    def _make_node_button(self, node: Node) -> QPushButton:
        icon = {
            "battle": "⚔",
            "elite": "💀",
            "rest": "🏕",
            "boss": "👑",
        }.get(node.type, "❓")

        btn = QPushButton(f"{icon}  {node.label}")
        btn.setObjectName("node_btn")
        btn.clicked.connect(lambda checked=False, n=node: self._on_node_selected(n))
        return btn

    # ------------------------------------------------------------------ #
    # イベントハンドラ
    # ------------------------------------------------------------------ #

    def _on_node_selected(self, node: Node) -> None:
        self.node_selected.emit(node)
