"""ユーザーインターフェース関連の処理をまとめたもの"""
def handle_key(event):
    """キーボード入力のハンドラ"""  # --- (*1)
    # キーごとの処理を辞書型で定義 --- (*2)
    key_handlers = {
        "ArrowLeft": on_move_left,  # [←]で左移動
        "ArrowRight": on_move_right,  # [→]で右移動
        "ArrowDown": lambda e: tick(),  # [↓]で下移動
        "ArrowUp": on_rotate,  # [↑]で回転
        " ": hard_drop_piece,  # スペースキーで一気に落下
        "r": on_restart_game,  # Rキーでリスタート
    }
    # 対応するキーが押されたら実行 --- (*3)
    if event.key in key_handlers:
        event.preventDefault()  # デフォルトの動作を抑制
        key_handlers[event.key](event)  # 実行

# キーボード入力のハンドラを登録 --- (*4)
js.document.addEventListener("keydown", handle_key)

# --- ピースの移動や回転などの処理 ---

def move_h(dcol):
    """ピースを左右に移動させる"""  # --- (*5)
    if game["piece"] is not None and not game["game_over"]:
        move_piece(game["piece"], 0, dcol)
        draw()

def on_rotate(event):
    """回転処理"""  # --- (*6)
    if game["piece"] is not None and not game["game_over"]:
        rotate_piece(game["piece"])
        draw()

def on_restart_game(event):
    """Rキー押下時のゲームリスタート処理"""  # --- (*7)
    if game["game_over"]:
        reset_game()

def hard_drop_piece(event):
    """ピースを一気に落下させる処理"""  # --- (*8)
    while move_piece(game["piece"], 1, 0):
        pass

# ピースの左右移動用の関数を定義 --- (*9)
on_move_left = lambda e: move_h(-1)
on_move_right = lambda e: move_h(1)

# ボタンクリック時のイベントハンドラ --- (*10)
q("#btn-rotate").addEventListener("click", on_rotate)
q("#btn-left").addEventListener("click", on_move_left)
q("#btn-right").addEventListener("click", on_move_right)
