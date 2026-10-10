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

## 2026-10-10 – OP-Versicherung: fünf Artikelschienen (Nutzerauftrag, technische Übernahme ausstehend)

**Fachlicher Beschluss:** Bestehenden Hub `Wissen > Versicherungen & Recht > Pferde-OP-Versicherung` nicht verschieben. Unter dem Hub genau fünf eigenständige Artikelkategorien vorsehen, inklusive FAQ; Vergleich und Kosten werden wegen Überschneidung zusammengelegt. Pferdekrankenversicherung und alle sieben bestehenden Geschwisterkacheln unverändert lassen.

| Kachel | Vorgesehener Artikelkategorie-Slug | Thema |
| --- | --- | --- |
| Tarife & Kosten | `pferde-op-versicherung-tarife-und-kosten` | Preise, Tarifvergleich, Selbstbeteiligung |
| Leistungen & Bedingungen | `pferde-op-versicherung-leistungen` | Erstattung, Wartezeiten, Ausschlüsse, Nachbehandlung |
| OP-Arten & Kostenübernahme | `pferde-op-versicherung-op-arten` | Kolik-, Chip-, Zahn-, Kastrations- und Fraktur-OP; nur Versicherungsfragen |
| Beratung | `pferde-op-versicherung-beratung` | individuelle Wahl, Alter, Vorerkrankung, Wechsel, OP- vs. Krankenversicherung |
| FAQ | `pferde-op-versicherung-faq` | Schadenmeldung, Rechnungen, Unterlagen, Genehmigung und Meldefristen |

**Pflicht vor dem technischen Kategorie-Apply:**
1. Frischen WordPress-Kategorieexport/Readback vom aktuellen Bestand verwenden und `KATEGORIEN.tsv` als einzige zentrale Quelle fortschreiben. Im hier verfügbaren Branch hat die TSV weiterhin Blob-SHA `44684b554110560ffccab9ccf50b910a97259a06` und 1160 Zeilen mit Daten; sie enthält noch keine Krankenversicherung, OP-Versicherung oder Reithalle. Keine gesonderte kategorieführende Quelle anlegen.
2. Der Nutzer hat am 10.10.2026 installierte Versionen belegt: Template Kit **1.50.589**, Affiliate-Zentrale **6.72.212**, PSTE **0.57.68**, PSERC **0.28.34**, PPM **6.7.9**, Production Center **1.1.1**. Die installierten Originalquellen der neueren Versionen und deren aktuellen SHA sind in der technischen GitHub-Release-Current-Quelle nicht nachgewiesen. Niemals aus einer älteren Basis überschreiben.
3. Alle nachweislich betroffenen **bestehenden** Verbraucher einheitlich berücksichtigen: Affiliate Portalstruktur/Katalog, Template-Kit-Kacheln/Icons/Texte, PSTE-Kategorienbindung, PSERC-Dynamikrefresh, PPM-Kategorie-/Slotbindung und Production Center. Bei dynamischem Verbraucher ausschließlich Refresh/Readback, wenn keine statische Änderung nachgewiesen ist.
4. Kategorietexte in den bestehenden 150–200-Wörter-Regeln prüfen; Kurztexte maximal 18 Wörter. Keine neue Kachel-/Icon-Architektur. Bestehendes Exact-7-Raster der sieben Schwesterkacheln unverändert.
5. Vor Änderungen an Live: vollständiger Quellversions- und SHA-Abgleich, Altbestandserhalt, lokale positive/negative Regression, echter WordPress-Dry-Run `writes_performed=false`, dann genau ein autorisierter Apply und neuer Request mit Readback. Ohne diese Nachweise **kein Installer-Release, kein Live-Apply, kein PASS**.

**Aktueller Status:** FACHLICH BESCHLOSSEN / IN ZENTRALER ÄNDERUNGSAKTE ERFASST / TECHNISCHER APPLY GESPERRT, BIS AKTUELLER WORDPRESS-BESTAND UND INSTALLIERTE QUELLPAKETE EXAKT GEBUNDEN SIND.

