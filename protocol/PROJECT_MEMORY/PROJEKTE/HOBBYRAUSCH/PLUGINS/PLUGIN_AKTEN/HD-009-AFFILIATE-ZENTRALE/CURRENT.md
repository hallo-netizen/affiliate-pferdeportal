# HD-009 – Hobby Depot Affiliate-Zentrale – technische Pluginakte

Technischer Eintrag zur **einzigen** Affiliate-Statusautorität `../../../AFFILIATE/CURRENT_STATE.md`.

Einzige vollständige aktuelle GitHub-ZIP: `../../ISOLIERTE_PLUGINS/HD-009-AFFILIATE-ZENTRALE/CURRENT.zip`, **0.1.13-dev**. SHA-256 `d6536031f0eca61c15a2d8c754015ed92de3ad474da9a10e961782a076681d43`, 707164 Bytes, Blob `fd18e2caea3836a8054189edac67e70c9c6d10b0`. Normaler Pluginroot `affiliate-portal-router/`.

Ursache und Lösung: Die bereits aus Pferdeatelier übernommene zentrale Bannerautomatik (Fachziel/Elternpfad/Slot) lag unverändert im Hobby-Plugin. Die in 0.1.12 eingeführte separate manuelle Eigenbanner-Speicherung und -Ausgabe umging diese Automatik; beides wurde in 0.1.13 entfernt, Startmodus-Blockade aufgehoben. Für gültige Werbemittel gilt der ursprüngliche zentrale Auswahlweg. Erhaltene Motivdateien sind noch nicht als Werbemittel importiert.

Neue Funktion: **kostenloser DataForSEO-Verbindungstest** im bestehenden Menü `Affiliate-Zentrale → Amazon + idealo`, read-only GET `/v3/appendix/user_data`, keine Merchant-Suche, keine Hintergrundroutine, WordPress-Rechte- und Nonce-Schutz. Versionen/Konfiguration anderer Portale unberührt.

Prüfbericht: [HD009 0.1.13](EVIDENCE/HD009_0113_NATIVE_BANNER_DATAFORSEO_TEST_20261107.md). ZIP/24 PHP-Lint/4 simulierte API-Fälle bestanden. Echtes WordPress-Upgrade und DataForSEO-Loginprüfung ausstehend. Ältere 0.1.12- und 0.1.10-Protokolle sind historisch, nicht aktuelle Installationsversion.
