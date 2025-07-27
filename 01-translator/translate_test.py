import socket
import binascii

def query(trans_0, trans_1):
    # 接続先
    host = "01-translator.challenges.beginners.seccon.jp"
    port = 9999
    
    # ソケット接続
    with socket.create_connection((host, port)) as sock:
        # 入力を順に送る
        sock.recv(1024)
        sock.sendall((trans_0 + '\n').encode())

        sock.recv(1024)
        sock.sendall((trans_1 + '\n').encode())

        # 出力を受け取る
        response = sock.recv(4096).decode()
        ct_hex = response.split('ct: ')[1].strip()
        return ct_hex

# 実験: 同じ文字を指定 → 同じビット列になったときのエンコードを見る
ct1 = query('a', 'a')
ct2 = query('a', 'b')
ct3 = query('a', 'c')
ct4 = query('a', 'd')

# 16バイト（32文字のhex）ごとに分割
def split_blocks(ct_hex):
    return [ct_hex[i:i+32] for i in range(0, len(ct_hex), 32)]

print("a/a", split_blocks(ct1))
print("a/b", split_blocks(ct2))
print("a/c", split_blocks(ct3))
print("a/d", split_blocks(ct4))
