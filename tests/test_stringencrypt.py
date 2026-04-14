"""Unit tests for StringEncrypt WebAPI client (HTTP mocked)."""

import zlib
import base64
from urllib.parse import parse_qs

import responses

from stringencrypt import StringEncrypt


API = StringEncrypt.API_URL


@responses.activate
def test_encrypt_success_plain_source():
    body = {"error": 0, "source": "print('ok')\n"}
    responses.add(responses.POST, API, json=body, status=200)

    se = StringEncrypt("", session=requests_session())
    se.enableCompression = False
    r = se.encrypt_string("hi", "lbl")
    assert r is not False
    assert r["error"] == 0
    assert r["error_string"] == "ERROR_SUCCESS"
    assert r["source"] == "print('ok')\n"


@responses.activate
def test_encrypt_success_compressed_source_roundtrip():
    plain = "decrypted source"
    compressed_field = base64.b64encode(
        zlib.compress(plain.encode("utf-8"), 9)
    ).decode("ascii")
    body = {"error": 0, "source": compressed_field}
    responses.add(responses.POST, API, json=body, status=200)

    se = StringEncrypt("", session=requests_session())
    se.enableCompression = True
    r = se.encrypt_string("hello", "lab")
    assert r is not False
    assert r["source"] == plain


@responses.activate
def test_http_error_returns_false():
    responses.add(responses.POST, API, status=500)
    se = StringEncrypt("", session=requests_session())
    assert se.encrypt_string("a", "b") is False


@responses.activate
def test_invalid_json_returns_false():
    responses.add(responses.POST, API, body="not json", status=200)
    se = StringEncrypt("", session=requests_session())
    assert se.encrypt_string("a", "b") is False


@responses.activate
def test_unknown_error_code_maps_to_unknown_string():
    body = {"error": 99999, "source": ""}
    responses.add(responses.POST, API, json=body, status=200)
    se = StringEncrypt("", session=requests_session())
    se.enableCompression = False
    r = se.encrypt_string("x", "y")
    assert r is not False
    assert r["error_string"] == "ERROR_UNKNOWN_99999"


@responses.activate
def test_info_command():
    body = {"engine_version": "v1.5.0", "supported_languages": [{"cpp": "C / C++"}]}
    responses.add(responses.POST, API, json=body, status=200)
    se = StringEncrypt("CODE", session=requests_session())
    r = se.info()
    assert r is not False
    assert r["engine_version"] == "v1.5.0"
    assert "error_string" not in r


@responses.activate
def test_encrypt_posts_include_flags():
    responses.add(responses.POST, API, json={"error": 0, "source": "x"}, status=200)
    se = StringEncrypt("", session=requests_session())
    se.enableCompression = False
    se.includeTags = True
    se.includeExample = True
    se.returnTemplate = True
    se.includeDebugComments = True
    se.highlight = "js"
    se.encryptionTemplate = '{"commands":[]}'
    se.encrypt_string("s", "l")

    assert len(responses.calls) == 1
    sent = responses.calls[0].request.body
    if isinstance(sent, bytes):
        sent = sent.decode("utf-8")
    q = parse_qs(sent, keep_blank_values=True)
    assert q.get("include_tags") == ["1"]
    assert q.get("include_example") == ["1"]
    assert q.get("return_template") == ["1"]
    assert q.get("include_debug_comments") == ["1"]
    assert q.get("highlight") == ["js"]
    assert "template" in q and q["template"]


def test_encrypt_file_empty(tmp_path):
    p = tmp_path / "empty.bin"
    p.write_bytes(b"")
    se = StringEncrypt("")
    assert se.encrypt_file_contents(p, "lbl") is False


def test_encrypt_file_reads_bytes(tmp_path, monkeypatch):
    p = tmp_path / "one.bin"
    p.write_bytes(b"\x00\xff")

    captured = {}

    def fake_post(self, params):
        captured["bytes"] = params.get("bytes")
        return {"error": 0, "source": ""}

    monkeypatch.setattr(StringEncrypt, "post_request", fake_post)
    se = StringEncrypt("")
    se.enableCompression = False
    se.encrypt_file_contents(p, "x")
    assert captured["bytes"] == b"\x00\xff"


def requests_session():
    import requests

    return requests.Session()


@responses.activate
def test_corrupt_compressed_source_returns_false():
    body = {"error": 0, "source": "not-valid-base64!!!"}
    responses.add(responses.POST, API, json=body, status=200)
    se = StringEncrypt("", session=requests_session())
    se.enableCompression = True
    assert se.encrypt_string("a", "b") is False
