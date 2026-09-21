#!/usr/bin/env python3
from pathlib import Path
import sys

p = Path(sys.argv[1])
s = p.read_text(encoding="utf-8")

old = """    private static function quarantineCorruptedTopicRow(array &$poolRows,int $index,array $row,string $reasonCode): string {
        $table=self::table('topic_pool');$topic=(string)($row['pool_key']??'');
        if($topic==='')throw new RuntimeException('PSTE_PAYLOAD_RECOVERY_TOPIC_KEY_EMPTY');"""
new = """    private static function quarantineCorruptedTopicRow(array &$poolRows,int $index,array $row,string $reasonCode): string {
        global $wpdb;
        $table=self::table('topic_pool');$topic=(string)($row['pool_key']??'');
        if($topic==='')throw new RuntimeException('PSTE_PAYLOAD_RECOVERY_TOPIC_KEY_EMPTY');
        $traceBefore=$wpdb->get_row($wpdb->prepare("SELECT id,pool_key,normalized_key,candidate_id,LENGTH(payload_json) AS payload_len FROM ".$table." WHERE id=%d",(int)$row['id']),ARRAY_A);error_log('PSTE_QUARTRACE BEFORE t='.sprintf('%.6f',microtime(true)).' pid='.getmypid().' id='.(int)$row['id'].' stale_pool_key='.$topic.' reason='.$reasonCode.' db_row_b64='.base64_encode(wp_json_encode($traceBefore,JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES)));"""
if old not in s:
    raise SystemExit("QUARANTINE_ENTRY_ANCHOR_MISSING")
s = s.replace(old, new, 1)

old = """        self::checkedUpdate($table,$updated,['id'=>(int)$row['id']],['%s','%s','%s','%s','%s','%s','%s','%s','%s','%d','%s'],['%d'],'PSTE_PAYLOAD_RECOVERY_QUARANTINE_UPDATE_FAILED');
        self::assertTopicPayloadPersisted($topic,$encoded,'PSTE_PAYLOAD_RECOVERY_QUARANTINE');"""
new = """        self::checkedUpdate($table,$updated,['id'=>(int)$row['id']],['%s','%s','%s','%s','%s','%s','%s','%s','%s','%d','%s'],['%d'],'PSTE_PAYLOAD_RECOVERY_QUARANTINE_UPDATE_FAILED');
        $traceById=$wpdb->get_row($wpdb->prepare("SELECT id,pool_key,normalized_key,candidate_id,LENGTH(payload_json) AS payload_len FROM ".$table." WHERE id=%d",(int)$row['id']),ARRAY_A);
        $traceByKey=$wpdb->get_row($wpdb->prepare("SELECT id,pool_key,normalized_key,candidate_id,LENGTH(payload_json) AS payload_len FROM ".$table." WHERE pool_key=%s",$topic),ARRAY_A);
        error_log('PSTE_QUARTRACE AFTER_UPDATE t='.sprintf('%.6f',microtime(true)).' pid='.getmypid().' id='.(int)$row['id'].' expected_pool_key='.$topic.' by_id_b64='.base64_encode(wp_json_encode($traceById,JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES)).' by_key_b64='.base64_encode(wp_json_encode($traceByKey,JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES)));
        self::assertTopicPayloadPersisted($topic,$encoded,'PSTE_PAYLOAD_RECOVERY_QUARANTINE');"""
if old not in s:
    raise SystemExit("QUARANTINE_READBACK_ANCHOR_MISSING")
s = s.replace(old, new, 1)

old = """    public static function repairInvalidTopicPayloads(): array {
        self::assertOwnJsonStorageReady();"""
new = """    public static function repairInvalidTopicPayloads(): array {
        error_log('PSTE_QUARTRACE REPAIR_ENTER t='.sprintf('%.6f',microtime(true)).' pid='.getmypid().' uri='.(string)($_SERVER['REQUEST_URI']??'CLI'));
        self::assertOwnJsonStorageReady();"""
if old not in s:
    raise SystemExit("REPAIR_ENTRY_ANCHOR_MISSING")
s = s.replace(old, new, 1)

p.write_text(s, encoding="utf-8")
print("PASS QUARANTINE_TRACE_INJECTED")
