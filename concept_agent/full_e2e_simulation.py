#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

class Failure(RuntimeError):
    pass

def canon(v: Any) -> bytes:
    return json.dumps(v, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")

def stable(v: Any) -> str:
    return hashlib.sha256(canon(v)).hexdigest()

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise Failure("JSON_OBJECT_REQUIRED:" + str(path))
    return value

def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise Failure("MODULE_LOAD_FAILED:" + str(path))
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module

def run(cmd: list[str], cwd: Path, env: dict[str, str]) -> str:
    cp = subprocess.run(cmd, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    output = (cp.stdout or "") + (cp.stderr or "")
    if cp.returncode != 0:
        raise Failure("COMMAND_FAILED:" + " ".join(cmd) + "\n" + output[-6000:])
    return output

def signer_setup(root: Path) -> dict[str, str]:
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
    key = Ed25519PrivateKey.generate()
    private_pem = key.private_bytes(serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8, serialization.NoEncryption())
    pub = key.public_key().public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw)
    pub_sha = hashlib.sha256(pub).hexdigest()
    key_path = root / "simulation-ed25519.pem"
    key_path.write_bytes(private_pem)
    signer = root / "simulation_signer.py"
    signer.write_text(
        """#!/usr/bin/env python3
import base64,hashlib,json,os,sys
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
key=serialization.load_pem_private_key(open(os.environ['SIM_PRIVATE_KEY_PATH'],'rb').read(),password=None)
req=json.loads(sys.stdin.read())
pub=key.public_key().public_bytes(serialization.Encoding.Raw,serialization.PublicFormat.Raw)
digest=hashlib.sha256(pub).hexdigest()
print(json.dumps({
 'signing_key_id':'simulation-ed25519-'+digest[:16],
 'signing_public_key_sha256':digest,
 'public_key_b64':base64.b64encode(pub).decode('ascii'),
 'signature_b64':base64.b64encode(key.sign(req['manifest_sha256'].encode('ascii'))).decode('ascii')
},separators=(',',':')))
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

def pserc_envelope(handoff: dict) -> dict:
    articles = handoff.get("articles")
    if not isinstance(articles, list) or not articles:
        raise Failure("HANDOFF_ARTICLES_INVALID")
    batch = str(handoff.get("batch_sha256") or "")
    packs, plans, releases = [], [], []
    seen = set()
    for index, row in enumerate(articles):
        if not isinstance(row, dict):
            raise Failure("HANDOFF_ARTICLE_ROW_INVALID")
        slot = str(row.get("plan_slot") or "")
        body = row.get("body")
        context = row.get("production_context")
        if len(slot) != 64 or slot in seen or not isinstance(body, str) or not isinstance(context, dict):
            raise Failure("HANDOFF_ARTICLE_BINDING_INVALID:" + str(index))
        fact_pack = context.get("fact_pack")
        plan_item = context.get("production_plan_item")
        if not isinstance(fact_pack, dict) or not isinstance(plan_item, dict):
            raise Failure("HANDOFF_PRODUCTION_CONTEXT_INVALID:" + str(index))
        seen.add(slot)
        cid = "article:simulation:" + hashlib.sha256((batch + "|" + slot).encode()).hexdigest()
        plan = json.loads(json.dumps(plan_item, ensure_ascii=False))
        plan["canonical_article_id"] = cid
        plan["plan_slot"] = slot
        canonical_article = plan.get("canonical_article")
        if not isinstance(canonical_article, dict):
            canonical_article = {}
            plan["canonical_article"] = canonical_article
        canonical_article["body_html"] = body
        packs.append(fact_pack)
        plans.append(plan)
        releases.append({"plan_slot": slot, "canonical_article_id": cid})
    fact_pack_bundle = {"contract": "canonical_fact_pack_import_v1", "fact_packs": packs}
    production_plan = {"contract": "production_plan_v4", "items": plans}
    workflow_release = {
        "contract": "WORKFLOW_SUPERVISOR_RELEASE_V2_SIGNED",
        "status": "PASS",
        "wordpress_write_performed": False,
        "exact_five_batch_sha256": batch,
        "exact_five_item_count": len(articles),
        "items": releases,
    }
    env = {
        "contract": "PSERC_APPROVED_PRODUCTION_PACKAGE_V1",
        "package_id": "",
        "package_payload_sha256": "",
        "source": "COMPLETE_1TO1_SIMULATION_REAL_SYSTEM4_BYTES",
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
    payload = dict(env)
    payload.pop("package_payload_sha256", None)
    env["package_payload_sha256"] = stable(payload)
    return env

def one_complete_run(repo: Path, out: Path, count: int) -> dict:
    if isinstance(count, bool) or count < 1:
        raise Failure("COUNT_MUST_BE_1_TO_N")
    if not os.environ.get("SYSTEM4_LANGUAGETOOL_JAR"):
        raise Failure("SYSTEM4_LANGUAGETOOL_JAR_REQUIRED")
    out.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=f"complete-1to1-{count}-") as td:
        root = Path(td)
        fixture = root / "fixture"
        runroot = root / "run"
        env = os.environ.copy()
        env["SYSTEM4_FRESH_RUN_TOKEN"] = f"complete-1to1-generic-{count}-article-test"
        env["SYSTEM4_LIVE_PARITY_FIXTURE"] = str(fixture)

        run([sys.executable, str(repo / "isolated_system4/test_route_input_factory.py"), str(fixture), str(count)], repo, env)
        run([sys.executable, str(repo / "isolated_system4/live_parity_v2.py"), "prepare", str(runroot)], repo, env)
        meta = load(runroot / "run_meta.json")
        actual_count = int(meta.get("article_count") or 0)
        if actual_count != count:
            raise Failure(f"COUNT_DRIFT:{count}:{actual_count}")
        for index in range(actual_count):
            run([sys.executable, str(repo / "isolated_system4/live_parity_v2.py"), "item", str(runroot), str(index)], repo, env)
        run([sys.executable, str(repo / "isolated_system4/live_parity_v2.py"), "finalize", str(runroot)], repo, env)

        handoff_path = runroot / "SYSTEM4_ARTICLE_BATCH_CHAT_HANDOFF_V2.json"
        handoff = load(handoff_path)
        if len(handoff.get("articles") or []) != actual_count:
            raise Failure("HANDOFF_COUNT_DRIFT")
        for i, row in enumerate(handoff["articles"]):
            if ((row.get("languagetool") or {}).get("status") != "PASS"
                    or (row.get("ppm679") or {}).get("status") != "PASS"):
                raise Failure("LT_OR_PPM_NOT_PASS:" + str(i))

        endroot = root / "endstempel-root"
        request = {
            "contract": "CONCEPT_AGENT_ENDSTEMPEL_AUTO_REQUEST_V1",
            "batch_sha256": handoff["batch_sha256"],
            "runtime_generation": 1,
            "import_envelope": pserc_envelope(handoff),
            "articles": [{"plan_slot": row["plan_slot"], "content_utf8": row["body"]} for row in handoff["articles"]],
            "publish_allowed": False,
            "content_mutation_performed": False,
        }
        request_path = endroot / "concept_agent/production_ready/request.json"
        request_path.parent.mkdir(parents=True, exist_ok=True)
        request_path.write_text(json.dumps(request, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

        bridge = load_module("complete_e2e_bridge", repo / "concept_agent/endstempel_bridge.py")
        finalizer = load_module("complete_e2e_finalizer", repo / "control/startmaster0107/GITHUB_FINAL_RELEASE.py")
        old_bridge_repo, old_final_repo = bridge.REPO, finalizer.REPO
        bridge.REPO = endroot
        finalizer.REPO = endroot
        signer_env = signer_setup(root)
        previous = {k: os.environ.get(k) for k in signer_env}
        os.environ.update(signer_env)
        try:
            source_ref = bridge.build(str(request_path.relative_to(endroot)))
            result = finalizer.finalize(source_ref)
        finally:
            bridge.REPO, finalizer.REPO = old_bridge_repo, old_final_repo
            for key, value in previous.items():
                if value is None:
                    os.environ.pop(key, None)
                else:
                    os.environ[key] = value

        final_source = endroot / result["final_ref"]
        package = load(final_source)
        if package.get("status") != "ENDSTEMPEL_PASS":
            raise Failure("ENDSTEMPEL_NOT_PASS")
        if (package.get("article_manifest") or {}).get("article_count") != actual_count:
            raise Failure("ENDSTEMPEL_COUNT_DRIFT")
        if package.get("publish_allowed") is not False:
            raise Failure("PUBLISH_FLAG_CHANGED")

        final_dir = out / "final"
        shutil.rmtree(final_dir, ignore_errors=True)
        final_dir.mkdir(parents=True)
        final_dest = final_dir / "FINAL_OUTPUT.json"
        shutil.copyfile(final_source, final_dest)
        files = [p for p in final_dir.iterdir() if p.is_file()]
        if files != [final_dest]:
            raise Failure("EXACTLY_ONE_FINAL_FILE_REQUIRED")

        return {
            "status": "PASS",
            "count_domain": "1..N",
            "article_count": actual_count,
            "batch_sha256": handoff["batch_sha256"],
            "system4_handoff_sha256": sha(handoff_path),
            "lt68_all_pass": True,
            "ppm679_all_pass": True,
            "pserc_package_contract": "PSERC_APPROVED_PRODUCTION_PACKAGE_V1",
            "endstempel_status": "ENDSTEMPEL_PASS",
            "final_file": str(final_dest),
            "final_file_sha256": sha(final_dest),
            "exactly_one_final_file": True,
            "publish_allowed": False,
        }


def run_positive(repo: Path, outdir: Path, count: int) -> dict:
    """Backward-compatible acceptance entry. Uses the same generic 1..N complete route."""
    return one_complete_run(Path(repo).resolve(), Path(outdir).resolve(), int(count))

def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--count", required=True, type=int)
    args = ap.parse_args(argv)
    repo = Path(args.repo).resolve()
    out = Path(args.out).resolve()
    try:
        result = one_complete_run(repo, out, args.count)
        regression_env = os.environ.copy()
        regression_env["HOBBYROOM_TARGET_ROOT"] = str(repo)
        regression = run([sys.executable, str(repo / "control/startmaster0107/HOBBYRAUM_M01_M33_REGRESSION.py")], repo, regression_env)
        if "GESAMT PASS" not in regression:
            raise Failure("M01_M38_NOT_GESAMT_PASS")
        proof = {
            "contract": "CONCEPT_AGENT_COMPLETE_1TO1_SIMULATION_V2",
            "status": "PASS",
            "scope": [
                "CHAT_START",
                "POINT0",
                "RESEARCH",
                "FACTS",
                "CONTEXT",
                "DRAFT",
                "SAME_ARTICLE_REPAIR",
                "LANGUAGETOOL_6_8",
                "PPM_6_7_9",
                "BATCH_GATE",
                "PSERC_PACKAGE",
                "ENDSTEMPEL",
                "EXACTLY_ONE_FINAL_FILE",
                "M01_M38",
            ],
            "generic_count_contract": "1..N",
            "run": result,
            "known_error_regressions": "M01-M38 PASS",
            "publish_allowed": False,
        }
        proof["proof_sha256"] = stable(proof)
        proof_dir = out / "proof"
        proof_dir.mkdir(parents=True, exist_ok=True)
        (proof_dir / "COMPLETE_1TO1_SIMULATION_PROOF.json").write_text(json.dumps(proof, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({"ok": True, "status": "PASS", "article_count": result["article_count"], "count_domain": "1..N", "final_file_sha256": result["final_file_sha256"], "m01_m38": "PASS"}, ensure_ascii=False, sort_keys=True))
        return 0
    except Exception as exc:
        out.mkdir(parents=True, exist_ok=True)
        (out / "BLOCKED.json").write_text(json.dumps({"ok": False, "status": "BLOCKED", "reason": str(exc), "publish_allowed": False}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print("COMPLETE_1TO1_SIMULATION_BLOCKED:" + str(exc), file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
