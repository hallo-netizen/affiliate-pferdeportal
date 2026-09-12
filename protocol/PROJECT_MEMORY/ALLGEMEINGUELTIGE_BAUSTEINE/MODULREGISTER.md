# ZENTRALES MODULREGISTER

STAND: 2026-09-12
ZWECK: Der Nutzer muss sich NICHT merken, welche Grundmodule existieren, wo sie liegen oder ob sie projektübergreifend nutzbar sind.

## Rolle

Das Modulregister ist kein zusätzliches Fachbüro und keine zweite technische Wahrheit.

Es ist der zentrale Karteikasten des Campus:
- Welche Module gibt es?
- Was ist ihr Hauptort?
- Sind sie allgemeingültig oder projektbezogen?
- Welcher Stand ist belegt?
- Welche Projekte nutzen sie?
- Welche Voraussetzungen gelten?

Die technische Wahrheit bleibt beim jeweiligen Modul.

## Pflichtprüfung

Das Modulregister wird automatisch geprüft bei:
- neuem Projekt;
- neuer Masterdatei;
- neuem Plugin/Modul;
- geplanter Wiederverwendung;
- Frage „haben wir dafür schon etwas?“.

Bei normaler Facharbeit ohne Modulbezug muss es nicht jedes Mal vollständig gelesen werden.

## Modulklassen

### ALLGEMEINGÜLTIG
Der Modul-Kern ist projektunabhängig.
Hauptort liegt unter `ALLGEMEINGUELTIGE_BAUSTEINE/`.

### PROJEKTBEZOGEN
Der Modul-Kern ist bewusst nur für ein bestimmtes Projekt bestimmt.
Hauptort liegt im jeweiligen Projektgebäude.

### UNGEKLÄRT
Die Modulklasse ist noch nicht belastbar geklärt.
Default bei Unsicherheit.
Nicht automatisch verschieben oder wiederverwenden.

## Wichtig: GEMISCHT ist KEINE Modulklasse

„Gemischt“ beschreibt eine Datei/Masterakte, die z. B.:
- allgemeinen Plugin-Code
- plus projektspezifische Konfiguration
- plus Projekthistorie

enthält.

Dann wird die Masterakte im Büro inventarisiert und in Bestandteile zerlegt.
Der allgemeine Modul-Kern kann trotzdem eindeutig ALLGEMEINGÜLTIG sein.

## Pflichtfelder je Modul

- MOD-ID
- NAME
- MODULKLASSE
- STATUS / Prüfgrad
- HAUPTORT
- AKTUELL BELEGTER STAND
- ZWECK
- ABHÄNGIGKEITEN
- NUTZENDE PROJEKTE
- AUTORITATIVE QUELLE / BELEG
- OFFENE PUNKTE

## MOD-001 – KATEGORIENMODELL

MODULKLASSE: ALLGEMEINGÜLTIG
STATUS: Master R10/R9 + WordPress-Plugin V1.8.0 hart inventarisiert; lokaler/fresh Prüfstand PASS; Live-WordPress-Deployment noch nicht PASS
HAUPTORT: `ALLGEMEINGUELTIGE_BAUSTEINE/KATEGORIENMODELL/`
AKTUELL BELEGTER STAND:
- Master 016 R10/R9 Runtime Deployment
- Plugin V1.8.0
ZWECK:
evidenzbasierte, allgemeingültige Kategorie-/Strukturentwicklung für Content, HivePress/Marketplace und explizit gebundene Journal-Taxonomien
ABHÄNGIGKEITEN:
- WordPress >= 6.4
- PHP >= 8.1
- DataForSEO für gebundene Research-Schritte
- HivePress nur wenn Marketplace-Säule genutzt wird
NUTZENDE PROJEKTE:
- historischer Real-/Pilotbeleg Gaumen Atelier im Master; keine fachliche Vererbung
- konkrete neue Projektnutzungen bei Einsatz eintragen
AUTORITATIVE QUELLE:
`ALLGEMEINGUELTIGE_BAUSTEINE/KATEGORIENMODELL/CURRENT_STATE.md`
ARCHIV:
`/Campus-Archiv/ALLGEMEINGUELTIGE_BAUSTEINE/KATEGORIENMODELL/2026-09-05/`
OFFEN:
echter Live-WordPress-Deploymentlauf auf Zielinstallation

## MOD-002 – BILDZENTRALE

