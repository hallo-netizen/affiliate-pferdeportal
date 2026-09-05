# BAUCONTAINER – ENTWICKLUNGSPROTOKOLL

STAND: 2026-09-05
STATUS: AKTIV

## 1-KLICK-ÜBERSICHT

**WAS IST DAS?**  
Das Gedächtnis unseres konzeptionellen Austauschs über den Campus.

**HIER BIST DU RICHTIG, WENN …**  
du verstehen willst, wie eine Architekturidee entstanden ist, welche Alternativen diskutiert wurden oder welche offenen Gedanken noch nicht zu einer festen Regel geworden sind.

**DU DARFST …**  
Ideen, Einwände, Korrekturen, verworfene Varianten und offene Architekturfragen dokumentieren.

**DU DARFST NICHT …**  
dieses Protokoll als aktuelle Hauptwahrheit behandeln oder damit BAUPLAN/AENDERUNGSREGISTER ersetzen.

**ALS NÄCHSTES …**  
für aktuelle Architektur → `BAUPLAN.md`; für tatsächlich gebaute Änderungen → `BAUPROTOKOLL.md`; für dauerhaft gültige Entscheidungen/WHY → `AENDERUNGSREGISTER.md`.

## Harte Regel

Substanzieller Architektur-Austausch darf nicht nur im Chat verschwinden.

Wenn ein Gespräch eine relevante:
- Idee,
- Nutzerkorrektur,
- verworfene Variante,
- offene Architekturfrage,
- neue Metapher/Arbeitsregel

hervorbringt, wird sie hier kurz festgehalten.

Nicht als Wort-für-Wort-Chatkopie, sondern als vollständiger sachlicher Entscheidungs-/Gedankenverlauf.

## Bisheriger Entwicklungsverlauf

### 2026-09-05 – Ausgangsproblem

Wiederkehrendes Problem:
Chats raten oder erfinden Ersatzwege, obwohl verbindliche Prozesse bereits existieren.

Daraus entstanden:
- Hauptpförtner als Reset;
- Handlungsverzeichnis;
- Pflicht-Readback;
- STOPP bei Unklarheit.

### 2026-09-05 – Bürogebäude-Metapher

Entwicklung:
- Projektorganisation als Gebäude;
- Fachbereiche als Büros;
- genau ein Hobbyraum je Büro;
- bestehender Maschinenraum bleibt technische Originalinfrastruktur.

Korrektur:
Keine neue Parallelarchitektur nur für die Metapher.

### 2026-09-05 – Campus statt nur ein Gebäude

Nutzerfrage:
Wie wird ein wirklich neues unabhängiges Projekt eingeordnet?

Entscheidung:
- eigenständiges Projekt = neues Projektgebäude;
- Campus-Hauptpförtner routet zuerst zum Projekt, dann zum Büro;
- Struktur bleibt organisch und umbaubar.

### 2026-09-05 – Paul

Entwicklung:
Paul erhält vollständigen Projektstand auf eigenem isolierten Branch.

Wichtige Nutzerkorrektur:
Fehlerregister und Änderungs-/Erklärungsregister sind für Paul Pflichtlektüre.

Entscheidung:
Paul darf frei lesen/testen/ändern auf seinem Branch, aber nicht selbst in offizielle Fachstände übernehmen.

### 2026-09-05 – BILD

Nutzer lieferte Masterakten und bestätigte:
LIVE-Version Bildzentrale = 2.6.9.

Erkenntnis:
- allgemeiner Bildzentrale-Kern ist allgemeingültig;
- Pferde-Atelier-Masterakten enthalten zugleich projektspezifische Konfiguration, Produktionsdaten und Historie;
- Masterakte und Modulklasse müssen getrennt werden.

### 2026-09-05 – Vollständige Masterdatei-Verwertung

Nutzerregel:
Nichts aus Masterdateien darf verloren gehen.

Entscheidung:
Jeder Bestandteil wird inventarisiert und zugeordnet:
Code, Daten, Historie, Fehler, Tests, Protokolle, Dubletten, UNGEKLÄRT.

Secrets werden nicht öffentlich kopiert, ihre Existenz/Funktion bleibt dokumentiert.

### 2026-09-05 – Allgemeingültige Module

Nutzer bestätigt:
Kategoriemodell ist allgemeingültig.

