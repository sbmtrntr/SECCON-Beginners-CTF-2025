from fastecdsa.curve import secp256k1

# 1) パラメータ
p = secp256k1.p
n = secp256k1.q
b = secp256k1.b
y = 86110314059807694788670006733716000347320501369737360547908334458189062161608

# 2) 立方数判定
m = (y*y - b) % p
k = (p - 1) // 3
if pow(m, k, p) != 1:
    print("この y には対応する x がない")
    exit(1)

# 3) x の計算
d = pow(3, -1, k)
x = pow(m, d, p)

# 4) a の計算
a = n - 1

print("x =", x)
print("a =", a)
