"""ダークテーマ用スタイルシート定義"""

# カラーパレット
COLOR_BG = "#1a1a2e"          # 背景（濃紺）
COLOR_PANEL = "#16213e"       # パネル背景
COLOR_ACCENT = "#e94560"      # アクセント（赤）
COLOR_TEXT = "#eaeaea"        # テキスト（白系）
COLOR_MUTED = "#a0a0b0"       # サブテキスト（グレー）
COLOR_BTN = "#0f3460"         # ボタン背景（青）
COLOR_BTN_HOVER = "#e94560"   # ボタンホバー

STYLESHEET = f"""
QWidget {{
    background-color: {COLOR_BG};
    color: {COLOR_TEXT};
    font-family: "Meiryo UI", "Yu Gothic UI", sans-serif;
    font-size: 13px;
}}

QLabel {{
    color: {COLOR_TEXT};
}}

QLabel#title {{
    font-size: 18px;
    font-weight: bold;
    color: {COLOR_ACCENT};
}}

QLabel#subtitle {{
    font-size: 14px;
    font-weight: bold;
    color: {COLOR_TEXT};
}}

QLabel#muted {{
    color: {COLOR_MUTED};
    font-size: 11px;
}}

QPushButton {{
    background-color: {COLOR_BTN};
    color: {COLOR_TEXT};
    border: 1px solid {COLOR_ACCENT};
    border-radius: 8px;
    padding: 8px 16px;
    font-size: 13px;
}}

QPushButton:hover {{
    background-color: {COLOR_BTN_HOVER};
    color: #ffffff;
}}

QPushButton:disabled {{
    background-color: #333355;
    color: {COLOR_MUTED};
    border: 1px solid #444466;
}}

QPushButton#card_btn {{
    background-color: {COLOR_PANEL};
    border: 2px solid {COLOR_BTN};
    border-radius: 10px;
    padding: 10px 8px;
    min-width: 90px;
    min-height: 80px;
    font-size: 12px;
    text-align: center;
}}

QPushButton#card_btn:hover {{
    border: 2px solid {COLOR_ACCENT};
    background-color: #1e2a4a;
}}

QPushButton#card_btn:disabled {{
    background-color: #1a1a2e;
    border: 2px solid #333355;
    color: {COLOR_MUTED};
}}

QPushButton#end_turn_btn {{
    background-color: {COLOR_ACCENT};
    color: #ffffff;
    border: none;
    border-radius: 8px;
    padding: 10px 24px;
    font-size: 14px;
    font-weight: bold;
}}

QPushButton#end_turn_btn:hover {{
    background-color: #c73652;
}}

QPushButton#node_btn {{
    background-color: {COLOR_PANEL};
    border: 2px solid {COLOR_BTN};
    border-radius: 10px;
    padding: 14px 28px;
    font-size: 14px;
    min-width: 160px;
}}

QPushButton#node_btn:hover {{
    border: 2px solid {COLOR_ACCENT};
    background-color: #1e2a4a;
}}

QTextEdit {{
    background-color: {COLOR_PANEL};
    color: {COLOR_TEXT};
    border: 1px solid #333355;
    border-radius: 6px;
    padding: 6px;
    font-size: 12px;
}}

QFrame#separator {{
    background-color: {COLOR_ACCENT};
    max-height: 2px;
}}

QFrame#panel {{
    background-color: {COLOR_PANEL};
    border: 1px solid #333355;
    border-radius: 8px;
}}
"""
