# config.json リファレンス

## グローバル設定

| キー | 説明 | デフォルト |
|------|------|-----------|
| `engine` | 使用する CLI エンジン（`claude` / `codex`）。**必須** | なし（未設定時はエラーで起動停止） |
| `novnc_bind_address` | noVNC のバインド先 IP | `localhost` |

## Discord 設定

| キー | 説明 | デフォルト |
|------|------|-----------|
| `discord.enabled` | Discord Bot を起動するか | `false` |
| `discord.model` | モデル名（`sonnet` / `opus` / `haiku`） | `sonnet` |
| `discord.thinking` | 思考モードの有効化 | `false` |
| `discord.skip_permissions` | CLI の権限確認をスキップ | `true` |
| `discord.browser_enabled` | ブラウザ操作機能の有効化 | `false` |
| `discord.browser_cdp_port` | Chrome DevTools Protocol のポート | `9222` |
| `discord.browser_novnc_port` | noVNC Web UI のポート | `6080` |
| `discord.browser_vnc_port` | Xtigervnc の VNC ポート | `5900` |
| `discord.browser_vnc_display` | Xtigervnc の仮想ディスプレイ番号 | `":99"` |
| `discord.allowed_user_ids` | ボットに話しかけられるユーザーの Discord ID（配列） | なし（必須） |
| `discord.heartbeat_enabled` | Heartbeat 自律巡回の有効化 | `false` |
| `discord.heartbeat_channel_id` | Heartbeat 通知を送るチャンネル ID | なし |
| `discord.heartbeat_interval_minutes` | Heartbeat の実行間隔（分） | `60` |
| `discord.heartbeat_thinking` | Heartbeat 専用の Thinking モード | `false` |
| `discord.no_mention_channels` | メンション不要で反応するチャンネル ID（配列） | `[]` |

## Slack 設定

| キー | 説明 | デフォルト |
|------|------|-----------|
| `slack.enabled` | Slack Bot を起動するか | `false` |
| `slack.allowed_user_ids` | ボットに話しかけられるユーザーの Slack ユーザー ID（配列） | なし（必須） |
| `slack.no_mention_channels` | メンション不要で反応するチャンネル ID（配列） | `[]` |
| `slack.browser_enabled` | ブラウザ操作機能の有効化 | `false` |
| `slack.browser_cdp_port` | Chrome DevTools Protocol のポート | `9221` |
| `slack.browser_novnc_port` | noVNC Web UI のポート | `6081` |
| `slack.browser_vnc_port` | Xtigervnc の VNC ポート | `5901` |
| `slack.browser_vnc_display` | Xtigervnc の仮想ディスプレイ番号 | `":100"` |
| `slack.reply_in_thread` | メッセージをスレッドで返信するか（`false` でチャンネルに直接投稿） | `true` |
| `slack.heartbeat_thinking` | Heartbeat 専用の Thinking モード | `false` |

## マルチプラットフォーム

プラットフォームごとに独立したワークスペース（人格・記憶・設定）を持つ設計。`enabled` フラグで起動するプラットフォームを制御する。

新しいプラットフォーム用ワークスペースを初期化（例: discord の記憶を slack に移植）:

```bash
sudo su - clive
source venv/bin/activate
python3 main.py --init-workspace slack --from discord
deactivate
exit
```

コピー後に `platforms/slack/workspace/SOUL.md` を編集してプラットフォームに合った人格に調整する。
