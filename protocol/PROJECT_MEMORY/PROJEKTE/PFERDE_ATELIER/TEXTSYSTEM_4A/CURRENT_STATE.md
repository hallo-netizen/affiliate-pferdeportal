# TEXTSYSTEM 4A – CURRENT STATE

STAND: 2026-09-13
STATUS: AKTIV / PROTOTYP NICHT PRODUKTIONSFREIGEGEBEN

## Gesicherter Ausgangsbefund

- System 4 läuft isoliert in PR #238, Branch `hobbyroom/system4-true-single-room-v1`, aktueller geprüfter Head bei Büroanlage: `77c02a9df1745a28157fcc27f65f74e9c4fb1153`.
- System 4 ist aktuell BLOCKED, weil der vollständige aktuelle Unittest-/E2E-Beweis auf genau diesem Head noch fehlt.
- Der aktuelle System-4-Einzelartikelkern ist bereits deutlich verbessert: kanonischer Zustand, feste Phasen, Same-Article-Repair, interne Content-/Designprüfungen und ein zentraler Fullcheck.
- Deshalb ist 4a **keine neue Textmaschine** und kein Ersatz der vorhandenen Qualitätslogik.

## Entscheidungsmaßstab 4 vs. 4a

Die aktuell noch vorhandene feste 7er- bzw. `Beratung`-Bindung in System 4 wird als **behebbarer Implementierungsfehler** behandelt und ist ausdrücklich **kein Entscheidungskriterium für 4a**.

4a muss gegen ein entsprechend bereinigtes Konzept 4 bestehen. Entscheidend sind ausschließlich:
1. Zahl echter Laufzeit-/Zustandsautoritäten und Übergabegrenzen;
2. Schutz vor externer Workflow-Freiheit;
3. unveränderte Fach-, Design- und Qualitätsautorität;
4. vollständiger Weg vom Produktionsanstoß bis zur korrekten WordPress-Datei im Elternchat;
5. Offenheit für neue autoritativ definierte Beitragsarten ohne neue Controllerlogik;
6. Automatisierbarkeit und robuste Same-Article-Reparatur.

## Separat zu reparierende System-4-Punkte

- feste Artikelzahl im aktuellen Handoff entfernen;
- feste `Beratung`-Bindung im Handoff entfernen;
- Signing-/Direct-Import-Endpfad eindeutig machen.

Diese Punkte werden **nicht** als Vorteil von 4a gewertet.

## Unverändert / unangetastet

- bestehende Textmaschine und Fachregeln;
- PPM 6.7.9;
- LanguageTool 6.8 / Bestand 43;
- PSERC/PSTE/SEO-/Link-/Tabellen-/Metadatenregeln;
- Design, Theme/CSS, WordPress-Plugin;
- offizieller STARTMASTER/CURRENT_STATE;
- System 4 / PR #238;
- `publish_allowed=false`.

## 4a-Status

Büro angelegt. Architekturprüfung läuft gegen **bereinigtes Konzept 4**, nicht gegen dessen aktuelle Stückzahl-/Artikeltyp-Hardcodes.

Noch NICHT bewiesen:
- dass 4a tatsächlich weniger echte Übergaben/Zustandsautoritäten besitzt als bereinigtes Konzept 4;
- realer vollständiger Validatoranschluss;
- echter positiver End-to-End-Lauf;
- 1/3/25/1000;
- mehrere reale Beitragsarten;
- direkte WordPress-Importprüfung gegen den aktuell installierten Importer.

Kein PASS darf daraus abgeleitet werden.