MODULKLASSE: ALLGEMEINGÜLTIG
STATUS: allgemeingültiger Modul-Kern; aktueller 2.6.9-Installer + Nullpunkt 069 als Dateien vorhanden; beide Installer byte-identisch; Pferde-LIVE-Version 2.6.9 separat belegt
HAUPTORT: `ALLGEMEINGUELTIGE_BAUSTEINE/BILDZENTRALE/`
AKTUELL BELEGTER LIVE-STAND: 2.6.9 im Pferde-Atelier
ZWECK:
- Beiträge
- WordPress-Taxonomien
- optionale HivePress-Taxonomien
- Pixabay
- Pexels
- Magnific
- sichere Profile
- Export/Import
- Readback-Fallback
ABHÄNGIGKEITEN: WordPress; optionale HivePress-Nutzung; Providerzugänge
NUTZENDE PROJEKTE:
- PFERDE_ATELIER → `PROJEKTE/PFERDE_ATELIER/BILD/`
BELEG:
- allgemeiner Installer 2.6.9
- Nullpunkt 069
- Byte-Identität beider 2.6.9-Installer
- bestehende Nutzerbestätigung LIVE 2.6.9 im Pferde-Atelier
- Pferde Master 049 / historischer 2.4.9-Codebeleg
- 2.6.6-Konfigurationsbeleg
OFFEN:
- keine Fachprüfung in diesem Sortierschritt.

## Projektanwendung

Ein Projekt, das ein allgemeingültiges Modul nutzt, speichert NICHT den Modul-Kern ein zweites Mal als Hauptwahrheit.

Im Projekt bleiben nur:
- Verweis auf MOD-ID/Hauptort;
- projektspezifische Konfiguration;
- Projektdaten;
- projektspezifische Historie;
- projektspezifische Fehler und Tests.

## Automatische Klassifizierung neuer Eingänge

1. Masterdatei vollständig inventarisieren.
2. Bestandteile trennen: Code / Konfiguration / Daten / Historie / Tests / Protokolle.
3. Modul-Kern identifizieren.
4. Bei Unsicherheit zunächst MODULKLASSE = UNGEKLÄRT.
5. Auf harte Projektverdrahtung und Konfigurierbarkeit prüfen.
6. Modulklasse festlegen.
7. Genau einen Hauptort festlegen.
8. Projektanwendungen nur verweisen.
9. Modulregister aktualisieren.

Der Nutzer muss diese Einordnung weder erinnern noch manuell vorgeben.


## MOD-003 – UNIVERSAL PORTAL DESIGN SUITE

MODULKLASSE: ALLGEMEINGÜLTIG
STATUS: V2.2.40 / Contract V104 hart inventarisiert; spätere GitHub-Pferdehistorie bestätigt ausdrücklich „kein Universal-Update erforderlich“
HAUPTORT:
`ALLGEMEINGUELTIGE_BAUSTEINE/DESIGN/`
AKTUELL BELEGTER STAND:
- Plugin 2.2.40
- Designvertrag V104
ABHÄNGIGKEITEN:
- WordPress >= 6.0
- PHP >= 7.4
- HivePress-Funktionen nur bei entsprechender Nutzung
NUTZENDE PROJEKTE:
- PFERDE_ATELIER → eigene Projektlinie unter `PROJEKTE/PFERDE_ATELIER/DESIGN/`
BELEG:
- übergebener Universal Plugin/Master
- GitHub `UNIVERSAL_STATUS.md` auf Commit `f1e074b...`
ARCHIV:
`/Campus-Archiv/ALLGEMEINGUELTIGE_BAUSTEINE/DESIGN/2026-09-05/`

## MOD-004 – HIVEPRESS-ANZEIGENSUCHE

MODULKLASSE: UNGEKLÄRT

STATUS:
als separater Plugin-/Source-Baustein in Universal- und Pferde-Designmaster erkannt; eigener Audit noch offen.

HAUPTORT:
bis zur Modulklassifizierung ausschließlich dieser MOD-004-Registereintrag plus die unten genannten Belegquellen.
Kein eigener freigegebener Modulraum.

AKTUELL BELEGTER STAND:
v2.1.5 als Universal- und Pferde-Artefakt in den Designmastern.

ZWECK:
separater HivePress-Anzeigensuche-Baustein; weitergehende Modulfreigabe UNGEKLÄRT.

ABHÄNGIGKEITEN:
UNGEKLÄRT bis separatem Audit.

NUTZENDE PROJEKTE:
PFERDE_ATELIER als belegter Projektkontext.

