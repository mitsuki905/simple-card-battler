"""メインウィンドウ（画面遷移管理）"""
from __future__ import annotations

from PySide6.QtWidgets import QMainWindow, QStackedWidget
from PySide6.QtCore import Qt

from src.models.game import Game
from src.models.map_node import Node, NODE_REST
from src.gui.battle_screen import BattleScreen
from src.gui.map_screen import MapScreen
from src.gui.result_screen import ResultScreen
from src.gui.styles import STYLESHEET

# 画面インデックス
IDX_MAP = 0
IDX_BATTLE = 1
IDX_RESULT = 2


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Card Battler")
        self.setMinimumSize(700, 600)
        self.setStyleSheet(STYLESHEET)

        self._game = Game()
        self._stack = QStackedWidget()
        self.setCentralWidget(self._stack)

        self._map_screen = MapScreen(self._game)
        self._battle_screen: BattleScreen | None = None
        self._result_screen = ResultScreen()

        # マップ画面を追加（index 0）
        self._stack.addWidget(self._map_screen)
        # 戦闘画面のプレースホルダ（index 1）
        self._stack.addWidget(QStackedWidget())  # 後で差し替え
        # 結果画面（index 2）
        self._stack.addWidget(self._result_screen)

        # シグナル接続
        self._map_screen.node_selected.connect(self._on_node_selected)
        self._result_screen.restart_requested.connect(self._on_restart)

        # 最初のマップ画面を表示
        self._show_map()

    # ------------------------------------------------------------------ #
    # 画面遷移
    # ------------------------------------------------------------------ #

    def _show_map(self) -> None:
        self._map_screen.refresh()
        self._stack.setCurrentIndex(IDX_MAP)

    def _show_battle(self) -> None:
        # 既存の戦闘画面を削除して新規作成
        if self._battle_screen is not None:
            self._stack.removeWidget(self._battle_screen)
            self._battle_screen.deleteLater()

        self._battle_screen = BattleScreen(self._game)
        self._battle_screen.battle_ended.connect(self._on_battle_ended)
        self._stack.insertWidget(IDX_BATTLE, self._battle_screen)
        self._stack.setCurrentIndex(IDX_BATTLE)

    def _show_result(self, cleared: bool) -> None:
        if cleared:
            self._result_screen.show_clear()
        else:
            self._result_screen.show_game_over()
        self._stack.setCurrentIndex(IDX_RESULT)

    # ------------------------------------------------------------------ #
    # イベントハンドラ
    # ------------------------------------------------------------------ #

    def _on_node_selected(self, node: Node) -> None:
        self._game.enter_node(node)

        if node.type == NODE_REST:
            # 休憩ノードは即マップへ戻る
            self._show_map()
        else:
            # 戦闘ノード
            self._show_battle()

    def _on_battle_ended(self, victory: bool) -> None:
        g = self._game
        if g.game_clear:
            self._show_result(True)
        elif g.game_over:
            self._show_result(False)
        else:
            # 通常勝利 → マップへ
            self._show_map()

    def _on_restart(self) -> None:
        """ゲームをリセットして最初から"""
        self._game = Game()

        # 画面を再生成
        old_map = self._map_screen
        self._map_screen = MapScreen(self._game)
        self._map_screen.node_selected.connect(self._on_node_selected)
        self._stack.insertWidget(IDX_MAP, self._map_screen)
        self._stack.removeWidget(old_map)
        old_map.deleteLater()

        if self._battle_screen is not None:
            self._stack.removeWidget(self._battle_screen)
            self._battle_screen.deleteLater()
            self._battle_screen = None

        self._show_map()
