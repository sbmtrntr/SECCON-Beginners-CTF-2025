#!/usr/bin/env python3
import socket
import sys


def recv_until(sock, delim):
    """
    ソケットから delim バイト列が出現するまで受信し続ける
    """
    data = b''
    while not data.endswith(delim):
        chunk = sock.recv(1)
        if not chunk:
            break
        data += chunk
    return data


def main():
    # 引数チェック
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} HOST PORT")
        sys.exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2])

    # 0 と 1 のマッピング文字列（16バイトずつ）
    trans0 = b"A" * 16
    trans1 = b"B" * 16

    # サービスへ接続
    with socket.create_connection((host, port)) as sock:
        # プロンプトを読み飛ばしてマッピング送信
        recv_until(sock, b"translations for 0>")
        sock.sendall(trans0 + b"\n")

        recv_until(sock, b"translations for 1>")
        sock.sendall(trans1 + b"\n")

        # 暗号文行を受信
        line = recv_until(sock, b"\n").decode().strip()

    # 正しい形式か確認
    if not line.startswith("ct:"):
        print("Failed to get ciphertext:", line)
        sys.exit(1)

    # 16進文字列 → バイト列
    ct_hex = line.split("ct:")[1].strip()
    ct = bytes.fromhex(ct_hex)

    # 16バイトずつのブロックに分割し、最後のパディングブロックを削除
    blocks = [ct[i:i+16] for i in range(0, len(ct), 16)]
    blocks = blocks[:-1]

    # 最初のブロックは必ず "1" に対応
    block_one = blocks[0]
    # 他のブロックから "0" 対応を抽出
    uniq = set(blocks)
    uniq.discard(block_one)
    if len(uniq) != 1:
        print("Unexpected number of distinct blocks:", len(uniq)+1)
        sys.exit(1)
    block_zero = uniq.pop()

    # 各ブロックを比較してビット列を復元
    bits = ''.join('1' if b == block_one else '0' for b in blocks)

    # ビット列 → 整数 → バイト列 → デコード
    flag_int = int(bits, 2)
    flag_bytes = flag_int.to_bytes((len(bits)+7)//8, 'big')
    try:
        flag = flag_bytes.decode()
    except UnicodeDecodeError:
        flag = flag_bytes

    print("Recovered flag:", flag)


if __name__ == "__main__":
    main()
