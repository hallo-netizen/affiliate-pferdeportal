#!/usr/bin/env python3
"""HD009: style-only update of the verified 0.1.19 current release, no new plugin."""
from pathlib import Path
from zipfile import ZipFile
from io import BytesIO
import re, hashlib, subprocess, tempfile

P = Path("protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH/PLUGINS/ISOLIERTE_PLUGINS/HD-009-AFFILIATE-ZENTRALE/CURRENT.zip")
EXPECTED_SHA = "53f0feb7bf5e97032f840fd5e1fe2ddee80f24b3440202e0c136cf38a67e6579"
CSS = "affiliate-portal-router/assets/hdar-amazon-start.css"
AMAZON = "affiliate-portal-router/includes/class-hdar-amazon-start.php"
MAIN = "affiliate-portal-router/hobby-depot-affiliate-router.php"
append_css = r"""

/* HD009 0.1.20: agreed subdued banner finish, identical topic photo reused
   with format-specific crop; existing provider choice and slots untouched. */
a.hdar-ci-amazon-banner {
  border-radius:2px!important;
  border-color:#d8c5af!important;
  background:#e8d9c6!important;
}
a.hdar-ci-amazon-banner .hdar-ci-content {
  background:linear-gradient(108deg,#fffaf2 0%,#f3dec5 54%,#dfae82 100%)!important;
}
a.hdar-ci-amazon-banner .hdar-ci-photo {
  background:#e8d9c6!important;
}
a.hdar-ci-amazon-banner .hdar-ci-photo>img {
  transform:scale(.96)!important;
  transform-origin:50% 50%!important;
}
a.hdar-ci-amazon-banner .hdar-ci-button {
  border-radius:2px!important;
  padding:4px 7px!important;
  gap:5px!important;
  bottom:clamp(7px,2cqw,13px)!important;
  box-shadow:0 2px 9px rgba(0,0,0,.15)!important;
}
a.hdar-ci-amazon-banner .hdar-ci-amazon-official {
  width:clamp(140px,23cqw,166px)!important;
  min-width:140px!important;
  max-width:166px!important;
}
a.hdar-ci-amazon-banner .hdar-ci-amazon-arrow {
  font-size:clamp(15px,2.3cqw,22px)!important;
  margin-left:2px!important;
}
a.hdar-ci-amazon-banner-square .hdar-ci-content {
  padding:clamp(7px,2.2cqw,14px) clamp(9px,3cqw,18px)!important;
}
a.hdar-ci-amazon-banner-wide {
  aspect-ratio:4.2/1!important;
  min-height:128px!important;
}
a.hdar-ci-amazon-banner-wide .hdar-ci-content {
  padding:clamp(7px,1.3cqw,12px) clamp(12px,2.5cqw,22px)!important;
}
a.hdar-ci-amazon-banner-wide .hdar-ci-title {
  font-size:clamp(16px,3.15cqw,26px)!important;
}
a.hdar-ci-amazon-banner-wide .hdar-ci-button {
  right:clamp(8px,2.5cqw,17px)!important;
}
@media(max-width:640px) {
  a.hdar-ci-amazon-banner-wide {
    min-height:140px!important;
  }
  a.hdar-ci-amazon-banner-wide .hdar-ci-button {
    right:7px!important;
  }
}
"""

def main():
    raw = P.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == EXPECTED_SHA, "Unexpected CURRENT.zip; do not overwrite"
    buf = BytesIO()
    changes = {}
    with ZipFile(BytesIO(raw)) as old, ZipFile(buf,"w") as new:
        names = old.namelist()
        assert len(names) == len(set(names)), "Duplicate ZIP path"
        assert {CSS, AMAZON, MAIN} <= set(names), "Expected current 0.1.19 files absent"
        assert old.testzip() is None, "Source ZIP corrupted"
        for info in old.infolist():
            before = old.read(info.filename)
            after = before
            if info.filename == CSS:
                decoded = before.decode("utf-8")
                assert "HD009 0.1.19" in decoded and "a.hdar-ci-amazon-banner .hdar-ci-button" in decoded, "CSS not recognized"
                assert "HD009 0.1.20" not in decoded, "Already updated"
                after = (decoded + append_css).encode("utf-8")
            elif info.filename == AMAZON:
                decoded = before.decode("utf-8")
                assert decoded.count("'0.1.19'") == 1, "CSS cache signature unexpected"
                after = decoded.replace("'0.1.19'","'0.1.20'").encode("utf-8")
            elif info.filename == MAIN:
                decoded = before.decode("utf-8")
                print("MAIN_HEAD", repr(decoded[:520]))
                pat = r"(?m)^(\s*\*\s*Version:\s*)0\.1\.19(?:-dev)?(\s*)$"
                updated, count = re.subn(pat, r"\g<1>0.1.20-dev\2", decoded)
                assert count == 1, "Expected plugin header version absent"
                after = updated.encode("utf-8")
            if before != after:
                changes[info.filename] = (len(before), len(after))
            new.writestr(info, after)
        new.comment = old.comment
    assert set(changes) == {CSS, AMAZON, MAIN}, "Unexpected modification set"
    output = buf.getvalue()
    with ZipFile(BytesIO(output)) as built:
        assert built.testzip() is None, "New ZIP CRC fail"
        assert set(built.namelist()) == set(names)
        assert "0.1.20-dev" in built.read(MAIN).decode()
        assert "HD009 0.1.20" in built.read(CSS).decode()
        assert "/v3/merchant/amazon/products/live/advanced" in built.read(AMAZON).decode()
        with tempfile.TemporaryDirectory() as td:
            php_files = [i for i in built.namelist() if i.endswith(".php")]
            for i in php_files:
                f = Path(td)/i
                f.parent.mkdir(parents=True,exist_ok=True)
                f.write_bytes(built.read(i))
                p = subprocess.run(["php","-l",str(f)],capture_output=True,text=True)
                assert p.returncode == 0,(i,p.stderr,p.stdout)
            print("PHP_LINT_PASS",len(php_files))
    P.write_bytes(output)
    print("CHANGED_FILES",changes)
    print("OUTPUT_ZIP_BYTES",len(output))
    print("OUTPUT_ZIP_SHA256",hashlib.sha256(output).hexdigest())
    print("DATAFORSEO_EXISTING_PATH_PRESERVED",True)

if __name__ == "__main__":
    main()
