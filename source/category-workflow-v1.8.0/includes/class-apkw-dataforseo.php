<?php
if (!defined('ABSPATH')) { exit; }

final class APKW_DataForSEO {
    private const USER_DATA_ENDPOINT = 'https://api.dataforseo.com/v3/appendix/user_data';
    private const KEYWORD_IDEAS_ENDPOINT = 'https://api.dataforseo.com/v3/dataforseo_labs/google/keyword_ideas/live';
    private const KEYWORD_OVERVIEW_ENDPOINT = 'https://api.dataforseo.com/v3/dataforseo_labs/google/keyword_overview/live';
    private const KEYWORD_SUGGESTIONS_ENDPOINT = 'https://api.dataforseo.com/v3/dataforseo_labs/google/keyword_suggestions/live';
    private const MAX_IDEA_SEEDS = 200;
    private const MAX_OVERVIEW_KEYWORDS = 700;

    public static function test_connection(): array {
        $response = self::request('GET', self::USER_DATA_ENDPOINT, null);
        $cost = (float) ($response['decoded']['cost'] ?? 0);
        if (abs($cost) > 0.0000001) {
            throw new RuntimeException('DataForSEO-Verbindungstest meldet unerwartete Kosten und wird vorsorglich als BLOCKED behandelt.');
        }
        return [
            'ok' => true,
            'endpoint' => self::USER_DATA_ENDPOINT,
            'http_code' => $response['http_code'],
            'status_code' => (int) ($response['decoded']['status_code'] ?? 0),
            'status_message' => (string) ($response['decoded']['status_message'] ?? ''),
            'cost_usd' => $cost,
        ];
    }

    public static function keyword_ideas(array $keywords, string $location_name, string $language_code, int $limit = 300, bool $include_serp_info = false, string $tag = ''): array {
        $keywords = self::clean_keywords($keywords);
        if (!$keywords) { throw new RuntimeException('DataForSEO Keyword-Ideas: Seed-Keywords fehlen.'); }
        if (count($keywords) > self::MAX_IDEA_SEEDS) { throw new RuntimeException('DataForSEO Keyword-Ideas: maximal 200 Seed-Keywords pro Cluster.'); }
        self::validate_market($location_name, $language_code);

        $limit = max(10, min(1000, $limit));
        $task = [
            'keywords' => $keywords,
            'location_name' => trim($location_name),
            'language_code' => trim($language_code),
            'closely_variants' => false,
            'ignore_synonyms' => false,
            'include_serp_info' => $include_serp_info,
            'limit' => $limit,
            'order_by' => ['relevance,desc', 'keyword_info.search_volume,desc'],
            'tag' => $tag !== '' ? substr($tag, 0, 255) : 'apkw-ideas-' . substr(hash('sha256', implode('|', $keywords)), 0, 24),
        ];
        $body = self::json([$task]);
        $response = self::request('POST', self::KEYWORD_IDEAS_ENDPOINT, $body);
        return self::parse_live_items($response, self::KEYWORD_IDEAS_ENDPOINT, $task, $body);
    }

    public static function keyword_suggestions(string $keyword, string $location_name, string $language_code, int $limit = 50, bool $include_serp_info = false, string $tag = ''): array {
        $keyword = preg_replace('/\s+/u', ' ', trim($keyword));
        if ($keyword === '' || self::length($keyword) < 3) { throw new RuntimeException('DataForSEO Keyword-Suggestions: Seed-Keyword fehlt.'); }
        self::validate_market($location_name, $language_code);

        $limit = max(10, min(1000, $limit));
        $task = [
            'keyword' => $keyword,
            'location_name' => trim($location_name),
            'language_code' => trim($language_code),
            'include_seed_keyword' => true,
            'include_serp_info' => $include_serp_info,
            'include_clickstream_data' => false,
            'exact_match' => false,
            'ignore_synonyms' => false,
            'limit' => $limit,
            'order_by' => ['keyword_info.search_volume,desc'],
            'tag' => $tag !== '' ? substr($tag, 0, 255) : 'apkw-suggestions-' . substr(hash('sha256', $keyword), 0, 24),
        ];
        $body = self::json([$task]);
        $response = self::request('POST', self::KEYWORD_SUGGESTIONS_ENDPOINT, $body);
        return self::parse_live_items($response, self::KEYWORD_SUGGESTIONS_ENDPOINT, $task, $body);
    }

