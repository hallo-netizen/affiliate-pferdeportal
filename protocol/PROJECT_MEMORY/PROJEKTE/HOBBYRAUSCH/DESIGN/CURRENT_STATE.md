# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-20
STATUS: **1.50.704 HOBBYFINDER-VOLLBESTAND LOCAL HARD PASS / LIVE-INSTALLATION + READBACK OFFEN**

Zielvertrag: **ZV-HOBBYRAUSCH-DESIGN-001 Fassung 5.5 / 2026-10-19**

## Basis

1.50.704 basiert exakt auf **1.50.703**.

Unverändert erhalten:
- stabile Laufzeitklasse `Hobby_Depot_Profile_V150699`;
- Startseite 1.50.699 mit einzigem Hero-Weg Hobbyfinder;
- 69/69 Hub2-Einstiege;
- 395 Detail-Hubs;
- Kategoriebaum;
- Bilder;
- Affiliate-Slotarchitektur;
- Meta-/SEO-Titel;
- 1.50.703 Serviceseitentitel-/Footer-Fix.

1.50.700 bleibt verworfen und wird niemals als Basis verwendet.

## Neu 1.50.704 – Hobbyfinder

Die vorhandene WordPress-Seite mit Slug `hobbyfinder` wird als eigener Hobby-Depot-Content-Route gerendert.

Datenquelle:
**ausschließlich HD-007 Hobbyregister Core** über:
- `hd_hobbyregister_ready()`;
- `hd_hobbyregister_finder_rows()`.

HD-003 enthält **keine persistente Kopie** der 862 Hobbydatensätze.

Finder:
- 8 Schritte;
- eine Frage pro Bildschirm;
- große Auswahlkarten;
- Fortschritt + Zurück;
- harte Filter nur für explizite Nutzergrenzen;
- 6 Ergebnis-Hobbys;
- Passungswert + Begründungen;
- „Überrasch mich“;
- 4 zentrale Kurzprofilfelder je Ergebniskarte.

Ziel-URLs:
- ausschließlich über vorhandenes `hd_category_registry_resolve(target_node_id)`;
- keine erfundenen Slugs/URLs;
- aktueller Datenstand: **383** Hobbyidentitäten mit auflösbarem CORE-Ziel;
- übrige Identitäten werden angezeigt, aber ohne erfundenen CTA, solange kein echtes WordPress-Zielobjekt existiert.

Fail-closed:
Wenn HD-007 fehlt, nicht ready ist oder nicht exakt 862 geprüfte Datensätze liefert, erscheint nur ein neutraler Einrichtungs-Hinweis; kein Fatal Error und kein Fallback auf eine zweite Hobbyliste.

## Lokale QA 1.50.704

- PHP-Lint: **135/135 PASS**;
- geänderte Dateien gegen 1.50.703: exakt **3**;
- stabile Klasse/Templates: **PASS**;
- HD-007 Runtime-Readback: **862/862 PASS**;
- Kurzprofile: **862/862 PASS**;
- eindeutige Finder-IDs: **862/862 PASS**;
- über HD-004-Harness auflösbare Ziel-URLs: **383**;
- fehlendes HD-007: **FAIL-CLOSED PASS**;
- Hobbyfinder-Owned-Route: **PASS**;
- gerendertes Finder-JavaScript: **Syntax PASS**;
- ZIP-Integrität: **PASS**.

## Artefakt

`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.704_HOBBYFINDER_RUNTIME_LOCALPASS.zip`

Library:
`/Hobby Depot/Plugin-Büro/AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.704_HOBBYFINDER_RUNTIME_LOCALPASS.zip`

SHA-256:
`558ed2a17cd5123cdad5c7719d2554d64e413f628f29a07a1d06e6b4dca476fc`

Größe:
58,681,497 Bytes.

## Abhängigkeit

Für den Finder:
- **HD-007 1.0.0** muss aktiv sein;
- HD-004 ist für echte zentrale CORE-Ziel-URLs erforderlich; fehlt die Auflösung, wird keine URL erfunden.

## ERSTER OFFENER BLOCKER

Echter WordPress-/Frontend-Readback von **HD-007 1.0.0 + HD-003 1.50.704**.

## EXAKT EINE NEXT ACTION

**Zuerst HD-007 1.0.0 installieren/aktivieren, danach HD-003 1.50.704 installieren. Hobbyfinder real öffnen und prüfen: 8 Schritte, Ergebnisranking, vier Kurzprofilfelder, Überrasch-mich, vorhandene CORE-Ziellinks und fail-closed Verhalten. Kein Kategorie-Sync und kein erneuter Footer-Import.**