AUTORITATIVE QUELLEN / BELEGE:
- `ALLGEMEINGUELTIGE_BAUSTEINE/DESIGN/MASTERDATEIEN_INVENTAR.md`
- `PROJEKTE/PFERDE_ATELIER/DESIGN/MASTERDATEIEN_INVENTAR.md`
- Universal: `UNIVERSAL_HIVEPRESS_ANZEIGENSUCHE_v2.1.5_AJAX_ANZEIGENKATEGORIEN_INSTALLIEREN.zip`
- Pferde: `PFERDE_ATELIER_HIVEPRESS_ANZEIGENSUCHE_v2.1.5_AJAX_ANZEIGENKATEGORIEN_INSTALLIEREN.zip`

OFFENE PUNKTE:
separater Modul-Audit.

REGEL:
Nicht im Designmaster verlieren; keine Allgemeingültigkeit behaupten.


## MOD-005 – UNIVERSAL RESEARCH & FILL

MODULKLASSE: ALLGEMEINGÜLTIG
STATUS: aktueller Plugin-/Master-Dateibeleg 1.9.9; externer Plugin-ZIP und im Master eingebetteter CURRENT_PLUGIN-ZIP byte-identisch.
HAUPTORT: `ALLGEMEINGUELTIGE_BAUSTEINE/UNIVERSAL_RESEARCH_FILL/`
AKTUELL BELEGTER STAND:
- Plugin 1.9.9
- Master 1.9.9
HISTORISCH:
- Plugin 1.9.5
- Master 1.9.5
NUTZENDES PROJEKT:
- PFERDE_ATELIER → `PROJEKTE/PFERDE_ATELIER/HIVEPRESS/`
PROJEKTBEZUG:
`config/pferde-atelier.php`
GITHUB-ABGLEICH:
auf aktuellem `main` kein eigener URF-Dateistand unter den entsprechenden Namen/Pfaden gefunden.
ARCHIV:
`/Campus-Archiv/ALLGEMEINGUELTIGE_BAUSTEINE/UNIVERSAL_RESEARCH_FILL/`


## MOD-006 – PRODUKTVERGLEICHS-ENGINE

MODULKLASSE: UNGEKLÄRT

STATUS:
V1-ARCHITEKTUR ENTSCHIEDEN / isolierter Vergleichskern vorhanden / WordPress+MySQL Produkt-/Variantenregeln PASS / reales PV-REG-001-Dossier PASS / Writer und Live-Ausgabe noch offen. Allgemeingültigkeit ist Ziel, technisch noch nicht vollständig bewiesen.

GEPLANTER HAUPTORT:
nach Prototypprüfung unter `ALLGEMEINGUELTIGE_BAUSTEINE/`; bis dahin keine künstliche zweite Modulwahrheit anlegen.

ZWECK:
Projektunabhängige Engine für:
- Definition vergleichbarer Produkte/Varianten;
- Vergleichstyp und Vergleichsebene;
- produktgruppenabhängige Vergleichsmerkmale;
- priorisierte Hersteller-/Primärquellen-Recherche;
- strukturierte Herstellerfakten;
- NOT_IN_SOURCE / SOURCE_CONFLICT / CONFIGURATION_DEPENDENT;
- neutrale Eignungsableitung nach dokumentierten Eigenschaften;
- strukturiertes Faktendossier als Übergabe an ein Text-/Publishing-System.

GEPLANTE GRENZE:
Kein Klon eines kompletten bestehenden Produktions-/Workflow-Stacks.
V1 besitzt eine eigene kleine Produktvergleichsstraße bis WordPress-DRAFT und keine Laufzeitabhängigkeit von STARTMASTER/TEXT.
Produktfakten kommen aus MOD-007 UNIVERSAL PRODUKTWISSEN.
SEO liefert optional Signale; aktuelle Kaufquellen/Preise/Verfügbarkeit bleiben bei der bestehenden Affiliate-Zentrale über eindeutige Produktidentitäten.

ERSTE PROJEKTANWENDUNG:
PFERDE_ATELIER → `PROJEKTE/PFERDE_ATELIER/PRODUKTVERGLEICH/`

PROJEKTKONFIGURATION:
Pferde-spezifische Kategorien, Produktgruppen, Merkmalskataloge und Quellenprofile müssen außerhalb des Kerncodes liegen.

BELEG:
Nutzerunterlagen vom 2026-09-06, insbesondere das 68-Dossier-Übergabepaket mit getrennten Produktionsaufträgen, Kernfakten, Herstellerquellen, Konfliktliste und Produktionsvertrag.

