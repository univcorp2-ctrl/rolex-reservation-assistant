# CAPTCHA Provider Decision

## 結論

第三者の予約サイトに対してCAPTCHAを解くAIモデルや外部解決APIは実装しません。このリポジトリでは、実サイトのCAPTCHAと最終送信は人間が画面を確認して完了する設計を維持します。

自社または社内で所有・管理するサイトにbot対策を入れる場合は、CAPTCHAを突破するモデルではなく、正規のbot対策プロバイダを実装します。

## 候補

| 候補 | 向いているケース | 実装方針 |
| --- | --- | --- |
| Cloudflare Turnstile | 無料・低摩擦・プライバシー重視でCAPTCHA代替を入れたい | widgetを埋め込み、サーバー側でtoken検証 |
| Google reCAPTCHA / reCAPTCHA Enterprise | Google Cloudでリスク評価、スコア、Enterprise管理を使いたい | フロントでtoken取得、バックエンドでassessment作成 |
| hCaptcha / hCaptcha Enterprise | reCAPTCHA代替、Enterprise、Passive mode、アクセシビリティを重視 | widgetを埋め込み、サーバー側でtoken検証 |
| manual | 第三者予約サイト、または権限のないサイト | 人間がCAPTCHAと最終送信を確認 |

## 実装しないもの

- CAPTCHA画像をAI vision modelへ渡して解答する処理
- CAPTCHA farm / 外部突破API連携
- bot検知を避けるための人間風マウス操作・入力操作
- 第三者サイトでの無人応募送信

## このrepoでの採用

- 実サイト: `manual`
- ローカルE2E: CAPTCHAなしのmock form
- 自社/社内サイトへ拡張する場合: `Cloudflare Turnstile` を第一候補、Google Cloud運用が必要なら `reCAPTCHA Enterprise`、Enterpriseアクセシビリティ/Passive mode重視なら `hCaptcha Enterprise`

## 実装メモ

CAPTCHA providerを追加する場合でも、`solve()` メソッドでCAPTCHAを突破するのではなく、以下のような正規フローだけにします。

1. フロントエンドでproviderのwidgetを表示する。
2. ユーザーが正規のchallengeまたはsilent verificationを完了する。
3. フロントエンドがtokenを取得する。
4. バックエンドがprovider公式APIでtokenを検証する。
5. 検証結果に基づいて予約・応募処理を続行する。
