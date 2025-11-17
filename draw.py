"""描画処理をまとめたもの"""
# キャンバスとコンテキストの取得 --- (*1)
canvas = q("#game-canvas")
ctx = canvas.getContext("2d")

def draw():
    """ゲーム画面全体の描画"""  # --- (*2)
    ctx.fillStyle = "#101010"
    ctx.fillRect(0, 0, canvas.width, canvas.height)
    # 描画済みのタイルと現在のピース --- (*3)
    for r in range(ROWS):
        for c in range(COLS):
            color_index = game["board"][r][c]
            if color_index is not None:
                draw_cell(r, c, COLORS[color_index])
    # グリッドを描画 --- (*4)
    ctx.strokeStyle = "rgba(255, 255, 255, 0.4)"
    ctx.lineWidth = 1
    for r in range(ROWS + 1):
        ctx.beginPath()
        ctx.moveTo(0, r * CELL_SIZE)
        ctx.lineTo(canvas.width, r * CELL_SIZE)
        ctx.stroke()
    for c in range(COLS + 1):
        ctx.beginPath()
        ctx.moveTo(c * CELL_SIZE, 0)
        ctx.lineTo(c * CELL_SIZE, canvas.height)
        ctx.stroke()
    # 落下中のピースがあれば描画 --- (*5)
    piece = game["piece"]
    if piece is not None:
        for r, c in piece["cells"]:
            draw_cell(r, c, COLORS[piece["color_index"]])

def draw_cell(r, c, color):
    """指定されたセル位置にタイルを描画"""  # --- (*6)
    x, y, p = c * CELL_SIZE, r * CELL_SIZE, 2
    ctx.fillStyle = color
    ctx.fillRect(x + p, y + p, CELL_SIZE - p * 2, CELL_SIZE - p * 2)
    ctx.strokeStyle = "rgba(255, 255, 255, 0.15)"
    ctx.strokeRect(x + p, y + p, CELL_SIZE - p * 2, CELL_SIZE - p * 2)

def update_panels():
    """スコアやレベル表示の更新"""  # --- (*7)
    q_text("#score", str(game["score"]))
    q_text("#cleared", str(game["cleared_blocks"]))
