import socket
import binascii

# ソケットでクエリを送信して暗号文を取得する関数
def query(trans_0, trans_1):
    host = "01-translator.challenges.beginners.seccon.jp"
    port = 9999
    
    with socket.create_connection((host, port)) as sock:
        # サーバーからの初期メッセージを受信
        sock.recv(1024)
        
        # trans_0, trans_1 を順番に送信
        sock.sendall((trans_0 + '\n').encode())
        sock.recv(1024)  # 応答を受け取る（不要なら省略可能）
        
        sock.sendall((trans_1 + '\n').encode())
        response = sock.recv(4096).decode()  # 応答を受け取る

        # 暗号文を抽出
        ct_hex = response.split('ct: ')[1].strip()
        return ct_hex

# フラグの長さを確認するためにクエリを送る関数
def get_flag_length():
    for length in range(1, 50):  # 50バイトくらいを仮定
        print(f"試行: {length} バイト")
        
        # クエリを送信して暗号文を得る
        ct = query("a", "b")  # 任意のtrans_0, trans_1
        ct_len = len(bytes.fromhex(ct))  # 暗号文の長さを取得
        
        if ct_len == length:
            print(f"フラグの長さ: {length} バイト")
            return length
    return 0

# フラグのバイナリを復元する関数
def recover_flag(flag_length):
    flag_bin = ""
    
    # 各ビットを復元
    for i in range(flag_length * 8):  # 1ビットずつ復元
        print(f"復元中: ビット {i + 1}/{flag_length * 8}")
        
        # 最初のクエリ
        ct1 = query('a', 'b')
        ct1_bytes = bytes.fromhex(ct1)
        
        # 2回目のクエリ
        ct2 = query('a', 'c')
        ct2_bytes = bytes.fromhex(ct2)
        
        # 暗号文の一致を比較してビットを推測
        if ct1_bytes == ct2_bytes:
            flag_bin += "0"  # 暗号文が一致 → ビットは 0
        else:
            flag_bin += "1"  # 暗号文が異なる → ビットは 1
    
    return flag_bin

# バイナリ列を文字列に変換
def bin_to_string(flag_bin):
    flag = ''.join(chr(int(flag_bin[i:i+8], 2)) for i in range(0, len(flag_bin), 8))
    return flag

# 実行部分
def main():
    flag_length = get_flag_length()  # フラグの長さを取得
    if flag_length == 0:
        print("フラグの長さを特定できませんでした。")
        return
    
    print(f"フラグの長さ: {flag_length} バイト")
    
    # フラグのバイナリ列を復元
    flag_bin = recover_flag(flag_length)
    
    # バイナリ列を文字列に変換して表示
    flag = bin_to_string(flag_bin)
    print(f"復元したフラグ: {flag}")

# 実行
if __name__ == "__main__":
    main()
