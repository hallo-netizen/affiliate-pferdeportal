<?php
if (!defined('ABSPATH')) { exit; }

final class APKW_Settings {
    private const OPT_LOGIN = 'apkw_dataforseo_login';
    private const OPT_PASSWORD = 'apkw_dataforseo_password';
    private const OPT_LOCATION = 'apkw_default_location_name';
    private const OPT_LANGUAGE = 'apkw_default_language_code';

    public static function credentials(): array {
        $login = defined('APKW_DFS_LOGIN') ? (string) APKW_DFS_LOGIN : (string) get_option(self::OPT_LOGIN, '');
        $password = defined('APKW_DFS_PASSWORD') ? (string) APKW_DFS_PASSWORD : (string) get_option(self::OPT_PASSWORD, '');
        return ['login' => trim($login), 'password' => trim($password), 'source' => defined('APKW_DFS_LOGIN') && defined('APKW_DFS_PASSWORD') ? 'wp-config' : 'wordpress-option'];
    }

    public static function defaults(): array {
        return [
            'location_name' => (string) get_option(self::OPT_LOCATION, 'Germany'),
            'language_code' => (string) get_option(self::OPT_LANGUAGE, 'de'),
        ];
    }

    public static function save(array $input): void {
        if (!defined('APKW_DFS_LOGIN')) {
            update_option(self::OPT_LOGIN, sanitize_text_field((string) ($input['login'] ?? '')), false);
        }
        if (!defined('APKW_DFS_PASSWORD')) {
            $password = trim((string) ($input['password'] ?? ''));
            if ($password !== '') {
                update_option(self::OPT_PASSWORD, $password, false);
            }
        }
        update_option(self::OPT_LOCATION, sanitize_text_field((string) ($input['location_name'] ?? 'Germany')), false);
        update_option(self::OPT_LANGUAGE, sanitize_key((string) ($input['language_code'] ?? 'de')), false);
    }

    public static function constants_active(): bool {
        return defined('APKW_DFS_LOGIN') && defined('APKW_DFS_PASSWORD');
    }
}
