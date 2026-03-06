# スキルシステム

`skills/` ディレクトリに SKILL.md を配置することで、AI エンジンへの指示を拡張できる。

## SKILL.md の書き方

```yaml
---
name: review
description: 調査済みトピックのレビューと報告
platforms: [discord, slack]
user-invocable: true
---

# Instructions
ここに AI エンジンへの指示を書く。
```

## フィールド一覧

| フィールド | 必須 | 説明 |
|---|---|---|
| `name` | Yes | スキルの識別名（ディレクトリ名と一致させる） |
| `description` | Yes | スキルの説明（マッチング時の判断に使用） |
| `platforms` | No | 有効なプラットフォーム（省略すると全プラットフォームで有効） |
| `user-invocable` | No | `true` でユーザーが直接呼び出せるスキルとして登録 |

## 動作の仕組み

- `skills/` 配下のディレクトリを起動時にスキャンし、各 SKILL.md を読み込む
- `platforms` フィールドで現在のプラットフォームに該当するスキルだけが有効化される
- スキルの Instructions セクションはエンジン呼び出し時にプロンプトの先頭に自動注入される
- `user-invocable: true` のスキルは `/skills-list` コマンドのボタンから直接呼び出せる
- `/skills-list` 実行時にスキルを再スキャンするため、新規作成したスキルは**再起動不要で即座に認識される**

## 例: 毎朝 X に投稿するスキル

```yaml
---
name: morning-post
description: 毎朝の X 投稿を作成して投稿する
platforms: [discord]
user-invocable: false
---

# Instructions
HEARTBEAT.md のチェックリストに従い、毎朝の X 投稿を作成する。
ブラウザで X を開き、投稿内容を入力して送信する。
投稿内容は USER.md の関心事に基づいて生成する。
```
