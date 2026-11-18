# Hobbydepot – Texterstellung: aktueller Stand

**Status:** ARBEITSKOPIE 0.4.23 ERHALTEN; INSTALLATIONSKANDIDAT 0.4.24 GEPRÜFT, ABER NICHT FÜR LIVE FREIGEGEBEN. Stand: 16.11.2026.

- Source: Texterstellung 0.4.23; eigene ZIP: `/hobbydepot/TEXTERSTELLUNG/ARBEITSKOPIEN/Texterstellung_HOBBYDEPOT_ARBEITSKOPIE_0.4.23.zip`.
- Identität der ZIP (SHA-256): `03ffe443d6879ca4170cc8660aceb8b567cbc7a85d8673e9b00bea90971420dc`.
- WordPress-Live-Abnahme: **NEIN**.
- Portaleigene Fachregeln vollständig: **NEIN** (74 von 78 PHP-Dateien mit Pferde-/PSTE-Suchtreffern; Anzahl der tatsächlich fachlich zu ändernden Stellen noch nicht bewertet).
- Alte Pferde-Kategoriekarte und Familien-Overrides: **entfernt, nicht durch Schätzwerte ersetzt**.
- K0-Änderungen: **0**.
- Redaktionsplan zurückgesetzt: **NEIN**, gesonderter aktueller Export steht aus.
- Nächste Aufgabe: Portalanpassung im jeweiligen eigenen Chat, danach eigenständige Installationsfreigabe.

## Portierung 0.4.24 – separater Prüfstand (16.11.2026)

- Neue ZIP im Hobbydepot-Dateienbüro: `/hobbydepot/TEXTERSTELLUNG/INSTALLATIONSKANDIDATEN/Texterstellung_Hobbydepot_0.4.24_INSTALLATIONSKANDIDAT.zip`.
- Eigener WordPress-Pluginordner; 79 PHP-Dateien syntaktisch geprüft, ZIP-CRC bestanden. K0-Importer unverändert.
- Pferde-Kategorie- und Seed-Daten sind entfernt; die alten Pferde-Journal-/Tarif-Sonderrouten für Hobbydepot stillgelegt. Nur auf hobbydepot.de administrativ aktivierbar.
- **Noch keine Produktionsfreigabe:** Kategorieabgleich HD-004 → Recherche-/MINI-Vertrag nicht fertig; kein WordPress-DataForSEO-K0-Endtest. Automatischer fachlicher Start bleibt gesperrt.
- Vollständiger Einzelbeleg: `PORTIERUNG_0.4.24_INSTALLATIONSKANDIDAT_20261116.md` im gleichen Büro.

## 18.11.2026 – vollständiger Quellaudit 0.4.25

- **Neue getrennte Arbeitskopie 0.4.25 im Hobbydepot-Dateienbüro; NICHT INSTALLIEREN.** SHA-256 `d16f0950de6792313a1e9894740a51f15e92b20644d7584d04a06d75b8e2cde7`.
- Pferde-Spezialfälle im redaktionellen Programmcode entfernt. Der historische K0-Rückimportname bleibt genau zweimal als notwendige externe technische Kennung bestehen. Original-PSERC-Importer unverändert.
- Fehlerhafte Sperre gegen nachträgliches manuelles Veröffentlichen entfernt; Diagnose bereinigt. Stale-Research-Bootstrap und sämtliche manuellen Forschungs-/MINI-/K0-Produktionsaktionen technisch gesperrt, solange HD004→PSTE nicht **echt** verifiziert ist.
- **79/79 PHP-Lint; 16/16 lokale Vertragstests; 4/4 Bootstrap-Tests; 88/88 ZIP-Dateien PASS.** Das sind keine realen WordPress-/DataForSEO-/K0-Echtläufe.
- **Genau eine offene fachliche Arbeit:** HD004 read-only Kategorieabbildung aus dem echten WordPress nachweisen, dann einmaliger vollständiger Durchlauf. Keine Produktionsfreigabe und keine Benutzerinstallation bis dahin.
- Beleg im gleichen Büro: `QUELLENAUDIT_KISS_0425_20261118.md`. Ausführlicher Bericht und ZIP in `/hobbydepot/TEXTERSTELLUNG/`.

## 18.11.2026 – HD004-Originalcode und 0.4.26-Arbeitsstand

- Letzter überprüfter Source: `HOBBYDEPOT_TEXTERSTELLUNG_0.4.26_QUELLE_NICHT_INSTALLIEREN.zip` im Hobbydepot-Dateienbüro; vorherige 0.4.25 unverändert archiviert.
- Original-HD004 1.0.0 aus GitHub-ZIP **tatsächlich geöffnet und geprüft**; vorhandene Runtime-API belegt, aktuelle Live-Werte noch nicht geprüft.
- Die vorhandene Texterstellungs-Diagnose liest künftig eine reine HD004-Kategorieübersicht: keine neue Kategorieentscheidung und kein weiteres Diagnose-Plugin.
- Tests: 80/80 PHP-Lint, 89/89 ZIP, 16/16 Bestand, 4/4 Start, 10/10 neue HD004-Simulationen. Original-PSERC-K0 unverändert.
- Keine Livefreigabe, keine WordPress-/DataForSEO-/K0-Echtprüfung. Keine Benutzerinstallation. Fachliche Kategorie-/Artikelart-Anbindung bleibt die EINZIGE offene Entwicklungsaufgabe.
- Einzelbeleg: `HD004_BINDUNG_ARBEITSSTAND_0426_20261118.md` in diesem Büro; Dateienbericht `/hobbydepot/TEXTERSTELLUNG/PRUEFBERICHTE/HOBBYDEPOT_TEXTERSTELLUNG_0.4.26_ZWISCHENSTAND.md`.

## 18.11.2026 – K0-Artikelarten: Schutzsperre nachgewiesen

- Hobbydepot-Kopie nennt `authority=K0_PORTAL_ADAPTER_PENDING`; `TXE_K0_Article_Types::all()` verlangt aber zurecht `K0_RULE_VALUES_JSON` und meldet im lokalen Realcode-Aufruf `K0_ARTICLE_TYPE_AUTHORITY_UNAVAILABLE`. **Nicht freigeben und nicht durch bloßes Umbenennen reparieren.**
- Im vorhandenen historischen Repo `hallo-netizen/k0-multiportal/quarantine/k0_sources/RULE_VALUES.json.source` stehen nur vier Arten mit Regeldefinitionen: Beratung, FAQ, Pflege, Vergleich. Die Hobbydepot-Vorliste mit zusätzlich Anleitung ist **nicht** als heutige produktive Regelquelle bestätigt. Die aktuelle K0-Typquelle muss vor Freigabe geprüft werden.
- Die offen gebliebene Integration umfasst nun ausdrücklich sowohl (a) HD004→PSTE-Livekategorie-/Artikelartenbindung als auch (b) Abgleich mit der aktuellen K0-Regelautorität, beides innerhalb eines Sammelreleases; keine zusätzliche nachgelagerte Fachentscheidung.