    public static function keyword_overview(array $keywords, string $location_name, string $language_code, bool $include_serp_info = false, string $tag = ''): array {
        $keywords = self::clean_keywords($keywords);
        if (!$keywords) { throw new RuntimeException('DataForSEO Keyword-Overview: Keywords fehlen.'); }
        if (count($keywords) > self::MAX_OVERVIEW_KEYWORDS) { throw new RuntimeException('DataForSEO Keyword-Overview: maximal 700 Keywords pro Aufruf.'); }
        self::validate_market($location_name, $language_code);

        $task = [
            'keywords' => $keywords,
            'location_name' => trim($location_name),
            'language_code' => trim($language_code),
            'include_serp_info' => $include_serp_info,
            'include_clickstream_data' => false,
            'tag' => $tag !== '' ? substr($tag, 0, 255) : 'apkw-overview-' . substr(hash('sha256', implode('|', $keywords)), 0, 24),
        ];
        $body = self::json([$task]);
        $response = self::request('POST', self::KEYWORD_OVERVIEW_ENDPOINT, $body);
        return self::parse_live_items($response, self::KEYWORD_OVERVIEW_ENDPOINT, $task, $body);
    }

    public static function max_overview_keywords(): int { return self::MAX_OVERVIEW_KEYWORDS; }
    public static function max_idea_seeds(): int { return self::MAX_IDEA_SEEDS; }

    private static function validate_market(string $location_name, string $language_code): void {
        if (trim($location_name) === '') { throw new RuntimeException('Zielmarkt fehlt.'); }
        if (trim($language_code) === '') { throw new RuntimeException('Sprachcode fehlt.'); }
    }

    private static function clean_keywords(array $keywords): array {
        $out = [];
        foreach ($keywords as $keyword) {
            $keyword = preg_replace('/\s+/u', ' ', trim((string) $keyword));
            if ($keyword === '' || self::length($keyword) < 3) { continue; }
            $key = self::key($keyword);
            if (!isset($out[$key])) { $out[$key] = $keyword; }
        }
        return array_values($out);
    }

    private static function request(string $method, string $endpoint, ?string $body): array {
        $credentials = APKW_Settings::credentials();
        if ($credentials['login'] === '' || $credentials['password'] === '') { throw new RuntimeException('DataForSEO-Zugangsdaten fehlen.'); }
        $args = [
            'timeout' => 60,
            'redirection' => 0,
            'headers' => [
                'Authorization' => 'Basic ' . base64_encode($credentials['login'] . ':' . $credentials['password']),
                'Accept' => 'application/json',
            ],
            'user-agent' => 'Affiliate-Portal-Kategorie-Workflow/' . APKW_VERSION,
        ];
        if ($method === 'POST') {
            $args['headers']['Content-Type'] = 'application/json; charset=utf-8';
            $args['body'] = (string) $body;
            $args['data_format'] = 'body';
            $response = wp_remote_post($endpoint, $args);
        } else {
            $response = wp_remote_get($endpoint, $args);
        }
        if (is_wp_error($response)) { throw new RuntimeException('DataForSEO-Verbindung fehlgeschlagen: ' . $response->get_error_message()); }
        $http_code = (int) wp_remote_retrieve_response_code($response);
        $raw_body = (string) wp_remote_retrieve_body($response);
        $decoded = null;
        try { $decoded = json_decode($raw_body, true, 512, JSON_THROW_ON_ERROR); }
        catch (Throwable $e) { $decoded = null; }
        if ($http_code < 200 || $http_code >= 300) {
            $provider_code = is_array($decoded) ? (int) ($decoded['status_code'] ?? 0) : 0;
            $provider_message = is_array($decoded) ? trim((string) ($decoded['status_message'] ?? '')) : '';
            $task = is_array($decoded) && is_array($decoded['tasks'][0] ?? null) ? $decoded['tasks'][0] : [];
            if ($provider_code === 0 && $task) { $provider_code = (int) ($task['status_code'] ?? 0); }
            if ($provider_message === '' && $task) { $provider_message = trim((string) ($task['status_message'] ?? '')); }
            $detail = '';
            if ($provider_code !== 0 || $provider_message !== '') {
                $detail = ' · DataForSEO ' . ($provider_code !== 0 ? (string) $provider_code : 'ohne Subcode') . ($provider_message !== '' ? ': ' . $provider_message : '');
            }
            throw new RuntimeException('DataForSEO HTTP-Fehler ' . $http_code . $detail . '.');
        }
        if (!is_array($decoded)) { throw new RuntimeException('DataForSEO-Antwort ist kein gültiges JSON.'); }
        if ((int) ($decoded['status_code'] ?? 0) !== 20000) { throw new RuntimeException('DataForSEO-Fehler: ' . (string) ($decoded['status_message'] ?? 'unbekannt')); }
        return ['http_code'=>$http_code, 'raw_body'=>$raw_body, 'decoded'=>$decoded];
    }

