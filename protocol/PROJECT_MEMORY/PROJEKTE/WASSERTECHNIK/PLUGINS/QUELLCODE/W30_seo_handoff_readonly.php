<?php
/** W30: one read-only input adapter for the existing WT001 SEO stage. Not a WordPress plugin. */
declare(strict_types=1);

final class Wassertechnik_W30_Seo_Handoff {
    public static function read(string $path): array {
        if (!is_file($path) || !is_readable($path)) {
            throw new RuntimeException('W28-Handoff fehlt oder ist nicht lesbar.');
        }
        $raw = file_get_contents($path);
        if ($raw === false || $raw === '') {
            throw new RuntimeException('W28-Handoff leer.');
        }
        try {
            $data = json_decode($raw, true, 512, JSON_THROW_ON_ERROR);
        } catch (JsonException $e) {
            throw new RuntimeException('W28-Handoff kein gueltiges JSON.', 0, $e);
        }
        $master = 'protocol/PROJECT_MEMORY/PROJEKTE/WASSERTECHNIK/REGISTER_GLOSSAR/W27_ZENTRALES_FACHREGISTER_20261116.json';
        if (!is_array($data)
            || ($data['version'] ?? '') !== 'W28_2026-11-16'
            || ($data['einzige_masterquelle'] ?? '') !== $master
            || ($data['status'] ?? '') !== 'ABGELEITETER_EINMAL_HANDOFF_NICHT_AKTIVER_MASTER_KEINE_SEO_WP_FREIGABE'
            || ($data['anzahl'] ?? null) !== 81
            || !isset($data['produkte']) || !is_array($data['produkte']) || count($data['produkte']) !== 81
        ) {
            throw new RuntimeException('Falscher W28-Stand oder unvollstaendiger Handoff.');
        }
        $areas = ['PUMPEN', 'BRUNNEN', 'REGEN', 'TRINK', 'MESSEN', 'ABWASSER', 'POOL'];
        $seenIds = []; $seenKeywords = []; $countCategories = 0;
        foreach ($data['produkte'] as $item) {
            if (!is_array($item)) throw new RuntimeException('Defekter Produktdatensatz.');
            $id = $item['register_id'] ?? '';
            $key = trim((string)($item['keyword_vorschlag_ungeprueft'] ?? ''));
            if (!is_string($id) || !preg_match('/^W(?:12|14|15|16)-\d{3}$|^W(?:17|18|19|20|21|22|23)-P\d{3}$/D', $id)
                || ($item['kanonisch_id'] ?? null) !== $id
                || isset($seenIds[$id]) || $key === '' || isset($seenKeywords[$key])
                || !in_array($item['geplanter_hauptbereich'] ?? null, $areas, true)
                || ($item['fachstatus'] ?? '') !== 'marktprodukt'
                || ($item['seo_status'] ?? '') !== 'ungeprueft'
                || ($item['w5_suchvolumen'] ?? '') !== 'nicht_gemessen'
                || ($item['seo_owner_freigabe'] ?? null) !== false
                || ($item['wp_seitenfreigabe'] ?? null) !== false
                || !isset($item['quellen']) || !is_array($item['quellen']) || count($item['quellen']) < 1
                || !isset($item['artikelkategorien']) || !is_array($item['artikelkategorien']) || count($item['artikelkategorien']) < 1
                || !isset($item['referenzierte_funktionsvergleiche']) || !is_array($item['referenzierte_funktionsvergleiche'])
            ) {
                throw new RuntimeException('Ungültiger/duplizierter oder fälschlich freigegebener Kandidat: ' . (string)$id);
            }
            foreach ($item['artikelkategorien'] as $cat) {
                $ideas = $cat['article_ideas'] ?? null;
                if (!is_array($cat) || !is_string($cat['name'] ?? null) || !is_array($ideas) || count($ideas) < 3
                    || count(array_unique(array_map('trim', $ideas))) !== count($ideas)) {
                    throw new RuntimeException('Artikelrubrik ohne mindestens drei unterschiedliche Ideen: ' . $id);
                }
                ++$countCategories;
            }
            $seenIds[$id] = true; $seenKeywords[$key] = true;
        }
        if ($countCategories !== 90) throw new RuntimeException('W28-Rubrikzahl nicht 90.');
        return ['status' => 'NUR_EINGELESEN_KEINE_SEO_ENTSCHEIDUNG', 'anzahl' => 81, 'rubriken' => 90, 'produkte' => $data['produkte']];
    }
}
