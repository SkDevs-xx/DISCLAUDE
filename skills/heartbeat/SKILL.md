---
name: heartbeat
description: 定期的な自律チェックと状態報告
platforms: [discord, slack]
user-invocable: false
---

# Heartbeat Instructions

HEARTBEAT.md のチェックリストを評価し、以下のルールに従って応答してください。

## 応答ルール

- wrapup の実行が必要な場合は `WRAPUP_NEEDED` を含めてください
- すべて問題なく報告事項がなければ `HEARTBEAT_OK` だけを返してください
- 報告事項がある場合は内容を日本語で送信してください（HEARTBEAT_OK は使わない）

## チェックリスト評価

チェックリストに厳密に従い、推測や過去の会話からタスクを作り出さないでください。
報告事項がなければサイレントに OK を返すのが正しい動作です。
