from pathlib import Path
import sys
p=Path(sys.argv[1]); s=p.read_text()
repls = {
'''background_selfpump_gate(){ local src="$1" p="$2" core_version="${3:-7.0.1}" port="${4:-8099}" tag="${core_version//./_}" out="$E/$p/V652_BACKGROUND_SELFPUMP_$tag"; mkdir -p "$out"; setup_wp "$core_version"''':
'''background_selfpump_gate(){\n local src="$1" p="$2" core_version="${3:-7.0.1}" port="${4:-8099}"\n local tag="${core_version//./_}"\n local out="$E/$p/V652_BACKGROUND_SELFPUMP_$tag"\n mkdir -p "$out"; setup_wp "$core_version"''',
'''background_lock_failclosed_gate(){ local src="$1" p="$2" core_version="${3:-7.0.1}" port="${4:-8101}" tag="${core_version//./_}" out="$E/$p/V652_CRON_LOCK_FAILCLOSED_$tag"; mkdir -p "$out"; setup_wp "$core_version"''':
'''background_lock_failclosed_gate(){\n local src="$1" p="$2" core_version="${3:-7.0.1}" port="${4:-8101}"\n local tag="${core_version//./_}"\n local out="$E/$p/V652_CRON_LOCK_FAILCLOSED_$tag"\n mkdir -p "$out"; setup_wp "$core_version"'''
}
for old,new in repls.items():
    if s.count(old)!=1:
        raise SystemExit('BLOCKED: V6.52 bash nounset local-init anchor mismatch')
    s=s.replace(old,new,1)
p.write_text(s)
