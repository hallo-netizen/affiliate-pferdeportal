from __future__ import annotations
import base64, hashlib, json, tempfile
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization
import signature_bridge as s


def canon(x):
    return json.dumps(x, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()


def sh(x):
    return hashlib.sha256(canon(x)).hexdigest()


def fixture(root: Path):
    key = Ed25519PrivateKey.generate()
    pub = key.public_key().public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw)
    trust = s.Trust("test-key", hashlib.sha256(pub).hexdigest(), base64.b64encode(pub).decode())
    import_env = {"contract": "PSERC_APPROVED_PRODUCTION_PACKAGE_V1", "x": "y"}
    import_sha = sh(import_env)
    rows = []
    proof_rows = []
    for i in range(7):
        slot = f"{i+1:064x}"
        body = f"# Test {i}\n\nInhalt {i}\n"
        digest = hashlib.sha256(body.encode()).hexdigest()
        rows.append({"name": f"ARTICLE_{slot}.md", "plan_slot": slot, "sha256": digest, "byte_length": len(body.encode()), "content_utf8": body})
        proof_rows.append({"plan_slot": slot, "final_draft_sha256": digest})
    manifest = {"contract": s.MANIFEST_CONTRACT, "batch_sha256": "a"*64, "article_count": 7, "articles": rows, "import_envelope_sha256": import_sha, "publish_allowed": False, "content_mutation_performed": False}
    proof = {"batch_sha256": "a"*64, "articles": proof_rows, "publish_allowed": False, "next_required": "SIGNED_WORKFLOW_RELEASE"}
    unsigned = {"contract": s.FINAL_CONTRACT, "endstamp_contract": s.ENDSTAMP_CONTRACT, "batch_sha256": "a"*64, "article_manifest": manifest, "import_envelope": import_env, "import_envelope_sha256": import_sha, "publish_allowed": False, "content_mutation_performed": False}
    mp, pp, up = root/"manifest.json", root/"proof.json", root/"unsigned.json"
    for p, obj in ((mp, manifest), (pp, proof), (up, unsigned)):
        p.write_text(json.dumps(obj, sort_keys=True), encoding="utf-8")
    req = s.build_sign_request(mp, pp, "isolated_system4/batch_proof/proof.json")
    sig = base64.b64encode(key.sign(req["manifest_sha256"].encode("ascii"))).decode()
    resp = {"contract": s.SIGN_RESPONSE_CONTRACT, "manifest_sha256": req["manifest_sha256"], "batch_sha256": req["batch_sha256"], "article_count": 7, "algorithm": "ED25519", "signing_key_id": trust.key_id, "signing_public_key_sha256": trust.public_sha256, "public_key_b64": trust.public_b64, "signature_b64": sig}
    rp = root/"sig.json"
    rp.write_text(json.dumps(resp), encoding="utf-8")
    return trust, mp, pp, up, rp


def expect_fail(fn):
    try:
        fn()
    except s.SignatureBridgeError:
        return
    raise AssertionError("expected SignatureBridgeError")


with tempfile.TemporaryDirectory() as td:
    root = Path(td)
    trust, mp, pp, up, rp = fixture(root)
    out = root/"final.json"
    result = s.apply_signature(up, rp, out, trust)
    assert result["status"] == "SYSTEM4_SIGNED_WORDPRESS_JSON_READY"
    final = json.loads(out.read_text(encoding="utf-8"))
    payload = dict(final)
    package_hash = payload.pop("package_payload_sha256")
    assert package_hash == s.stable_hash(payload)

    bad_manifest = json.loads(mp.read_text(encoding="utf-8"))
    bad_manifest["articles"][0]["content_utf8"] += "x"
    bmp = root/"bad_manifest.json"
    bmp.write_text(json.dumps(bad_manifest), encoding="utf-8")
    expect_fail(lambda: s.build_sign_request(bmp, pp, "x"))

    bad_unsigned = json.loads(up.read_text(encoding="utf-8"))
    bad_unsigned["import_envelope"]["x"] = "z"
    bup = root/"bad_unsigned.json"
    bup.write_text(json.dumps(bad_unsigned), encoding="utf-8")
    expect_fail(lambda: s.apply_signature(bup, rp, root/"x.json", trust))

    bad_response = json.loads(rp.read_text(encoding="utf-8"))
    bad_response["signature_b64"] = base64.b64encode(b"\0"*64).decode()
    brp = root/"bad_sig.json"
    brp.write_text(json.dumps(bad_response), encoding="utf-8")
    expect_fail(lambda: s.apply_signature(up, brp, root/"y.json", trust))

print("SYSTEM4_SIGNATURE_BRIDGE_TEST_PASS:4/4")
