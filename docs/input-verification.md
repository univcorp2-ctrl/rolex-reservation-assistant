# Input Verification

## 検証結果

このリポジトリには実個人情報を保存しません。今回の入力検証では、個人情報そのものは書かず、形式だけを検証対象にしています。

| 項目 | 検証内容 | 結果 |
| --- | --- | --- |
| 氏名 | 姓・名に分けて保存できる必要がある | 要確認。ローカルSecret側で `family_name` と `given_name` に分ける |
| カナ | 多くの日本語フォームで必要になる可能性 | 追加必須。`family_name_kana` と `given_name_kana` をSecret側に入れる |
| メール | `name@example.com` 形式 | validatorで検証 |
| 電話番号 | 日本の10〜11桁、ハイフン除去、`+81` 正規化 | validatorで検証 |
| 生年月日 | `YYYY-MM-DD` / `YYYY.MM.DD` / `YYYY/MM/DD` を受け付け、ISO形式へ正規化 | validatorで検証 |
| 希望日 | `auto` の場合、直近1〜10日から選択 | 既存テストで検証 |
| 希望時間 | `afternoon` の場合、午後枠から選択 | 既存テストで検証 |
| 希望モデル | 候補リストから選択 | 既存テストで検証 |

## 追加した検証

- `normalize_email()`
- `normalize_japanese_phone()`
- `normalize_birth_date()`
- `validate_profile_shape()`
- `tests/test_validation.py`

## 入力ミス防止の要点

- 生年月日の `1981.11.05` のようなドット区切りは `1981-11-05` に正規化する。
- 電話番号はハイフン、スペース、括弧、`+81` を吸収する。
- カナがない場合は早い段階でエラーにする。
- 実個人情報は `config/applicant.local.json` またはSecretsにだけ置き、GitHubにはコミットしない。
