# コマンド一覧

Discord はプレフィックスなし（`/model`）、Slack は `-ai` サフィックス付き（`/model-ai`）。

## 基本操作

| Discord | Slack | 説明 |
|---------|-------|------|
| `@bot メッセージ` | `@bot メッセージ` | AI と会話（画像・PDF の添付も可） |
| `/model` | `/model-ai` | モデル（Sonnet / Opus / Haiku）と Thinking ON/OFF を設定 |
| `/status` | `/status-ai` | 現在のモデル・Thinking・実行中タスクの確認（Slack はスレッド返信 ON/OFF も設定可） |
| `/cancel` | `/cancel-ai` | 現在のチャンネルで実行中のプロセスを中止 |
| `/reset` | `/reset-ai` | 会話セッションをリセット（次のメッセージから新しい会話が始まる） |
| `/mention` | `/mention-ai` | このチャンネルでのメンション要否を設定（OFF にするとメンションなしで反応） |

## スケジュール

| Discord | Slack | 説明 |
|---------|-------|------|
| `/schedule add` | `/schedule-ai add` | 定期実行タスクの追加（UI フォーム） |
| `/schedule list` | `/schedule-ai list` | 登録済みスケジュールの一覧・編集・一時停止・削除 |

## 分析

| Discord | Slack | 説明 |
|---------|-------|------|
| `/summarize [prompt]` | `/summarize-ai [prompt]` | チャンネルの会話を AI に質問・要約（カスタムプロンプト対応） |

## Heartbeat

| Discord | Slack | 説明 |
|---------|-------|------|
| `/heartbeat` | `/heartbeat-ai` | Heartbeat のステータス表示・設定変更・手動実行（Slack は Heartbeat 専用 Thinking モードも設定可） |

## レビュー

| Discord | Slack | 説明 |
|---------|-------|------|
| `/review` | `/review-ai` | 調査済みトピックのレビュー・フィードバック |

## スキル

| Discord | Slack | 説明 |
|---------|-------|------|
| `/skills-list` | `/skills-list` | 利用可能なスキル一覧を表示し、ボタンで選択して発動する（新規作成スキルも再起動不要で認識） |

---

> **Slack のみ:**  Slack App のマニフェストへの登録が必要。[slack-bot-setup.md](slack-bot-setup.md) を参照。
