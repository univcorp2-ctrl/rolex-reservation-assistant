from __future__ import annotations

import base64
import json
import os
from pathlib import Path
from typing import Any

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from .applicant import ApplicantProfile

KDF_ITERATIONS = 390_000
SALT_BYTES = 16


def _derive_key(passphrase: str, salt: bytes) -> bytes:
    if not passphrase:
        raise ValueError("Passphrase must not be empty")
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=KDF_ITERATIONS,
    )
    return base64.urlsafe_b64encode(kdf.derive(passphrase.encode("utf-8")))


def passphrase_from_env(env_name: str) -> str:
    value = os.environ.get(env_name)
    if not value:
        raise ValueError(f"Environment variable is not set: {env_name}")
    return value


def encrypt_profile_json(input_path: str | Path, output_path: str | Path, passphrase: str) -> None:
    source = Path(input_path)
    data = json.loads(source.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Profile JSON must be an object")
    ApplicantProfile.from_mapping(data)

    salt = os.urandom(SALT_BYTES)
    token = Fernet(_derive_key(passphrase, salt)).encrypt(
        json.dumps(data, ensure_ascii=False, sort_keys=True).encode("utf-8")
    )
    payload: dict[str, Any] = {
        "version": 1,
        "algorithm": "fernet-aes128-cbc-hmac-sha256",
        "kdf": "pbkdf2-sha256",
        "iterations": KDF_ITERATIONS,
        "salt_b64": base64.b64encode(salt).decode("ascii"),
        "ciphertext": token.decode("ascii"),
    }
    destination = Path(output_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def decrypt_profile_json(input_path: str | Path, passphrase: str) -> dict[str, Any]:
    payload = json.loads(Path(input_path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or payload.get("version") != 1:
        raise ValueError("Unsupported encrypted profile format")
    salt = base64.b64decode(str(payload["salt_b64"]))
    ciphertext = str(payload["ciphertext"]).encode("ascii")
    try:
        raw = Fernet(_derive_key(passphrase, salt)).decrypt(ciphertext)
    except InvalidToken as exc:
        raise ValueError("Failed to decrypt profile. Check the passphrase.") from exc
    data = json.loads(raw.decode("utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Decrypted profile JSON must be an object")
    return data


def load_encrypted_profile(input_path: str | Path, passphrase: str) -> ApplicantProfile:
    return ApplicantProfile.from_mapping(decrypt_profile_json(input_path, passphrase))
