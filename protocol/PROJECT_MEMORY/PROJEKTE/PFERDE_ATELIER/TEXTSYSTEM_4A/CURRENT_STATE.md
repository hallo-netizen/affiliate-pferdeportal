# TEXTSYSTEM 4A – CURRENT STATE

STAND: 2026-09-13
STATUS: AKTIV / AUDIT- UND HÄRTUNGSBÜRO

## Gesicherter Ausgangsbefund

- System 4 läuft isoliert in PR #238, Branch `hobbyroom/system4-true-single-room-v1`, geprüfter Head bei dieser Architekturprüfung: `77c02a9df1745a28157fcc27f65f74e9c4fb1153`.
- System 4 ist weiterhin nicht als Gesamtproduktion freigegeben; für den aktuellen Head fehlt der vollständige aktuelle Unittest-/E2E-Beweis.
- Der System-4-Kern besitzt bereits: kanonischen Artikelzustand, gebundene Phasen, Research/Facts/Context, Same-Article-Repair, interne Content-/Designprüfungen und zentralen FULL-Production-Check.

## Entscheidung 4 vs. 4a

**Ein eigenständiges 4a-Laufzeitsystem wird derzeit nicht gebaut.**

Grund: Nach Bereinigung behebbarer Hardcodes bleibt kein ausreichender struktureller Unterschied übrig, der eine zweite Text-/Workflowarchitektur rechtfertigt. Die gewünschte 4a-Zielform ist im Wesentlichen die konsequente Härtung von Konzept 4 selbst.

Die feste 7er- bzw. `Beratung`-Bindung ist ausdrücklich **kein Entscheidungskriterium**. Sie wird separat aus Konzept 4 entfernt.

## Nachgewiesener struktureller Härtungspunkt in Konzept 4

Der aktuelle `controller.py` bietet technisch mehrere Wege an:
- `check` → BASIC_ARCHITECTURE → `release`;
- `fullcheck` → produktionsnaher FULL-Pfad;
- `prepare-release` → `SIGNATURE_REQUIRED` → `finalize-signed`.

Der aktuelle System-4-Zielvertrag verlangt dagegen nur den FULL-Pfad mit anschließendem Batch-/Direct-Import-Handoff und ausdrücklich keinen Signaturweg.

Damit besteht noch technische Wahlfreiheit, obwohl fachlich nur eine Straße erlaubt sein soll.

## Richtige Zielarchitektur

`1 Produktionscontroller + N unabhängige Artikelzustände + bestehende reale Prüfer als interne Aufrufe + 1 finaler Ausgang`

Keine zweite Textmaschine. Keine zweite State Machine. Keine neue Prüferautorität.

## WordPress frisch geprüft

Reale Library-ZIP geprüft:
`portal-seo-editorial-plan-compiler_0.28.23_SYSTEM4_DIRECT_IMPORT.zip`
SHA-256: `22a8459b64db488852841d894d887ec51e531a0872ee5f33afdd64e43a8a8c7f`

Der Importer 0.28.23 unterstützt bereits den generischen Vertrag `SYSTEM4_WORDPRESS_HANDOFF_V1`, mindestens 1 Artikel ohne feste Obergrenze im Importcode und frei gebundene `article_type`-Werte. Er erstellt ausschließlich WordPress-Entwürfe, prüft Kategorie/Slug/Kollisionen vollständig vor dem ersten Write, validiert nach dem Schreiben per Readback und rollt bei Fehlern bereits erzeugte Posts zurück.

Der vorgelagerte Metadatenvertrag erlaubt exakt fünf skalare Felder pro Artikel:
`title`, `target_keyword`, `category`, `article_type`, `plan_slot`.
Inhalts-, Design- und Promptfelder sind dort ausdrücklich verboten; `maximum_articles=0` und `maximum_articles_per_type=0` bedeuten unbegrenzt.

Details: `WORDPRESS_HANDOFF.md`.

## Unverändert / unangetastet

- bestehende Textmaschine und Fachregeln;
- PPM 6.7.9;
- LanguageTool 6.8 / Bestand 43;
- PSERC/PSTE/SEO-/Link-/Tabellen-/Metadatenregeln;
- Design, Theme/CSS, WordPress-Plugin;
- offizieller STARTMASTER/CURRENT_STATE;
- System 4 / PR #238;
- `publish_allowed=false`.

## Offene Arbeit

1. Konzept 4 auf genau eine technisch erreichbare Produktionsstraße reduzieren;
2. 7er-/`Beratung`-Hardcodes separat entfernen;
3. finalen generischen Handoff auf `SYSTEM4_WORDPRESS_HANDOFF_V1` vereinheitlichen;
4. danach harte Positiv-/Negativtests inklusive 1/3/25/1000 und mehrerer bereits freigegebener Beitragsarten;
5. erst bei realem E2E-PASS Produktionsfreigabe neu bewerten.

Kein PASS wird aus dieser Architekturprüfung abgeleitet.