    private static function parse_live_items(array $response, string $endpoint, array $task, string $body): array {
        $decoded = $response['decoded'];
        $task_result = $decoded['tasks'][0] ?? null;
        if (!is_array($task_result) || (int) ($task_result['status_code'] ?? 0) !== 20000) {
            throw new RuntimeException('DataForSEO-Task fehlgeschlagen: ' . (string) ($task_result['status_message'] ?? 'unbekannt'));
        }
        $result = $task_result['result'][0] ?? [];
        $items = is_array($result['items'] ?? null) ? $result['items'] : [];
        return [
            'endpoint' => $endpoint,
            'request' => $task,
            'request_sha256' => hash('sha256', $body),
            'http_code' => $response['http_code'],
            'cost_usd' => (float) ($task_result['cost'] ?? $decoded['cost'] ?? 0),
            'task_id' => (string) ($task_result['id'] ?? ''),
            'result_total_count' => (int) ($result['total_count'] ?? $result['items_count'] ?? count($items)),
            'returned_count' => count($items),
            'normalized_items' => self::normalize_items($items),
            'raw_response' => $decoded,
            'raw_response_sha256' => hash('sha256', $response['raw_body']),
        ];
    }

    private static function normalize_items(array $items): array {
        $out = [];
        foreach ($items as $position => $item) {
            if (!is_array($item)) { continue; }
            $info = is_array($item['keyword_info'] ?? null) ? $item['keyword_info'] : [];
            $intent = is_array($item['search_intent_info'] ?? null) ? $item['search_intent_info'] : [];
            $props = is_array($item['keyword_properties'] ?? null) ? $item['keyword_properties'] : [];
            $keyword = preg_replace('/\s+/u', ' ', trim((string) ($item['keyword'] ?? '')));
            if ($keyword === '') { continue; }
            $out[] = [
                'provider_rank' => (int) $position + 1,
                'keyword' => $keyword,
                'search_volume' => isset($info['search_volume']) && is_numeric($info['search_volume']) ? (int) $info['search_volume'] : null,
                'monthly_searches' => is_array($info['monthly_searches'] ?? null) ? $info['monthly_searches'] : [],
                'cpc' => isset($info['cpc']) && is_numeric($info['cpc']) ? (float) $info['cpc'] : null,
                'competition' => isset($info['competition']) && is_numeric($info['competition']) ? (float) $info['competition'] : null,
                'competition_level' => isset($info['competition_level']) ? (string) $info['competition_level'] : null,
                'main_intent' => isset($intent['main_intent']) ? (string) $intent['main_intent'] : null,
                'foreign_intent' => is_array($intent['foreign_intent'] ?? null) ? $intent['foreign_intent'] : [],
                'core_keyword' => isset($props['core_keyword']) ? (string) $props['core_keyword'] : null,
                'keyword_difficulty' => isset($props['keyword_difficulty']) && is_numeric($props['keyword_difficulty']) ? (int) $props['keyword_difficulty'] : null,
                'detected_language' => isset($props['detected_language']) ? (string) $props['detected_language'] : null,
                'serp_info' => is_array($item['serp_info'] ?? null) ? $item['serp_info'] : null,
                'source_last_updated' => isset($info['last_updated_time']) ? (string) $info['last_updated_time'] : null,
            ];
        }
        return $out;
    }

    private static function json(array $data): string {
        $body = wp_json_encode($data, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
        if (!is_string($body)) { throw new RuntimeException('DataForSEO-Anfrage konnte nicht serialisiert werden.'); }
        return $body;
    }

    private static function key(string $value): string {
        $value = html_entity_decode($value, ENT_QUOTES | ENT_HTML5, 'UTF-8');
        $value = preg_replace('/\s+/u', ' ', trim($value));
        return function_exists('mb_strtolower') ? mb_strtolower((string) $value, 'UTF-8') : strtolower((string) $value);
    }

    private static function length(string $value): int { return function_exists('mb_strlen') ? mb_strlen($value, 'UTF-8') : strlen($value); }
}
