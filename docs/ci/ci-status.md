# CI Status

## 現在の状態

- Repository CI runner: 実装済み (`ci/run_ci.py`)
- Makefile CI target: 実装済み (`make ci`)
- GitHub Actions workflow template: 実装済み (`docs/ci/python-ci.yml`)
- `.github/workflows/ci.yml`: GitHub API 404によりActions経由での作成に失敗

## GitHub API 404の意味

通常のソースファイルはコミットできていますが、`.github/workflows/*.yml` だけが `GitHub API 404: Not Found` になります。この症状は、GitHub token / GitHub App installation token がworkflowファイルを書き込む権限を持たない場合に起きます。

## 同梱しているCI内容

`ci/run_ci.py` は以下を順番に実行します。

1. `python -m pip install --upgrade pip`
2. `python -m pip install -e .[dev]`
3. `ruff check .`
4. `pytest`
5. `python -m rolex_reservation_assistant rehearse --profile config/applicant.example.json --location all --selectors config/selectors.mock.json --iterations 100`

GitHub Actions workflowとして使う内容は `docs/ci/python-ci.yml` に保存しています。
