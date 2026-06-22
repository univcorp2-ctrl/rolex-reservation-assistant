from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs

OUTPUT_PATH = Path("outputs/mock_submissions.jsonl")
FIELDS = [
    ("family_name", "姓", "text"),
    ("given_name", "名", "text"),
    ("family_name_kana", "セイ", "text"),
    ("given_name_kana", "メイ", "text"),
    ("email", "メール", "email"),
    ("phone", "電話番号", "tel"),
    ("birth_date", "生年月日", "text"),
    ("preferred_date", "希望日", "text"),
    ("preferred_time_window", "希望時間帯", "text"),
    ("preferred_model", "希望モデル", "text"),
]


class MockReservationHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa: N802
        self._send_html(self._form_html())

    def do_POST(self) -> None:  # noqa: N802
        length = int(self.headers.get("content-length", "0"))
        raw = self.rfile.read(length).decode("utf-8")
        parsed = {key: values[0] if values else "" for key, values in parse_qs(raw).items()}
        OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
        record = {"timestamp": datetime.now(timezone.utc).isoformat(), "payload": parsed}
        with OUTPUT_PATH.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
        self._send_html(
            "<html><body><h1 id='success'>送信を受け付けました</h1>"
            "<a href='/'>戻る</a></body></html>"
        )

    def log_message(self, format: str, *args: object) -> None:  # noqa: A002
        return

    def _send_html(self, html: str) -> None:
        encoded = html.encode("utf-8")
        self.send_response(200)
        self.send_header("content-type", "text/html; charset=utf-8")
        self.send_header("content-length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def _form_html(self) -> str:
        inputs = "\n".join(
            f"<label>{label}<input id='{key}' name='{key}' type='{input_type}' required></label><br>"
            for key, label, input_type in FIELDS
        )
        return f"""
<html lang="ja">
  <head><meta charset="utf-8"><title>Mock Reservation</title></head>
  <body>
    <h1>Mock Reservation Form</h1>
    <form method="post" action="/submit">
      {inputs}
      <label>応募文<textarea id="application_text" name="application_text"></textarea></label><br>
      <button id="submit" type="submit">送信する</button>
    </form>
  </body>
</html>
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    server = HTTPServer((args.host, args.port), MockReservationHandler)
    print(f"Mock reservation site running at http://{args.host}:{args.port}")
    server.serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
