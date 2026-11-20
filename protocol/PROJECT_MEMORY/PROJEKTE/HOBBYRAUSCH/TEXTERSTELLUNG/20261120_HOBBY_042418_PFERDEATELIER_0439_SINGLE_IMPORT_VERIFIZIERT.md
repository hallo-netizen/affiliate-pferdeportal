# Hobbydepot MINI: Pferdeatelier 0.4.39 Original-Einmalimport übertragen (20.11.2026)

## Bestand und Grund
- Horse Original 0.4.39 `Texterstellung-0.4.39-MINI-EINMALIMPORT.zip`, SHA256 `43380f8cf105d8d8713cbba6de1f9113533409e25349113c6b4410a907c270aa`, Stand Pferdeatelier-Büro.
- Horse neuer originaler `MINI_SINGLE_FILE_REIMPORT_V1` akzeptiert nur eine extern final freigegebene Rückgabedatei, die CATEGORY, EDITORIAL und TITLE **außerhalb** WordPress durch je einen Worker samt technischer Reparatur-/Freigabeprüfung durchlaufen hat.
- Hobby 0.4.24.17 erfüllte zwar **eine** Datei, aber mit anderem Mechanismus: Original `TEXTERSTELLUNG_SINGLE_EDITOR_BATCH_V1` wurde unfreigegeben akzeptiert und erst *innerhalb* WordPress durch drei Worker-Checkpoint-Funktionen bearbeitet. Damit fehlte die aktuelle Pferdeatelier-Externausschleuse.

## Abschlusskorrektur
- Neuestes Hobby-Plugin **0.4.24.18** – genau eine geänderte Hauptdatei `texterstellung.php`, alle übrigen **86/87 unverändert**. Originale `miniSingleImport`-Methode **byteidentisch** zu Horse 0.4.39.
- Der normal aktuelle Dateirückweg erwartet `MINI_SINGLE_FILE_REIMPORT_V1` mit Original-Quellen- und Mitarbeiterbeleg, Identitätsprüfsumme und genau einem Nachweis; unbearbeitete Rückgabe ohne diesen Vertrag blockiert mit `MINI_SINGLE_RELEASE_REQUIRED`.
- Bereits existierende historische Einzelcheckpoint-Rückgaben bleiben technisch rückwärtskompatibel, nicht der Normalweg.
- Backend-Texte: MINI-Export → EINMAL intern in GitHub/Chat bearbeiten und technisch freigeben → **eine** MINI-Importdatei → K0-Regal. Keine zusätzlichen kostenpflichtigen DataForSEO-Abfragen oder Änderung von Original K0, K-Multi, PSERC.
- ZIP `Texterstellung_Hobbydepot_0.4.24.18_PFERDEATELIER_ORIGINAL_MINI_EINMALIMPORT.zip`, SHA256 `03f21ca678f003ab55a2a3a86ccd44c0cceb1ed59b2cb1e6a758b6bb129de19b`, 519234 Bytes, 87 Einträge, 78 PHP-Syntaxchecks PASS.

## Tatsächlicher Testbeweis
- **Echter 20er Originalexport** `mini-20261120094038-87239ec1a38a` + bereits eingefrorene 20 CATEGORY-Belege + bereits existierende 20 EDITORIAL- und 3 TITLE-Entscheidungen durch originale externe Pferdeatelier-Gates `mini_release_gate.py` und `mini_single_release.py` lokal durchgelaufen: Ausgabe EINE freigegebene `MINI_SINGLE_FILE_REIMPORT_V1`, 0 neue CATEGORY-Entscheidungen. Fehlender Titel → Reparatur, manipulierte Quelle → Block, alte falsche Ausgabe wird gelöscht.
- Aus dem FINALEN Hobby-ZIP extrahierte PHP-Klassen gegen ECHTEN 20er-Export in kontrollierter WordPress-Mockumgebung: **20 DONE, 3 K0-Aufträge, 17 KLAERUNG, 0 Fehler**, ein Eintragsspeichervorgang, idempotentes Wiederholen ohne Duplikate, gezielte negative Tests gegen Quelle, Redaktionsbelege, Titel, Index, Regelvertrag und alte unfreigegebene Gesamtdatei.
- **92/92 konkrete Positiv-/Negativ-Checks** = 56 reale 20er-Methoden, 13 Gates/Reparatur, 22 originale Recherche→K0→Mock-WP-Regressionen, 1 echtes Admin-MINI-Import-Formular. Dazu **78 PHP-Lint PASS, 87 ZIP-CRC PASS, 86 identische Dateien**.
- Keine neue Recherche bezahlt, kein echter WP-Live-Import, kein vollwertiger neuer K-Multi-Writer/LT6.8-Nachweis. K-Multi-Profil weiterhin `NO_VALUES_BLOCKED`.

## Einschränkung: technischer GitHub-Ausstellerbeweis
`release.payload_sha256` prüft die Datei vollständig auf Veränderung und WordPress prüft jedes ursprüngliche Element. Es ist jedoch **keine digitale GitHub-Ausstellersignatur**; die originale Pferdeatelier-0.4.39-Methode allein kann daher nicht kryptografisch belegen, dass ein Dokument ursprünglich vom externen Runner freigegeben wurde. Dieses verbliebene Original-Integritäts-/Authentizitätsdelta offen benennen und keine stärkere Garantie behaupten. Keine weitere Pluginkorrektur ohne konkrete Freigabe.

## Ablage und nächster Schritt
Aktuelles Plugin, lesbarer kompletter Vergleich, maschinenlesbarer 92er-Test und ausführbare Tests unter **`/Hobby Depot/Plugin-Büro/`**; `Texterstellung-CURRENT.md` auf 0.4.24.18 gesetzt.

Die bereits ausgegebenen **3 Hobbydepot Bogenschießen-K0-Aufträge** nicht erneut in MINI importieren. Das Pluginupdate dient für neue/still offene MINI-Chargen. Nach Backup bestehendes Plugin überinstallieren. Für einen neuen Auftrag: `Texterstellung → MINI-Export`, EINEN Originalauftrag, drei Worker extern, EINMAL Gate, eine `MINI_EINMAL_REIMPORT.json` unter `Texterstellung → MINI-Import → MINI-Ergebnis übernehmen`. Nach echtem WP-Import aktuelle Diagnose sichern.
