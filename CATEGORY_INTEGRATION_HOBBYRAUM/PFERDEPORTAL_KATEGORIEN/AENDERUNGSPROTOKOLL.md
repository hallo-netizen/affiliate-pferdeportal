# Pferdeportal Kategorien – Änderungsprotokoll

Status: VERBINDLICHE ZENTRALE ABLAGE.

## Harte Regeln

- Aktuelle WordPress-XML -> genau eine zentrale Kategorienliste.
- Keine Automatik.
- Kein Kategorieplugin.
- Kein erneutes Durchtesten alter Beweise.
- Keine zweite Kategorienquelle.

## 2026-09-23 – Ausgangsstand

Quelle:
- `pferdeatelier.WordPress.2026-09-23.xml`
- WordPress-Export: `2026-09-23 07:14 UTC`
- Quell-SHA256: `d4564160f1a73cd6f6c79b4afa6c53d7e6c0c593d2d9de9c53adbcc5adea3655`

Durchgeführte Änderung:
1. Ausschließlich die `<wp:category>`-Einträge der aktuellen XML übernommen.
2. Pro Kategorie nur `term_id`, `slug`, `name` und `parent_slug` gespeichert.
3. Keine Kategorie ergänzt, umbenannt, verschoben oder gelöscht.
4. Keine Plugin-, PPM-, Affiliate-, PSERC- oder sonstige Logik eingebaut.
5. Zentrale Liste: `KATEGORIEN.tsv`.
6. Der verworfene Kandidat `PFERDEPORTAL_KATEGORIEN_V0.2.0_CANDIDATE_MIN.zip`, seine Statusdatei und sein eigener Workflow wurden entfernt.

Bestand der aktuellen XML:
- Kategorien gesamt: **1160**

Ab jetzt gilt:
Jede spätere Kategorienänderung wird in `KATEGORIEN.tsv` eingetragen und hier protokolliert. Andere Plugins dürfen daraus nur ihren eigenen benötigten Stand ableiten; sie sind keine zweite Kategorienquelle.

## 2026-09-23 – Steuerstand nachgezogen

- `CURRENT_RELEASE.json` bindet die zentrale `KATEGORIEN.tsv` jetzt ausdrücklich als einzige Kategorien-Inhaltsquelle.
- Die bestehende Kategorieakte wurde entsprechend präzisiert.
- PPM-/Plugin-interne Kategorienbestände gelten nur noch als technische Ableitungen, nicht als zweite Wahrheit.
- Keine Kategorie geändert.

## 2026-10-08 – VORGEMERKTE STRUKTURBEREINIGUNG / NOCH NICHT UMGESETZT

NUTZERENTSCHEID:
Diese Strukturänderungen sind fachlich beschlossen und für eine spätere gemeinsame Umsetzung vorgemerkt. **Jetzt keine WordPress-, PSTE-, PSERC-, PPM-, Template- oder Affiliate-Änderung ausführen.** Aktueller Artikelworkflow hat Vorrang.

### 1. Fütterung / Wasser

IST:
- Fütterung → Wassertechnik → Isolierte Wasserleitungen

SOLL:
- Fütterung → Wasser → Isolierte Wasserleitungen

ENTSCHEID:
- separaten Bereichshub **Wassertechnik entfernen**;
- `Isolierte Wasserleitungen` unter den bestehenden Bereich **Wasser** hängen;
- darunter vorhandene Artikel-/Intentkategorien erhalten und nur fachlich neu binden;
- bestehende IDs/Slugs möglichst erhalten; keine unnötigen URL-Änderungen.

BEGRÜNDUNG:
Ein eigener Bereichshub mit nur einem Kind bläht das Megamenü ohne fachlichen Mehrwert auf. `Isolierte Wasserleitungen` gehört logisch in den bereits vorhandenen Wasserbereich.

### 2. Versicherungen

IST:
- Wissen → Versicherungen & Recht → Pferdehaftpflicht
- Gesundheit bleibt eigenständiger Gesundheitsbereich.

SOLL:
- Wissen → Versicherungen & Recht → Pferdehaftpflicht
- Wissen → Versicherungen & Recht → **Pferdekrankenversicherung**
- Wissen → Versicherungen & Recht → **Pferde-OP-Versicherung**

Für `Pferdekrankenversicherung` zunächst vorgesehene sinnvolle Artikelschienen:
- Beratung
- Vergleich
- Kosten
- Leistungen
- FAQ

ENTSCHEID:
- Pferdekrankenversicherung **nicht** unter Gesundheit einsortieren;
- Pferde-OP-Versicherung als eigenen Geschwisterpunkt vorsehen, nicht tief unter Krankenversicherung verstecken;
- Gesundheit bleibt fachlich Gesundheit und erhält keine Versicherungsprodukte.

BEGRÜNDUNG:
Versicherung ist Vertrags-/Tarif-/Leistungsthema. Gesundheit deckt Krankheiten, Vorsorge, Verletzungen und praktische Gesundheitsthemen ab. Die Trennung ist für Nutzerführung, SEO und Monetarisierung sauberer.

### 3. Reithalle

IST:
- kein eigenständiger Reithallenbereich vorhanden;
- Reitplatz liegt unter Weide.

SOLL:
- Stall → **Reithalle**
  - Reithallenbau
  - Reithallenboden
  - Hallenbeleuchtung
  - Beregnung / Bewässerung
  - Hallenklima / Belüftung
  - Bande & Spiegel

ENTSCHEID:
- Reithalle unter **Stall**, nicht unter Weide;
- Reitplatz bleibt unter Weide;
- Reithalleninhalte nur dort anlegen, wo sie hallenspezifisch sind;
- allgemeine Außenplatzthemen bleiben beim Reitplatz.

BEGRÜNDUNG:
Eine Reithalle ist eine bauliche Anlage und passt fachlich zum Infrastruktur-/Gebäudebereich Stall. Unter Weide wäre die Nutzerlogik falsch.

### 4. KISS-Bereinigung vor späterer Umsetzung

Vor Apply gezielt alle Bereichshubs auf **Ein-Kind-Hubs** wie `Wassertechnik` prüfen.

Regel:
- kein Bereichshub nur zur optischen Zwischenstufe;
- zusammenlegen, wenn kein eigener fachlicher/SEO-/Navigationsnutzen besteht;
- keine pauschale Verflachung: echte eigenständige Themenbereiche bleiben erhalten.

### 5. Spätere technische Umsetzung

Wenn der Nutzer die Umsetzung ausdrücklich wieder aufnimmt:

1. zentrale Soll-Struktur zuerst aktualisieren;
2. ALT → NEU-Dry-Run erzeugen;
3. bestehende IDs/Slugs/URLs soweit möglich erhalten;
4. WordPress-Taxonomie bleibt technisch flach, sofern kein separater ausdrücklicher Beschluss vorliegt;
5. nur notwendige technische Ableitungen aktualisieren: Portalstruktur/Affiliate-Struktur, PSTE-Kategorienmap, Template-/Breadcrumb-/Hub-Ableitungen, PPM nur für tatsächlich neue Produktionskategorien/Slots;
6. PSERC benötigt grundsätzlich keinen Kategorie-Hardcode; nach aktualisierter Struktur nur neuen Struktur-/Planlauf;
7. danach Kategorie-Gesamt-Dry-Run;
8. erst bei PASS genau ein Apply;
9. neuer Request + Readback;
10. erst danach wieder Produktionsfreigabe.

STATUS:
**VORGEMERKT / BESCHLOSSEN / NICHT UMGESETZT.**
