<?php
if (!defined('ABSPATH')) { exit; }

final class APKW_Central_Category_Registry {
    private const OPT_CURRENT = 'apkw_central_category_registry_current_v1';
    private const OPT_FALLBACK = 'apkw_central_category_registry_fallback_v1';
    private const OPT_LOG = 'apkw_central_category_registry_change_log_v1';
    private const CONTRACT = 'APKW_CENTRAL_CATEGORY_REGISTRY_V1';
    private const INACTIVE_STATUSES = ['BLOCKED', 'DEPRECATED', 'REJECTED'];

    public static function current(): array {
        $value = get_option(self::OPT_CURRENT, null);
        return is_array($value) ? $value : self::empty_snapshot();
    }

    public static function fallback(): ?array {
        $value = get_option(self::OPT_FALLBACK, null);
        return is_array($value) ? $value : null;
    }

    public static function change_log(): array {
        $value = get_option(self::OPT_LOG, []);
        return is_array($value) ? array_values($value) : [];
    }

    public static function preview_package(array $package): array {
        $validation = APKW_Validator::validate($package);
        if (!$validation['valid']) {
            throw new RuntimeException('Zentraler Kategorienstand BLOCKED: ' . implode(', ', array_column($validation['errors'], 'code')));
        }
        if ((string)($package['mode'] ?? '') !== 'FINAL_APPROVED') {
            throw new RuntimeException('Zentraler Kategorienstand benötigt mode=FINAL_APPROVED.');
        }
        if ((string)($package['master_contract_id'] ?? '') !== APKW_MASTER_CONTRACT_ID) {
            throw new RuntimeException('MASTER_CONTRACT_MISMATCH');
        }

        $current = self::current();
        $nodes = self::active_nodes($validation['nodes']);
        $snapshot = [
            'contract' => self::CONTRACT,
            'generation' => ((int)$current['generation']) + 1,
            'source_master_contract_id' => APKW_MASTER_CONTRACT_ID,
            'source_package_id' => (string)($package['package_id'] ?? ''),
            'source_package_sha256' => self::hash_value($package),
            'category_set_sha256' => self::hash_value($nodes),
            'node_count' => count($nodes),
            'nodes' => $nodes,
        ];
        $diff = self::diff($current['nodes'] ?? [], $nodes);
        return [
            'status' => 'PASS_PREVIEW',
            'expected_previous_generation' => (int)$current['generation'],
            'expected_previous_sha256' => (string)$current['category_set_sha256'],
            'snapshot' => $snapshot,
            'diff' => $diff,
        ];
    }

    public static function commit_package(array $package, string $expected_previous_sha256, string $reason, bool $allow_deletions, int $actor_user_id): array {
        $preview = self::preview_package($package);
        $current = self::current();
        if (!hash_equals((string)$current['category_set_sha256'], $expected_previous_sha256)) {
            throw new RuntimeException('CENTRAL_CATEGORY_STALE_PREVIEW');
        }
        if (!empty($preview['diff']['removed']) && !$allow_deletions) {
            throw new RuntimeException('CENTRAL_CATEGORY_DELETION_CONFIRMATION_REQUIRED');
        }
        $reason = trim($reason);
        if ($reason === '') {
            throw new RuntimeException('CENTRAL_CATEGORY_CHANGE_REASON_REQUIRED');
        }

        $snapshot = $preview['snapshot'];
        $snapshot['activated_at_utc'] = gmdate('c');
        $snapshot['activated_by_user_id'] = $actor_user_id;
        $snapshot['change_reason'] = $reason;
        $snapshot['previous_category_set_sha256'] = (string)$current['category_set_sha256'];

        if ((int)$current['generation'] > 0) {
            self::write_option(self::OPT_FALLBACK, $current);
        }
        self::write_option(self::OPT_CURRENT, $snapshot);
        self::append_log([
            'action' => 'COMMIT',
            'generation' => (int)$snapshot['generation'],
            'timestamp_utc' => $snapshot['activated_at_utc'],
            'actor_user_id' => $actor_user_id,
            'reason' => $reason,
            'previous_sha256' => (string)$current['category_set_sha256'],
            'current_sha256' => (string)$snapshot['category_set_sha256'],
            'added' => $preview['diff']['added'],
            'removed' => $preview['diff']['removed'],
            'changed' => $preview['diff']['changed'],
            'node_count' => (int)$snapshot['node_count'],
        ]);
        return ['status'=>'PASS_COMMITTED','snapshot'=>$snapshot,'diff'=>$preview['diff']];
    }

