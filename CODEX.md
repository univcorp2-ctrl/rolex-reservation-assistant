# CODEX

## 開発方針

- 個人情報はコミットしない。
- 公開予約サイトに対する自動入力、自動送信、CAPTCHA突破は実装しない。
- ローカルE2Eでは入力、フォールバック、送信、成功確認までテストする。
- 変更後は `ruff check .` と `pytest` を実行する。
- 実サイト用の追加機能は、手動確認を残す形で実装する。

## 主要コマンド

```bash
pip install -e .[dev]
ruff check .
pytest
python -m rolex_reservation_assistant rehearse --profile config/applicant.example.json --location all --selectors config/selectors.mock.json --iterations 100
```
