## 本リポジトリの運用手順
### Issueでの問題管理
- タイトルに問題名を書く
- スレッドに調べたこと/解法手順/答え(フラグ)等を書いていく

### ファイルでの問題管理
- ファイル名を問題名にする
  - 問題名が日本語の場合も同様
- 解答に使った/途中まで書いたコードをアップする

## GitHubの使い方
### 最初だけ
```
git init
git branch -M main
git remote add origin https://github.com/sbmtrntr/SECCON-Beginners-CTF-2025.git
```

### ファイルアップするときの手順
今回はブランチ分けず、mainだけ使う
```
git add <変更したファイル>
git commit -m "やったこと"
git push origin main
```