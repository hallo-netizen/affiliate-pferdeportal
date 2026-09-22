#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import hashlib
import importlib.util
import json
import os
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any


class Failure(RuntimeError):
    pass


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise Failure("MODULE_LOAD_FAILED:" + str(path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def canon(v: Any) -> bytes:
    return json.dumps(v, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def stable(v: Any) -> str:
    return hashlib.sha256(canon(v)).hexdigest()


def make_articles(count: int) -> tuple[str, list[dict[str, Any]], dict[str, Any]]:
    rows = []
    plan_items = []
    release_items = []
    for i in range(count):
        slot = hashlib.sha256(f"full-e2e-slot-{count}-{i}".encode()).hexdigest()
        cid = f"article:full-e2e-{count}-{i}"
        body = (
            f'<article class="ppm-generated ppm-type-beratung" data-article-type="Beratung">'
            f'<section data-block="intro"><p>Vollständiger Konzept-5-E2E-Testartikel {i+1} von {count}.</p></section>'
            f'<section data-block="details"><h2>Gebundener Testablauf {i+1}</h2>'
            f'<p>Dieser Inhalt prüft ausschließlich Transport, Bindung, Endstempel und Dateiausgabe.</p></section>'
            f'</article>'
        )
        rows.append({"plan_slot": slot, "content_utf8": body})
        plan_items.append({
            "canonical_article_id": cid,
            "plan_slot": slot,
            "canonical_article": {"body_html": body},
        })
        release_items.append({"plan_slot": slot, "canonical_article_id": cid})
    batch = stable({"contract": "FULL_E2E_BATCH_V1", "count": count, "slots": [r["plan_slot"] for r in rows]})
    production_plan = {"contract": "production_plan_v4", "items": plan_items}
    workflow_release = {
        "contract": "WORKFLOW_SUPERVISOR_RELEASE_V2_SIGNED",
        "status": "PASS",
        "wordpress_write_performed": False,
        "exact_five_batch_sha256": batch,
        "items": release_items,
    }
    fact_pack_bundle = {"contract": "canonical_fact_pack_import_v1", "fact_packs": []}
    env = {
        "contract": "PSERC_APPROVED_PRODUCTION_PACKAGE_V1",
        "package_id": "",
        "package_payload_sha256": "",
        "source": "CONCEPT_AGENT_FULL_E2E_SIMULATION",
        "fact_pack_bundle": fact_pack_bundle,
        "fact_pack_bundle_sha256": stable(fact_pack_bundle),
        "production_plan": production_plan,
        "production_plan_sha256": stable(production_plan),
        "workflow_release": workflow_release,
        "workflow_release_sha256": stable(workflow_release),
    }
    env["package_id"] = stable({
        "contract": env["contract"],
        "fact_pack_bundle_sha256": env["fact_pack_bundle_sha256"],
        "production_plan_sha256": env["production_plan_sha256"],
        "workflow_release_sha256": env["workflow_release_sha256"],
    })
    copy = dict(env)
    copy.pop("package_payload_sha256", None)
    env["package_payload_sha256"] = stable(copy)
    return batch, rows, env


def signer_setup(root: Path) -> dict[str, str]:
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

    key = Ed25519PrivateKey.generate()
    private_pem = key.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.PKCS8,
        serialization.NoEncryption(),
    )
    pub = key.public_key().public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw)
    pub_sha = hashlib.sha256(pub).hexdigest()
    key_path = root / "sim-ed25519.pem"
    key_path.write_bytes(private_pem)
    signer = root / "sim_signer.py"
    signer.write_text(
        """#!/usr/bin/env python3
import base64,json,os,sys
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
raw=open(os.environ['SIM_PRIVATE_KEY_PATH'],'rb').read()
key=serialization.load_pem_private_key(raw,password=None)
if not isinstance(key,Ed25519PrivateKey): raise SystemExit(2)
req=json.loads(sys.stdin.read())
pub=key.public_key().public_bytes(serialization.Encoding.Raw,serialization.PublicFormat.Raw)
import hashlib
sha=hashlib.sha256(pub).hexdigest()
out={
 'signing_key_id':'simulation-ed25519-'+sha[:16],
 'signing_public_key_sha256':sha,
 'public_key_b64':base64.b64encode(pub).decode('ascii'),
 'signature_b64':base64.b64encode(key.sign(req['manifest_sha256'].encode('ascii'))).decode('ascii')
}
print(json.dumps(out,separators=(',',':')))
""",
        encoding="utf-8",
    )
    os.chmod(signer, 0o700)
    return {
        "SIM_PRIVATE_KEY_PATH": str(key_path),
        "ENDSTEMPEL_HSM_CMD": f"{sys.executable} {signer}",
        "ENDSTEMPEL_TRUSTED_KEY_ID": "simulation-ed25519-" + pub_sha[:16],
        "ENDSTEMPEL_TRUSTED_PUBLIC_KEY_SHA256": pub_sha,
        "ENDSTEMPEL_TRUSTED_PUBLIC_KEY_B64": base64.b64encode(pub).decode("ascii"),
    }


def build_source(root: Path, bridge, count: int, generation: int = 1) -> tuple[str, str]:
    batch, articles, env = make_articles(count)
    req = {
        "contract": "CONCEPT_AGENT_ENDSTEMPEL_AUTO_REQUEST_V1",
        "batch_sha256": batch,
        "runtime_generation": generation,
        "import_envelope": env,
        "articles": articles,
        "publish_allowed": False,
        "content_mutation_performed": False,
    }
    p = root / "concept_agent/production_ready/run.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(req, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    old = bridge.REPO
    bridge.REPO = root
    try:
        ref = bridge.build(str(p.relative_to(root)))
    finally:
        bridge.REPO = old
    return batch, ref


def run_positive(repo: Path, outdir: Path, count: int) -> dict[str, Any]:
    bridge = load_module(f"bridge_pos_{count}", repo / "concept_agent/endstempel_bridge.py")
    final = load_module(f"final_pos_{count}", repo / "control/startmaster0107/GITHUB_FINAL_RELEASE.py")
    with tempfile.TemporaryDirectory(prefix=f"concept-agent-e2e-{count}-") as td:
        root = Path(td)
        batch, source_ref = build_source(root, bridge, count)
        env = signer_setup(root)
        old_env = {k: os.environ.get(k) for k in env}
        os.environ.update(env)
        old_repo = final.REPO
        final.REPO = root
        try:
            result = final.finalize(source_ref)
        finally:
            final.REPO = old_repo
            for k, v in old_env.items():
                if v is None:
                    os.environ.pop(k, None)
                else:
                    os.environ[k] = v
        p = root / result["final_ref"]
        if not p.is_file():
            raise Failure("FINAL_FILE_MISSING")
        data = json.loads(p.read_text(encoding="utf-8"))
        if data.get("status") != "ENDSTEMPEL_PASS" or data.get("contract") != "PSERC_APPROVED_PRODUCTION_PACKAGE_V1":
            raise Failure("FINAL_FILE_CONTRACT_INVALID")
        if data.get("publish_allowed") is not False or data.get("content_mutation_performed") is not False:
            raise Failure("FINAL_FILE_FLAGS_INVALID")
        if (data.get("article_manifest") or {}).get("article_count") != count:
            raise Failure("FINAL_FILE_COUNT_INVALID")
        dest = outdir / f"positive-{count}" / f"FINAL_{count}_ARTICLES.json"
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(p, dest)
        return {
            "count": count,
            "status": "PASS",
            "batch_sha256": batch,
            "final_file": str(dest),
            "final_sha256": hashlib.sha256(dest.read_bytes()).hexdigest(),
            "endstempel_status": data["status"],
            "file_count": 1,
        }


def run_negative_article_tamper(repo: Path, outdir: Path) -> dict[str, Any]:
    bridge = load_module("bridge_neg_article", repo / "concept_agent/endstempel_bridge.py")
    final = load_module("final_neg_article", repo / "control/startmaster0107/GITHUB_FINAL_RELEASE.py")
    with tempfile.TemporaryDirectory(prefix="concept-agent-neg-article-") as td:
        root = Path(td)
        _, source_ref = build_source(root, bridge, 1)
        manifest = json.loads((root / source_ref).read_text(encoding="utf-8"))
        article = root / manifest["items"][0]["ref"]
        article.write_text(article.read_text(encoding="utf-8") + "\nTAMPER", encoding="utf-8")
        env = signer_setup(root)
        old_env = {k: os.environ.get(k) for k in env}
        os.environ.update(env)
        old_repo = final.REPO
        final.REPO = root
        try:
            try:
                final.finalize(source_ref)
            except Exception as exc:
                reason = str(exc)
            else:
                raise Failure("NEGATIVE_ARTICLE_TAMPER_NOT_BLOCKED")
        finally:
            final.REPO = old_repo
            for k, v in old_env.items():
                if v is None: os.environ.pop(k, None)
                else: os.environ[k] = v
        if "ARTICLE_HASH_MISMATCH" not in reason:
            raise Failure("NEGATIVE_ARTICLE_TAMPER_WRONG_REASON:" + reason)
        return {"case": "article-bytes-tampered-after-source-binding", "status": "PASS", "blocked": True, "reason": reason}


def run_negative_envelope_tamper(repo: Path, outdir: Path) -> dict[str, Any]:
    bridge = load_module("bridge_neg_env", repo / "concept_agent/endstempel_bridge.py")
    final = load_module("final_neg_env", repo / "control/startmaster0107/GITHUB_FINAL_RELEASE.py")
    with tempfile.TemporaryDirectory(prefix="concept-agent-neg-env-") as td:
        root = Path(td)
        _, source_ref = build_source(root, bridge, 3)
        manifest = json.loads((root / source_ref).read_text(encoding="utf-8"))
        env_path = root / manifest["import_envelope_ref"]
        env = json.loads(env_path.read_text(encoding="utf-8"))
        env["source"] = "TAMPERED"
        env_path.write_text(json.dumps(env, ensure_ascii=False), encoding="utf-8")
        old_repo = final.REPO
        final.REPO = root
        try:
            try:
                final.finalize(source_ref)
            except Exception as exc:
                reason = str(exc)
            else:
                raise Failure("NEGATIVE_ENVELOPE_TAMPER_NOT_BLOCKED")
        finally:
            final.REPO = old_repo
        if "IMPORT_ENVELOPE_FILE_HASH_INVALID" not in reason:
            raise Failure("NEGATIVE_ENVELOPE_TAMPER_WRONG_REASON:" + reason)
        return {"case": "pserc-envelope-tampered-before-final-file", "status": "PASS", "blocked": True, "reason": reason}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    repo = Path(args.repo).resolve()
    out = Path(args.out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    proof = {
        "contract": "CONCEPT_AGENT_CHAT_TO_FINAL_FILE_SIMULATION_V1",
        "status": "PASS",
        "positive": [run_positive(repo, out, 1), run_positive(repo, out, 3)],
        "negative": [run_negative_article_tamper(repo, out), run_negative_envelope_tamper(repo, out)],
        "path": [
            "CHAT_TRIGGER",
            "GITHUB_ACTION",
            "WORKFLOW_ENTRY",
            "FAST_FORWARD_VALIDATED_PRIOR_STAGES",
            "ARTICLE_PIPELINE",
            "PSERC_PACKAGE",
            "ENDSTEMPEL",
            "EXACTLY_ONE_FINAL_FILE",
            "CHAT_RETURN_ARTIFACT",
        ],
        "publish_allowed": False,
    }
    proof["proof_sha256"] = stable(proof)
    (out / "CONCEPT_AGENT_CHAT_TO_FINAL_FILE_SIMULATION_V1.json").write_text(
        json.dumps(proof, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({
        "ok": True,
        "status": "PASS",
        "positive_counts": [1, 3],
        "negative_cases": 2,
        "proof_sha256": proof["proof_sha256"],
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
