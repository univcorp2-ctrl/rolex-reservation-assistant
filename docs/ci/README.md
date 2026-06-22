# CI workflow template

GitHub APIが `.github/workflows/*.yml` の作成を拒否する環境でも内容を確認できるよう、同じworkflow定義をここに保存しています。

本来の配置先は次です。

```text
.github/workflows/python-ci.yml
```

このworkflowは、push、pull_request、workflow_dispatchで起動し、Python 3.11 / 3.12のmatrixで以下を実行します。

- checkout
- setup-python
- pip install
- ruff check
- pytest
- JUnit artifact upload
