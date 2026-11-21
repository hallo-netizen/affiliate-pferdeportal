# 18.11.2026 – Texterstellung Hobbydepot 0.4.23, MINIMALE DIAGNOSEKORREKTUR

**Maßgeblicher Auftrag: KEIN Umbau, KEIN Neubau, KEINE Eigenentwicklung. Bestehendes Originalplugin vom Pferdeatelier bereinigt.**

## Ursache und genau eine Korrektur
Im bestehenden Plugin brach `TXE_Diagnose::snapshot()` bei `K0_PORTAL_ADAPTER_PENDING` ab, da der reine Leseaufruf `TXE_K0_Article_Types::snapshot()` ungefangen die bestehende Sperre `K0_ARTICLE_TYPE_AUTHORITY_UNAVAILABLE` warf.

**Gezielte Fehlerbehebung innerhalb der bereits vorhandenen Diagnosefunktion:** Der exakt benannte Sperrfall wird als `status=BLOCKED`, `reason_code=K0_ARTICLE_TYPE_AUTHORITY_UNAVAILABLE`, `article_types=[]` angezeigt. Die K0-Typprüfung und ihre Sperre bleiben unverändert. Für alle anderen unerwarteten RuntimeExceptions bleibt der bisherige Fehlerpfad erhalten.

Die andere Änderung ist ausschließlich die WordPress-Pluginversionsanzeige `0.4.23-hobbydepot-bereinigung.2`. Keine zusätzlichen PHP-Dateien, Hooks, Fachentscheidungen, Kategorie-Abbildung, Recherche-, MINI-, K0- oder Importverarbeitung. Originale Test-Publish-Filter bleiben bestehen und halten importierte Artikel auch bei manuellem `publish`/`future` auf `draft` – **gewollter Testschutz, nicht stillschweigend entfernen**.

## Exakte Artefakte
- Ausgangsbasis `/hobbydepot/TEXTERSTELLUNG/ARBEITSKOPIEN/Texterstellung_Hobbydepot_0.4.23_BEREINIGT_TEST.zip`, SHA256 `c50caa2ed263fb1f42f4cd485ecb2d23bbece6df072d9cf8f55774161aa6e715`.
- Neuer Staging-TESTKANDIDAT im Hobbydepot-Dateienbüro `/hobbydepot/TEXTERSTELLUNG/INSTALLATIONSKANDIDATEN/Texterstellung_Hobbydepot_0.4.23_BEREINIGT_DIAGNOSE_TEST.zip`, SHA256 `86779493f975588520fe82148ee601568916fe69f1d0884207d5d6296781bc15`.
- Von 87 Dateien exakt **85 bytegleich**, 2 geändert: `texterstellung/includes/class-txe-diagnose.php`, `texterstellung/texterstellung.php`. Kein PSTE-, PSERC-, K0-, Kategorie-, Research-Source geändert. 2 historische Pferdeatelier-K0-Kompatibilitätskennungen bleiben erhalten; alle fachlichen Pferde-Begriffe bereits in Vorversion entfernt.

## Lokale technische Nachweise
- ZIP CRC 87/87 PASS; PHP-Lint 78/78 PASS; JSON 8/8 PASS.
- WordPress-Startsimulationen 3/3 PASS: unbestätigte Site (PSTE aus), bestätigte isolierte Testsite (PSTE original), Legacy-Plugin-Kollision (blockiert), jeweils 0 Test-WordPress-Writes.
- PHP-Funktions-/Bedienseitentest **25/25 PASS**, jetzt inklusive Diagnoseseite und Diagnose-JSON mit `BLOCKED`, ohne Freigabe unerlaubter Typen.
- Original-PSERC-Rückimport **5/5 PASS** gegen WordPress-Mock, als Entwurf. Veröffentlichungsschutz weiterhin aktiv. Keine Provider-/Kostenaufrufe in Mocks.
- **Echte WordPress-/DataForSEO-/MINI-/K0-End-to-End-Abnahme NICHT erfolgt.** K0-Hobby-Portalzuordnung weiterhin lediglich für `discgolf-beratung` belegt; keine flächendeckende Produktionsfreigabe.

## Nächste echte Handlung
Staging-TESTINSTALLATION der genannten ZIP auf einer **isolierten WordPress-Testseite** (nicht Live), Testseiten-Bestätigung nur bei tatsächlich isolierter Testumgebung. Sechs vorhandene Arbeitsbereiche inkl. Diagnose prüfen und den vorhandenen Diagnose-JSON einmal exportieren; keine bezahlte Recherche, kein K0-Export mit nicht autorisierten Kategorien und kein Livepublishing.

Umfang ist eine **einzige Fehlerkorrektur am bestehenden Plugin**, kein Neubau oder Architekturwechsel. Vorgängerfassung archiviert, K0 und Pferdeatelier-Original unangetastet.

Ausführlicher MD+JSON-Prüfbericht im Hobbydepot-Büro `/hobbydepot/TEXTERSTELLUNG/PRUEFBERICHTE/Texterstellung_Hobbydepot_0.4.23_DIAGNOSE_KORREKTUR_PRUEFBERICHT.*`.
