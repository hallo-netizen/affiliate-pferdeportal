#!/usr/bin/env python3
from pathlib import Path
import sys

p=Path(sys.argv[1])
s=p.read_text(encoding="utf-8")
old="""        }finally{self::releaseLock($lock);}
        if($continue){$state=self::loadOrDefault();self::dispatchLoopback((string)($state['loopback_token']??''),$delay);}"""
new="""        }finally{self::releaseLock($lock);}
        if($continue){$state=self::loadOrDefault();$loopbackToken=(string)($state['loopback_token']??'');register_shutdown_function(static function() use ($loopbackToken,$delay): void {self::dispatchLoopback($loopbackToken,$delay);});}"""
if old not in s:
    raise SystemExit("SERIAL_DISPATCH_ANCHOR_MISSING")
s=s.replace(old,new,1)
p.write_text(s,encoding="utf-8")
print("PASS SERIAL_DISPATCH_AFTER_RELEASE_INJECTED")
