# セキュリティ

AI エンジンは `--dangerously-skip-permissions` 相当のオプションで動作し、任意のコマンドを実行できる。以下の多層防御で被害を限定する。

## 専用ユーザーによる分離

`clive` 専用ユーザーで実行することで、他のユーザーのファイルやプロセスへのアクセスを OS レベルで制限する。

## systemd サンドボックス

`clive.service` に以下のサンドボックス設定が含まれる:

| 設定 | 効果 |
|------|------|
| `ProtectSystem=strict` | `/usr`, `/etc` 等のシステムファイルへの書き込みを禁止 |
| `ReadWritePaths=/home/clive` | clive の home だけ書き込み許可 |
| `PrivateTmp=true` | `/tmp` を他プロセスと分離（覗き見できない） |
| `NoNewPrivileges=true` | 権限昇格（sudo 等）を禁止 |
| `ProtectHome=true` | clive 以外の `/home/*` への読み取りを禁止 |
| `ProtectKernelTunables=true` | `/proc/sys` 等のカーネルパラメータ変更を禁止 |
| `ProtectControlGroups=true` | cgroup の変更を禁止 |
| `CapabilityBoundingSet=` | すべての Linux ケーパビリティを剥奪 |

これにより AI エンジンが任意コマンドを実行しても:

- `/home/clive` の外に書き込めない
- 他ユーザーのファイルが見えない（読めない）
- root 権限を取得できない
- カーネルパラメータを変更できない

> **注意:** `CapabilityBoundingSet=` を設定するとプロセスがユーザー名前空間を作成できなくなる。Chrome の内部サンドボックスがこの制約に引っかかるため、Chrome 側は `--no-sandbox` オプションでサンドボックス生成をスキップしている。

## .env のセキュリティ

`.env` は root 所有・600 権限で配置し、clive ユーザーがファイルを直接読めないようにする。systemd の `EnvironmentFile` ディレクティブが起動時に展開して環境変数として渡す。

```bash
sudo chown root:root /home/clive/.env
sudo chmod 600 /home/clive/.env
```

開発時に手元で直接実行する場合は `.env.local` を clive ユーザーで用意する。

## ブラウザ操作のリスク

ブラウザ操作を有効にすると、AI は Chrome の Cookie にアクセスできる（= ログイン済みサービスの操作権限を持つ）。`allowed_user_ids` で操作を許可するユーザーを限定し、不要なサービスにはログインしないこと。

## noVNC のアクセス制限

`novnc_bind_address` を `0.0.0.0` にすると、VNC パスワードだけでインターネット上の誰でもブラウザ画面にアクセスできてしまう。Tailscale や SSH トンネル経由でのアクセスを推奨する（詳細は [browser.md](browser.md) を参照）。