Entwicklung:
- Gebäude ALLGEMEINGÜLTIGE BAUSTEINE;
- zentrales MODULREGISTER;
- Nutzer muss nicht erinnern, was wiederverwendbar ist;
- neue Projekte prüfen zuerst vorhandene Module.

Korrektur:
„GEMISCHT“ ist keine Modulklasse.
Ein Modul ist ALLGEMEINGÜLTIG / PROJEKTBEZOGEN / UNGEKLÄRT.
Gemischt kann nur eine Masterakte sein.

### 2026-09-05 – Zielverträge

Nutzerbedarf:
Fester Ort für Zielverträge.

Entscheidung:
zentraler Zielvertragsraum mit Register.
Alte Fassungen bleiben erhalten; keine stillen Zieländerungen.

### 2026-09-05 – Archiv

Nutzerfrage:
Muss er selbst sortieren/hochladen?

Entscheidung:
Der bearbeitende Chat ordnet zu.
Nur lokale, noch nicht zugängliche Dateien müssen einmal bereitgestellt werden.
Historisch bedeutet nicht löschbar.

### 2026-09-05 – Zugriffsschutz

Nutzerfrage:
Gesamten Campus per Kennwort schützen?

Aktuelle Empfehlung:
kein Datei-Passwortsystem.
Stattdessen nach V1-Freigabe eigener privater Campus-Repository.

STATUS:
noch offene Architekturentscheidung.

### 2026-09-05 – Architektur darf selbst lernen

Nutzerregel:
Jeder Chat darf bei realem Optimierungsbedarf die Architektur verbessern.

Entscheidung:
kein spezieller Architekten-Chat nötig.
Architekturänderung nur in Baucontainer-Rolle + KISS + Bauprotokoll + WHY + Architektur-Fehlerkiste.

### 2026-09-05 – Hausmeister

Nutzeridee:
regelmäßig Ballast aus produktiven Räumen ins Archiv verteilen.

Entwicklung:
Hausmeister als Wartungsprozess.

Wichtige spätere Korrektur:
Hausmeister darf **keine Inhalte ändern**.
Nur unverändert ordnen/verschieben/verweisen/protokollieren.

### 2026-09-05 – Pförtner/Hausmeister reine Verwaltung

Nutzer-Hard-Rule:
Pförtner und Hausmeister müssen die Finger von Inhalten lassen.

Entscheidung:
- Pförtner = READ/ROUTE ONLY;
- Hausmeister = ORDNEN/VERSCHIEBEN OHNE INHALTSÄNDERUNG;
- Rolle bestimmt Rechte;
- für Architekturarbeit muss Chat ausdrücklich in Baucontainer-Rolle wechseln.

### 2026-09-05 – Ein Klick = alles klar

Nutzerregel:
Am Campus-, Gebäude-, Büro- und Paul-Eingang muss sofort verständlich sein:
- was ist das;
- wozu ist es da;
- was darf ich;
- was darf ich nicht;
- wo geht es weiter.

Entscheidung:
verbindlicher `EINGANGSSTANDARD.md`.

### 2026-09-05 – WordPress-Raum oder Register?

Nutzeridee:
Zentraler Ort für WordPress-Plugins bzw. Verweise darauf.

Kritische Prüfung:
Ein eigenes WordPress-Büro wäre aktuell zusätzliche Architektur ohne eigene Facharbeit.

Entscheidung:
- kein neues Büro/Gebäude;
- ein campusweites `WORDPRESS_REGISTER.md`;
- nur Plugin-/Installer-Navigation;
- keine zweite Modul-, LIVE- oder Release-Wahrheit.

Zusätzliche Bestandsaufnahme:
Bereits übergebene direkte Plugin-/Installer-Artefakte werden dort aufgenommen; große Masterpakete erst nach Inhaltsprüfung als Plugin klassifiziert.

## Offene Punkte

- Campus nach V1-Freigabe in eigenes privates Repository verschieben?
- exakter großer Hausmeister-Rhythmus erst nach realer Nutzung festlegen;
- weitere Masterdateien vollständig einordnen;
- Kategoriemodul-Code/Masterakten nach Übergabe inventarisieren;
- BILD 2.6.9-Code nach Übergabe byte-/portabilitätsprüfen;
- TEXT-Endstand erst nach Abschluss des parallelen Chats frisch synchronisieren.

## Grundsatz

Dieses Protokoll bewahrt den **Gedankenweg**.

Aktuelle Wahrheit wird immer aus den dafür vorgesehenen Hauptakten gelesen.
