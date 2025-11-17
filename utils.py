import js

def q(query):
    """簡単にHTML要素を取得する関数"""  # --- (*1)
    return js.document.querySelector(query)

def q_text(query, text):
    """指定した要素のテキストを設定する関数"""  # --- (*2)
    q(query).innerText = text

def set_timeout(f, ms):
    """タイマーを設定する関数"""  # --- (*3)
    return js.setTimeout(f, ms)
