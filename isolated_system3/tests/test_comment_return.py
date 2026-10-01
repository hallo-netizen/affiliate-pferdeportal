import base64
import hashlib
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from isolated_system3.comment_return import ReturnError, decode_return, materialize


def payload(raw: bytes) -> str:
    b64 = base64.b64encode(raw).decode("ascii")
    sha = hashlib.sha256(raw).hexdigest()
    return (
        "SYSTEM3_ARTICLE_B64_BEGIN\n"
        f"{b64}\n"
        "SYSTEM3_ARTICLE_B64_END\n"
        f"SYSTEM3_ARTICLE_SHA256:{sha}\n"
        "SYSTEM3_RETURN_PASS"
    )


class CommentReturnTests(unittest.TestCase):
    def test_positive_exact_roundtrip(self):
        raw = "Ein sauberer deutscher Testartikel.\n".encode("utf-8")
        self.assertEqual(decode_return(payload(raw)), raw)

    def test_materialize_exact_bytes(self):
        raw = "ÄÖÜ Pferd\n".encode("utf-8")
        with TemporaryDirectory() as td:
            out = Path(td) / "codex_output.md"
            sha = materialize(payload(raw), out)
            self.assertEqual(out.read_bytes(), raw)
            self.assertEqual(sha, hashlib.sha256(raw).hexdigest())

    def test_rejects_extra_prose(self):
        with self.assertRaisesRegex(ReturnError, "SYSTEM3_RETURN_SCHEMA_FAIL"):
            decode_return("Summary\n" + payload(b"x"))

    def test_rejects_wrong_sha(self):
        body = payload(b"x").replace(hashlib.sha256(b"x").hexdigest(), "0" * 64)
        with self.assertRaisesRegex(ReturnError, "SYSTEM3_RETURN_SHA_FAIL"):
            decode_return(body)

    def test_rejects_bad_base64(self):
        body = payload(b"x").replace("eA==", "!!!!")
        with self.assertRaises(ReturnError):
            decode_return(body)


if __name__ == "__main__":
    unittest.main()
