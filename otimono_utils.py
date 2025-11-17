"""落ちものゲーム固有の便利関数"""
def create_piece():
    """新しいピースを辞書として作成"""  # --- (*1)
    color_index = random.randrange(len(COLORS))  # ピースの色をランダムに決定
    orientation = random.choice(["縦", "横"])  # ピース形状をランダムに決定
    start_col = COLS // 2  # 中央寄せで開始位置を決定
    if orientation == "横":  # 横の配置の場合
        cells = [(0, start_col), (0, start_col + 1)]
    else:  # 縦の配置の場合
        cells = [(0, start_col), (1, start_col)]
    return {"cells": cells, "color_index": color_index}

def move_piece(piece, drow, dcol):
    """ピースを指定方向に移動させる"""  # --- (*2)
    new_cells = [(r + drow, c + dcol) for r, c in piece["cells"]]
    if can_place(new_cells):
        piece["cells"] = sorted(new_cells)
        return True
    return False

def get_rotated_cells(piece):
    """ピースのセルを回転させた位置のリストを返す"""  # --- (*3)
    cells = piece["cells"]
    anchor, other = cells[0], cells[1]
    if anchor[0] == other[0]:  # 横向きなら縦向きへ --- (*4)
        candidate = [anchor, (anchor[0] + 1, anchor[1])]
    else:  # 縦向きなら横向きへ
        candidate = [anchor, (anchor[0], anchor[1] + 1)]
    return candidate

def rotate_piece(piece):
    """ピースを回転させる"""  # --- (*5)
    rotated = get_rotated_cells(piece)
    if can_place(rotated):
        piece["cells"] = rotated

def can_place(cells):
    """指定されたセル位置にピースを置けるかどうかを判定"""  # --- (*6)
    for r, c in cells:
        if c < 0 or c >= COLS or r < 0 or r >= ROWS:
            return False
        if game["board"][r][c] is not None:
            return False
    return True

def lock_piece():
    """現在のピースをステージに固定する"""  # --- (*7)
    piece = game["piece"]
    for r, c in piece["cells"]:
        if 0 <= r < ROWS and 0 <= c < COLS:
            game["board"][r][c] = piece["color_index"]
    game["piece"] = None

def flood_fill(r, c, color, group):
    """再帰的に指定位置から同じ色の隣接タイルを探索"""  # --- (*8)
    if (r, c) in group:  # 既に探索済みか
        return
    if r < 0 or r >= ROWS or c < 0 or c >= COLS:  # 範囲外か
        return
    if game["board"][r][c] != color:  # 色が違うか
        return
    group.add((r, c))  # 指定位置をグループに追加
    # 引き続き上下左右を再帰的に探索 --- (*9)
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        flood_fill(r + dr, c + dc, color, group)  # 再帰呼び出し

def find_groups():
    """隣接する同色タイルを数えて消去対象として返す"""  # --- (*10)
    to_clear, visited = set(), set()
    # 全セルを走査して隣接グループを探す
    for r in range(ROWS):
        for c in range(COLS):
            if (r, c) in visited or game["board"][r][c] is None:
                continue
            # 隣接するタイルで同じ色のものを探索 --- (*11)
            group = set()
            flood_fill(r, c, game["board"][r][c], group)
            visited.update(group)
            # CLEAR_THRESHOLD以上なら消去対象に追加
            if len(group) >= CLEAR_THRESHOLD:
                to_clear.update(group)
    return to_clear

def apply_gravity():
    """タイルを下に落とす処理"""  # --- (*12)
    for c in range(COLS):
        stack = []
        for r in range(ROWS - 1, -1, -1):
            color = game["board"][r][c]
            if color is not None:
                stack.append(color)
        idx = 0
        for r in range(ROWS - 1, -1, -1):
            if idx < len(stack):
                game["board"][r][c] = stack[idx]
                idx += 1
            else:
                game["board"][r][c] = None
