# アンインストール

Clive を完全に削除する手順。root ユーザーで実行する。

## 1. サービスの停止・削除

```bash
sudo systemctl stop clive
sudo systemctl disable clive
sudo rm /etc/systemd/system/clive.service
sudo systemctl daemon-reload
```

## 2. clive ユーザーとホームディレクトリの削除

ホームディレクトリごと削除（config.json, .env, workspace/ 等すべて消える）:

```bash
sudo userdel -r clive
```

> `-r` を外すとユーザーだけ消してデータを残せる。`/home/clive/` は手動で削除可能。

## 3. Chrome プロファイルの削除

ブラウザ操作を使っていた場合、Cookie やログイン情報が残っている:

```bash
sudo rm -rf /home/clive/.config/clive-chrome-discord
sudo rm -rf /home/clive/.config/clive-chrome-slack
```

> Step 2 で `-r` を付けて削除済みなら不要。

## 4. VPS 向けパッケージの削除（任意）

ブラウザ操作用にインストールしたパッケージが不要なら:

```bash
sudo apt remove --purge tigervnc-standalone-server novnc google-chrome-stable
sudo apt autoremove
```

> `fonts-noto-cjk` は他のアプリでも使われるため残しておいてよい。完全に消したい場合は `sudo apt remove fonts-noto-cjk`。
