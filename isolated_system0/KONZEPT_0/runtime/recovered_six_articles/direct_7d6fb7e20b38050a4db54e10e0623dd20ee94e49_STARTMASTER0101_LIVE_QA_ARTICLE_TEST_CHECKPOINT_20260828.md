# STARTMASTER0101 – Live-QA vor 6er-Artikeltest

## Stand
STARTMASTER0101 ist ein Dokumentations-/Live-QA-Checkpoint ohne Pluginänderung. PSTE 0.56.25 und PSERC 0.28.14 bleiben unverändert.

## Live-Produktionswelle
- UI vor Start: Ziel 40 / max. 40 Themenfamilien.
- Echter Abschluss: 2 neue eindeutige PASS-Themen aus 20 Themenfamilien.
- Abschluss: `MAX_FAMILIES_REACHED`.
- Status: **OPEN LIVE FAIL**. Ursache nicht geraten, nicht durch Wiederholung verdeckt.
- Der lokale 40/40-Test aus STARTMASTER0100 hat diesen produktiven Laufzustand nicht abgedeckt.

## Live-Snapshot danach
- SEO gesamt: 2419
- eligible: 11
- READY: 6
- REVIEW_REQUIRED_TARGET_KEYWORD: 1
- BLOCKED_EXISTING_CONTENT_DUPLICATE: 3
- REVIEW_REQUIRED_SEMANTIC_OVERLAP: 1

READY:
1. Pflege – Schritt für Schritt Pferdebürsten reinigen
2. Pflege – Schritt für Schritt Pferdebürsten waschen
3. Beratung – So findest du die geeigneten Rampenmatten für Pferdeanhänger
4. Beratung – So findest du ideale Heuraufen für Pferde
5. Beratung – So wählst du geeignete Ekzemerdecken für Pferde
6. Beratung – Wissenswertes über Weidetore für Pferde

## Titel-QA
Titel insgesamt zunächst akzeptiert. `Wissenswertes über Weidetore für Pferde` bleibt als echter Beobachtungsfall stehen: für Beratung sprachlich zu allgemein. Später soll Beratung Auswahl, Unterschiede, Kriterien oder Eignung erkennbar machen, ohne neue starre Schablone.

Titel-Hardlock bleibt: Target-Keyword/echter Longtail = alleinige SEO-Autorität. Attribute/Qualifizierer = 0 SEO-Autorität; ausschließlich menschliche, geschmeidige, attraktive, direkte Oberfläche. Keine erfundenen Eigenschaften, Intents oder Fakten.

## Sandbox-/Bestandsreihenfolge – erkannt, aber absichtlich noch nicht umgebaut
Späterer Zielpfad: sichere Sandbox-`AUTO_REENTRY_ELIGIBLE`-Potenziale → gespeicherter Topic-/Keywordbestand/Retained Backlog → erst danach neue Provider-Recherche. Review-/unklare/veraltete Fälle bleiben fail-closed.

## Verbindliche Reihenfolge ab jetzt
1. Vor dem ersten Artikel genau einmal den Nutzer nach seinem verbindlichen Produktionsprompt fragen.
2. Danach alle 6 aktuellen READY-Fälle als echten Artikel-Testblock nach dem neuen Beschleunigungskonzept produzieren.
3. Während der echten Produktion Optimierungspotenzial protokollieren: Nullpunkte/Wiederverwendung, unnötige Doppelprüfungen, Recherche, Übergaben, LanguageTool, GitHub/Prüfstände und reale Zeitfresser – ohne Qualitätsverlust und ohne Regelumbau während des Tests.
4. Erst nach diesem Test Root-Cause-Fix des Live-40/40→20/2-FAILs.
5. Ebenfalls erst danach Sandbox/Bestand/Provider-Reihenfolge umbauen.
6. Jeder spätere Fix einzeln positiv/negativ gegen den gesamten Workflow, danach Source → Installer-Re-Extract → MASTER-Re-Extract. Vorher keine Pluginfreigabe.

## Datenbank
PSERC 0.28.14 Retention live abgeschlossen: 37 → 3 Generationen; `slfo_options` nach Rebuild 236,0 MiB.

Keine Veröffentlichung ohne separate Freigabe.