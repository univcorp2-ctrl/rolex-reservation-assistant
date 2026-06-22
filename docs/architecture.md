# Architecture

![Rolex Reservation Assistant Architecture](architecture.svg)

## 全体像

このツールは、予約応募の準備作業をCLIで整理し、実サイトでは人間の確認を必ず残す構成です。個人情報はGitHubに置かず、ローカルで暗号化したプロフィールまたはSecretsから読み込みます。

```mermaid
flowchart TD
    A[applicant.local.json / GitHub Secret] --> B[encrypt-profile]
    B --> C[applicant.enc]
    C --> D[CLI]
    D --> E[decrypt profile]
    E --> F[random preference resolver]
    F --> G[input plan builder]
    G --> H[application text generator]
    G --> I[manual real-site checklist]
    G --> J[local-only E2E script generator]
    J --> K[mock reservation form]
    K --> L[mock submission log]
    D --> M[captcha cost estimator]
    D --> N[audit log JSONL]
    O[rehearsal runner] --> G
    P[GitHub Actions] --> Q[ruff]
    P --> R[pytest]
    R --> S[test artifact]
```

## 処理の流れ

1. `config/applicant.local.json` をローカルに作成する。
2. `encrypt-profile` で `secrets/applicant.enc` に暗号化する。
3. `plan` で応募文、希望日、午後時間帯、希望モデル、入力チェックリストを生成する。
4. `open` で予約ページを1店舗ずつ開く。複数店舗では既定で20秒間隔を置く。
5. 実サイトでは人間がCAPTCHAと最終送信を確認する。
6. `e2e-script` はlocalhostなどのローカルE2E対象だけにPlaywrightスクリプトを生成する。
7. `rehearse --iterations 100` でランダム選択、必須項目、送信スクリプト、フォールバック、公開URLブロックを検証する。

## フォールバック設計

ローカルE2E用のPlaywrightスクリプトは、各フィールドに複数のセレクタ候補を持ちます。最初の候補が見つからない場合、次の候補を順に試します。入力後は `input_value()` で値を検証し、値が一致しない場合は `fill()` で再入力します。送信後は成功マーカーを確認します。

## セキュリティ

- 個人情報の平文ファイルは `.gitignore` で除外しています。
- 暗号化プロフィールは `cryptography.Fernet` とPBKDF2-SHA256で保護します。
- Secretsの実値はREADMEにもコードにも含めません。
- CAPTCHA突破APIの実装は入れていません。
- 公開予約サイトをE2E自動化対象にすると例外を出します。

## CI/CD

GitHub Actionsは以下を実行する設計です。workflow作成権限がある環境では `.github/workflows/ci.yml` に配置します。現在の代替テンプレートは `docs/ci/python-ci.yml` です。

- checkout
- Python 3.11 / 3.12 setup
- dependency install
- ruff lint
- pytest
- JUnit artifact upload

## GPT image 最新モデル用の図解方針

このドキュメントにはSVG画像版のアーキテクチャ図を含めています。追加でGPT imageの最新モデルに渡す再生成用プロンプトは `docs/gpt-image-architecture-prompt.md` に保存しています。