BRÜCKENKANDIDAT:
`hobbyroom/productwissen-affiliate-exact-bridge-20260907`
→ read-only Productvergleich/Productwissen → Affiliate Exact-Product-Requirements; isoliert, noch nicht in den offiziellen Produktvergleich-Prototyp integriert.

OFFEN:
- Product-Compare-Writer und Entscheidungsinterpretation;
- WordPress-DRAFT-Ausgabe;
- Vergleichsarchiv/Frontend;
- Prüfung/Übernahme + WordPress/E2E der Exact-Product-Brücke zur vorhandenen Affiliate-Zentrale;
- optionale SEO-Priorisierung ohne Pflichtkopplung;
- Recherche-/Aktualisierungsadapter;
- technischer Allgemeingültigkeitstest mit zweiter Projektkonfiguration.


## MOD-007 – UNIVERSAL PRODUKTWISSEN

MODULKLASSE: UNGEKLÄRT

STATUS:
V1-DATENVERTRAG DEFINIERT / isolierter Prototyp vorhanden / lokaler Vertrags-/Logiktest PASS / echter WordPress+MySQL-Smoke-Test PASS (`UPK_WORDPRESS_DB_GESAMT_PASS`, Run 34108014923). Kein Live-Portal-Deployment behauptet.

GEPLANTER HAUPTORT:
nach Prototypprüfung unter `ALLGEMEINGUELTIGE_BAUSTEINE/`.

ZWECK:
Eine einzige projektunabhängige interne Produktfaktenbasis für Produktvergleich, Variantenvergleich, Beratung und Affiliate-Exact-Match.

V1-KERN:
- Produktidentität;
- Varianten;
- Identifier;
- Hersteller-/Primärquellenfakten;
- Quellenstatus;
- Lebenszyklus/Aktualität.

NICHT ZUSTÄNDIG:
- Artikelproduktion;
- SEO-Priorisierung;
- Preise/Kaufangebote;
- öffentliche WordPress-Kategorien.

ERSTE PROJEKTANWENDUNG:
PFERDE_ATELIER.

AKTUELLER VERTRAG:
`PROJEKTE/PFERDE_ATELIER/PRODUKTVERGLEICH/PRODUKTWISSEN_V1_VERTRAG.md`.

OFFEN:
Allgemeingültigkeitsbeweis mit mindestens einer zweiten Projektkonfiguration sowie spätere produktive Release-/Liveprüfung.

## MOD-008 – UNIVERSAL GLOSSAR ENGINE

MODULKLASSE: UNGEKLÄRT / ZIEL ALLGEMEINGÜLTIG

STATUS:
V1-DATENVERTRAG DEFINIERT / isolierter 0.1.0-Prototyp vorhanden / PHP-Lint 8/8 PASS / statische Positiv-Negativprüfung 15/15 PASS / Runtime-Stub mit Pferde- und fachfremder Zweitkonfiguration PASS / echter WordPress-Smoke-Test noch offen.

HAUPTORT:
`ALLGEMEINGUELTIGE_BAUSTEINE/GLOSSAR/`

AKTUELL BELEGTER STAND:
- Prototype 0.1.0;
- Source-Manifest `SOURCE_SHA256.txt`;
- lokaler ZIP SHA-256 `c8f58f0b144d286567a269d3fc26f09db36cb94446619528ff8b896d6b8682ee`.

ZWECK:
Projektunabhängiger WordPress-Glossarkern mit eigenem Backendbereich, Begriffsdaten, Oberbereichen, eigenen Zieladressen, SEO-Feldern, Suche/A–Z/Aufklapper sowie strukturiertem JSON-Import/Export.

ABHÄNGIGKEITEN:
- WordPress >= 6.4;
- PHP >= 8.1;
- Yoast optional, keine Pflichtabhängigkeit.

NUTZENDE PROJEKTE:
- PFERDE_ATELIER → `PROJEKTE/PFERDE_ATELIER/GLOSSAR/` als erste Anwendung.

AUTORITATIVE QUELLE / BELEG:
- `ALLGEMEINGUELTIGE_BAUSTEINE/GLOSSAR/CURRENT_STATE.md`;
- `ALLGEMEINGUELTIGE_BAUSTEINE/GLOSSAR/PROTOTYPE_QA_0.1.0.md`.

OFFEN:
- echter WordPress-Install-/Upgrade- und Permalinktest;
- echter Yoast-/Astra-Test;
- realer Wissensdatenbankimport;
- größerer Bestands-/Performance-Test;
- zweites echtes WordPress-Portal vor Hochstufung auf ALLGEMEINGÜLTIG.