    public static function rollback_to_fallback(string $reason, int $actor_user_id): array {
        $current = self::current();
        $fallback = self::fallback();
        if ($fallback === null || (int)($fallback['generation'] ?? 0) < 1) {
            throw new RuntimeException('CENTRAL_CATEGORY_FALLBACK_MISSING');
        }
        $reason = trim($reason);
        if ($reason === '') {
            throw new RuntimeException('CENTRAL_CATEGORY_ROLLBACK_REASON_REQUIRED');
        }

        $restored = $fallback;
        $restored['generation'] = ((int)$current['generation']) + 1;
        $restored['activated_at_utc'] = gmdate('c');
        $restored['activated_by_user_id'] = $actor_user_id;
        $restored['change_reason'] = $reason;
        $restored['previous_category_set_sha256'] = (string)$current['category_set_sha256'];

        self::write_option(self::OPT_FALLBACK, $current);
        self::write_option(self::OPT_CURRENT, $restored);
        self::append_log([
            'action' => 'ROLLBACK',
            'generation' => (int)$restored['generation'],
            'timestamp_utc' => $restored['activated_at_utc'],
            'actor_user_id' => $actor_user_id,
            'reason' => $reason,
            'previous_sha256' => (string)$current['category_set_sha256'],
            'current_sha256' => (string)$restored['category_set_sha256'],
            'added' => [],
            'removed' => [],
            'changed' => [],
            'node_count' => (int)$restored['node_count'],
        ]);
        return ['status'=>'PASS_ROLLED_BACK','snapshot'=>$restored];
    }

    public static function export_payload(): array {
        return self::current();
    }

    public static function status(): array {
        $current = self::current();
        return [
            'contract' => self::CONTRACT,
            'generation' => (int)$current['generation'],
            'category_set_sha256' => (string)$current['category_set_sha256'],
            'node_count' => (int)$current['node_count'],
            'fallback_available' => self::fallback() !== null,
            'change_count' => count(self::change_log()),
        ];
    }

    private static function active_nodes(array $nodes): array {
        $active = [];
        foreach ($nodes as $node) {
            if (!is_array($node)) { continue; }
            if (isset($node['active']) && $node['active'] === false) { continue; }
            if (in_array((string)($node['status'] ?? ''), self::INACTIVE_STATUSES, true)) { continue; }
            $active[] = self::sort_recursive($node);
        }
        usort($active, static fn(array $a, array $b): int => strcmp((string)($a['concept_id'] ?? ''), (string)($b['concept_id'] ?? '')));
        return $active;
    }

    private static function diff(array $old_nodes, array $new_nodes): array {
        $old = self::index($old_nodes);
        $new = self::index($new_nodes);
        $added = array_values(array_diff(array_keys($new), array_keys($old)));
        $removed = array_values(array_diff(array_keys($old), array_keys($new)));
        $changed = [];
        foreach (array_intersect(array_keys($old), array_keys($new)) as $id) {
            if (!hash_equals(self::hash_value($old[$id]), self::hash_value($new[$id]))) { $changed[] = $id; }
        }
        sort($added, SORT_STRING); sort($removed, SORT_STRING); sort($changed, SORT_STRING);
        return ['added'=>$added,'removed'=>$removed,'changed'=>$changed,'unchanged_count'=>count($new)-count($added)-count($changed)];
    }

    private static function index(array $nodes): array {
        $out = [];
        foreach ($nodes as $node) {
            if (!is_array($node)) { continue; }
            $id = (string)($node['concept_id'] ?? '');
            if ($id !== '') { $out[$id] = self::sort_recursive($node); }
        }
        ksort($out, SORT_STRING);
        return $out;
    }

    private static function empty_snapshot(): array {
        return [
            'contract' => self::CONTRACT,
            'generation' => 0,
            'source_master_contract_id' => APKW_MASTER_CONTRACT_ID,
            'source_package_id' => '',
            'source_package_sha256' => '',
            'category_set_sha256' => str_repeat('0', 64),
            'node_count' => 0,
            'nodes' => [],
        ];
    }

    private static function hash_value($value): string {
        $normalized = self::sort_recursive($value);
        $json = wp_json_encode($normalized, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
        if (!is_string($json)) { throw new RuntimeException('CENTRAL_CATEGORY_JSON_ENCODE_FAILED'); }
        return hash('sha256', $json);
    }

    private static function sort_recursive($value) {
        if (!is_array($value)) { return $value; }
        if (array_is_list($value)) { return array_map([__CLASS__, 'sort_recursive'], $value); }
        ksort($value, SORT_STRING);
        foreach ($value as $k => $v) { $value[$k] = self::sort_recursive($v); }
        return $value;
    }

    private static function write_option(string $name, $value): void {
        if (get_option($name, null) === null) {
            add_option($name, $value, '', 'no');
            return;
        }
        update_option($name, $value, false);
    }

    private static function append_log(array $entry): void {
        $log = self::change_log();
        $log[] = $entry;
        self::write_option(self::OPT_LOG, $log);
    }
}
