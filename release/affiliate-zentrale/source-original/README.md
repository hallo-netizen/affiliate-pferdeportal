# Originalquelle 6.72.308 – ausschließlich Testeingang

Dieses Verzeichnis ist **kein** Plugin-Release und kein CURRENT-Ersatz. Der ursprüngliche Nutzer-Upload vom 08.11.2026 ist nachweislich erfolgt, wurde damals geöffnet, geprüft und gehasht, aber nicht dauerhaft als vollständige ZIP im GitHub-Repository gesichert.

Nur die unveränderte Original-ZIP gehört hierher:

- Dateiname: `AFFILIATE_ZENTRALE_6.72.308_URSACHENFIX_GESAMTTEST_NUR_TEST.zip`
- Exakter SHA-256: `b4d8547fd2aa134f7f82f568db3a81df54bb7d2131fd0752e76e3f0ca2251fe0`
- Größe: 5.345.251 Bytes
- Quelle: tatsächlicher geprüfter Originalupload, kein Rückbau aus 6.72.211, kein 6.72.309-Ersatz

Der **bestehende** Testlauf unter `.github/workflows/ebay-business-only-hardlock-qa.yml` prüft bei einer ZIP in diesem Verzeichnis erst die bytegenaue Übereinstimmung, dann ZIP-Integrität, 66 Dateien, 23 PHP-Dateien, Originalversion 6.72.308 und alle **58** Patchabschnitte gemeinsam. Nur bei vollständigem Erfolg wird ein **nicht freigegebenes Test-ZIP** als GitHub-Actions-Artefakt erstellt. Echte WordPress/eBay-Abnahmetests bleiben notwendig.

**Solange das Original nicht physisch hier liegt:** Der Original-Gesamttest ist explizit **SKIPPED**; andere erfolgreiche Referenzprüfungen dürfen nicht als Originaltest dargestellt werden. Die Upload-Historie wird dadurch nicht bestritten. Keine Änderung an K0, Produktion, WordPress oder HivePress.
