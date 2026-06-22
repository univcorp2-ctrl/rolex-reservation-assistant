from __future__ import annotations

import json

from rolex_reservation_assistant.crypto_profile import encrypt_profile_json, load_encrypted_profile


def test_encrypt_and_decrypt_profile_roundtrip(tmp_path) -> None:  # noqa: ANN001
    source = tmp_path / "profile.json"
    encrypted = tmp_path / "profile.enc"
    source.write_text(
        json.dumps(
            {
                "family_name": "山田",
                "given_name": "太郎",
                "family_name_kana": "ヤマダ",
                "given_name_kana": "タロウ",
                "email": "taro@example.com",
                "phone": "09000000000",
                "birth_date": "1980-01-01",
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    encrypt_profile_json(source, encrypted, "test-passphrase")
    raw = encrypted.read_text(encoding="utf-8")
    assert "taro@example.com" not in raw
    profile = load_encrypted_profile(encrypted, "test-passphrase")
    assert profile.full_name == "山田 太郎"
