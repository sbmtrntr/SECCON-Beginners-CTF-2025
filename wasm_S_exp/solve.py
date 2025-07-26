import re

def stir(x: int) -> int:
    # スクランブル関数そのまま実装
    return 1024 + ((23 + 37 * (x ^ 0x5A5A)) % 101)

def main():
    # .wat ファイルを読み込み
    with open('check_flag.wat', 'r', encoding='utf-8') as f:
        lines = f.readlines()

    pairs = []
    # check_flag 部分の "i32.const C" / "i32.const x" / "call $stir" の
    # パターンを拾って (x, C) のタプルを収集
    for i in range(len(lines) - 2):
        m0 = re.match(r'\s*i32\.const\s+(0x[0-9A-Fa-f]+|\d+)', lines[i])
        m1 = re.match(r'\s*i32\.const\s+(0x[0-9A-Fa-f]+|\d+)', lines[i+1])
        if m0 and m1 and 'call $stir' in lines[i+2]:
            C = int(m0.group(1), 0)
            x = int(m1.group(1), 0)
            pairs.append((x, C))

    # フラグ長は 25 文字（j=0..24）なので空リストを用意
    flag_chars = ['?'] * 25
    for x, C in pairs:
        addr = stir(x)
        j = addr - 1024
        flag_chars[j] = chr(C)

    flag = ''.join(flag_chars)
    print(flag)

if __name__ == '__main__':
    main()