# Setup Guide

## 1. Codespacesで開く

GitHubのリポジトリ画面で `Code` → `Codespaces` → `Create codespace on main` を選びます。devcontainerによりPython環境と開発依存関係が自動で入ります。

## 2. 個人情報をローカルファイルに入れる

`config/applicant.example.json` を `config/applicant.local.json` にコピーします。実名、メール、電話番号、生年月日は `config/applicant.local.json` にだけ入れてください。このファイルは `.gitignore` で除外済みです。

```bash
cp config/applicant.example.json config/applicant.local.json
```

## 3. 暗号化する

```bash
export APPLICANT_PROFILE_PASSPHRASE="長くランダムな文字列に変更"
python -m rolex_reservation_assistant encrypt-profile \
  --in config/applicant.local.json \
  --out secrets/applicant.enc
```

## 4. 入力計画を確認する

```bash
python -m rolex_reservation_assistant plan \
  --encrypted-profile secrets/applicant.enc \
  --location all
```

## 5. 実サイトを開く

```bash
python -m rolex_reservation_assistant open \
  --encrypted-profile secrets/applicant.enc \
  --location all \
  --interval-seconds 20
```

CAPTCHAと最終送信は画面を見て人間が行います。

## 6. ローカルE2Eで送信まで確認する

```bash
python scripts/run_mock_site.py --port 8765
```

別ターミナル:

```bash
python -m rolex_reservation_assistant e2e-script \
  --encrypted-profile secrets/applicant.enc \
  --location ginza \
  --url http://127.0.0.1:8765 \
  --selectors config/selectors.mock.json \
  --out outputs/e2e_fill_mock.py \
  --submit
pip install playwright
python -m playwright install chromium
python outputs/e2e_fill_mock.py
```

## 7. 100回リハーサル

```bash
python -m rolex_reservation_assistant rehearse \
  --profile config/applicant.example.json \
  --location all \
  --selectors config/selectors.mock.json \
  --iterations 100
```
