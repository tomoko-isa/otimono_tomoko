"""落ちものパズルゲームのメインロジック"""
import random

# 定数の宣言 --- (*1)
CLEAR_THRESHOLD = 9  # タイルを消去するために必要な隣接タイル数
DROP_INTERVAL = 600  # ピースが落ちる速度(ミリ秒)
ROWS, COLS = 15, 12  # ステージの行数と列数
CELL_SIZE = 30  # セルのサイズ(ピクセル)
COLORS = ["#d1495b", "#4d9de0", "#35a148",
          "#a05195", "#f2c14e"]  # ピースの色(赤, 青, 緑, 紫, 黄)

# ゲーム状態を表す変数 --- (*2)
game = {
    "board": [],  # 2次元でステージの状態を保持
    "piece": None,  # 落下するピース
    "score": 0,  # スコア
    "cleared_blocks": 0,  # クリアしたブロック数
    "game_over": False,  # ゲームオーバー状態の管理
}

def reset_game():
    """ゲーム全体の初期化"""  # --- (*3)
    game["board"] = [[None for _ in range(COLS)] for _ in range(ROWS)]
    fill_initial_blocks()  # 画面下層にランダムな色ブロックを配置
    game["game_over"] = False  # ゲームオーバー状態をリセット
    game["score"] = game["cleared_blocks"] = 0  # スコアを初期化
    game["piece"] = None  # 現在のピースをクリア
    q_text("#message", "")
    draw()
    update_panels()
    start_timer()  # ピースを落とすタイマーを開始

def start_timer():
    """一定時間ごとに実行するタイマー処理"""  # --- (*4)
    if game["game_over"]:
        return
    tick()  # ピースを落下させる処理を定期的に実行
    set_timeout(start_timer, DROP_INTERVAL)  # タイマーを再設定

def tick():
    """一定時間ごとにピースを落下させる処理"""  # --- (*5)
    if game["piece"] is None:  # ピースがないなら生成
        spawn_new_piece()
        if game["game_over"]:  # ゲームオーバーなら終了
            return
    moved = move_piece(game["piece"], 1, 0)  # ピースを下に移動 --- (*6)
    if not moved:  # 移動できない?
        lock_piece()  # ピースの固定処理
        resolve_board()  # ブロックを消す処理
        spawn_new_piece()  # 新しいピースを生成
    draw()

def spawn_new_piece():
    """新しいピースを生成"""  # --- (*7)
    candidate = create_piece()
    if can_place(candidate["cells"]):  # ピースが置ける？
        game["piece"] = candidate
    else:
        game["piece"] = None  # ピースを置けないならゲームオーバー
        game["game_over"] = True
        q_text("#message", "Game Over! Rキーで再スタート")

def resolve_board():
    """ボード上のタイルの消去と得点計算""" # --- (*8)
    total_cleared = 0
    while True:
        groups = find_groups()
        if not groups:
            break
        for r, c in groups:
            game["board"][r][c] = None
        total_cleared += len(groups)
        game["score"] += len(groups) * 10
        game["cleared_blocks"] += len(groups)
        apply_gravity()
    if total_cleared:
        update_panels()

def fill_initial_blocks():
    """ゲーム開始時に下3段をランダムな色で埋める"""  # --- (*9)
    for r in range(ROWS - 3, ROWS):
        for c in range(COLS):
            game["board"][r][c] = random.randrange(len(COLORS))

reset_game()
