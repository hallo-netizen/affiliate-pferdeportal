from pathlib import Path
import sys
p=Path(sys.argv[1]); s=p.read_text()
old="""  grep -Fxq 'ASSERTIONS=36 FAIL=2' \"$E/$p/v651_arch_old_version_red.log\" || return 1\n  grep -Fxq 'FAIL final version is 6.51.0' \"$E/$p/v651_arch_old_version_red.log\" || return 1\n  grep -Fxq 'FAIL final runtime build exact' \"$E/$p/v651_arch_old_version_red.log\" || return 1\n"""
new="""  grep -Fxq 'ASSERTIONS=36 FAIL=3' \"$E/$p/v651_arch_old_version_red.log\" || return 1\n  grep -Fxq 'FAIL final version is 6.51.0' \"$E/$p/v651_arch_old_version_red.log\" || return 1\n  grep -Fxq 'FAIL final runtime build exact' \"$E/$p/v651_arch_old_version_red.log\" || return 1\n  grep -Fxq 'FAIL README documents final technical contract' \"$E/$p/v651_arch_old_version_red.log\" || return 1\n"""
if s.count(old)!=1:
    raise SystemExit('BLOCKED: V6.52 final V6.51 legacy-red anchor mismatch')
p.write_text(s.replace(old,new,1))
