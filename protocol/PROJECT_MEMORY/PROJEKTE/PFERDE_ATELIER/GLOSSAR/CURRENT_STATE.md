# BÜRO GLOSSAR – CURRENT_STATE

STAND: 2026-09-13
STATUS: 0.2.6 TECHNISCHER KANDIDAT HARDTEST PASS / PFERDE-LIVE-READBACK OFFEN

## Belastbarer aktueller Stand

- Eigenes Büro `GLOSSAR` ist die Projekt-Steuerstelle für das öffentliche Pferde-Atelier-Glossar.
- Fachliche Glossar-Datenbank bleibt autoritativ in `../WISSENSDATENBANK/AKTENSCHRAENKE/GLOSSAR/`.
- Keine zweite Fachbegriffs-Datenbank im Büro GLOSSAR.
- Vorhandene WordPress-Seite `Glossar` bleibt Hauptseite.
- Keine normalen WordPress-Seiten oder Beiträge pro Glossarbegriff.
- Das bestehende Pferde-Designplugin bleibt unangetastet.
- Technischer Kern ist `MOD-008 – Universal Glossar Engine` unter `../../../ALLGEMEINGUELTIGE_BAUSTEINE/GLOSSAR/`.

## Aktueller Kandidat

Version:
`Universal Glossary Engine 0.2.6`

Rewrite-Schema:
`5`

Arbeitsbranch:
`hobbyroom/glossar-026-upgrade-hardtest-20260913`

Technisch getesteter Commit:
`e5f8c8ce1839a69f3e6fb712bd4a3d4a3e8ad059`

Autoritativer Hardtest:
Run `34748541630`.

Innerer Plugin-ZIP SHA-256:
`e0717db3aa247edc30b0fe84a261aa59037050d593e3432a6fb460f6d96f3b09`.

Actions-Artefakt-ID:
`10314822840`.

## Harte Positiv-/Negativprüfung

### Fresh-Install

Job `103700782149` → PASS.

Belegt unter echtem WordPress + MySQL + Astra:
- Version 0.2.6 und Rewrite-Schema 5;
- Glossarstartseite und Navigation;
- A–Z;
- Kartenlinks;
- AJAX positiv und ungültiger Nonce negativ;
- Draft nicht öffentlich;
- unbekannter Begriff 404;
- Preview;
- Duplikatsperre;
- Kategorie-/Begriffskollision;
- normaler WordPress-Beitrag unverändert;
- Einzelbegriff muss echtes Glossar-Artikelmarkup + H1 enthalten, nicht nur HTTP 200;
- Hero-Abstand-Regel;
- responsive Hero-Darstellung;
- Breadcrumb-Achse/Darstellung.

### Echter WordPress-Updateweg 0.2.5 → 0.2.6

Job `103700782306` → PASS.

Negativer Vorzustand wurde absichtlich und nachweisbar erzeugt:
- aktives 0.2.5;
- bekannte Einzelbegriffroute zunächst funktionsfähig;
- Einzelbegriff-Rewrite-Regel entfernt;
- bekannte URL danach 404;
- Schema bleibt 4.

Danach:
- WordPress-Plugin-Updater überschreibt 0.2.5 mit 0.2.6;
- installierte Dateien zeigen Version 0.2.6 / Schema 5;
- DB vor erstem neuen Request = Schema 4;
- erster neuer Webrequest migriert 4 → 5;
- Einzelbegriff-Regel wird wieder aufgebaut;
- bekannte Begriffseite wieder 200 + echtes Glossar-Artikelmarkup + erwarteter Inhalt.

Anschließend komplette Positiv-/Negativ- und Regressionsmatrix erneut PASS.

### Gated Package + lokaler Artefaktcheck

Paketjob `103700913568` → PASS und durfte erst nach beiden grünen Jobs laufen.

Das tatsächlich erzeugte Actions-Artefakt wurde anschließend lokal erneut geprüft:
- äußerer und innerer Hash stimmen;
- ZIP-Struktur positiv/negativ PASS;
- keine Path-Traversal-/Symlink-Einträge;
- 0.2.5↔0.2.6-Dateivergleich exakt nur zwei erlaubte Dateien geändert;
- alte Version/Schema und alte CSS-Hacks negativ nicht enthalten;
- PHP-Lint aller 10 PHP-Dateien PASS.

Technisches Protokoll:
`../../../ALLGEMEINGUELTIGE_BAUSTEINE/GLOSSAR/TESTPROTOKOLL_0.2.6_20260913.md`

## Die vier aktuell gemeldeten Pferde-Frontendfehler

Autoritative Fehlerquelle:
`FEHLERQUELLEN.md`

1. Hero-Abstand zu groß → 0.2.6-Kandidat technisch PASS / Live-Sichtprüfung offen.
2. Hero-Bild nicht responsive → 0.2.6-Kandidat technisch PASS / Live-Sichtprüfung offen.
3. Einzelbegriff-Links/weiße Seiten → Fehlerklasse mit defekter Rewrite-Regel hart reproduziert und Update-Reparatur bewiesen; exakte Live-Rootcause weiterhin nicht behauptet; Live-Readback offen.
4. Kategorie-Breadcrumb falsch → 0.2.6-Kandidat technisch PASS / Live-Sichtprüfung offen.

## Designbindung

Vollständiger Pferde-Designstand 1.50.469 wurde auf die Glossar-relevanten Punkte geprüft:
- fremde Taxonomie wird nicht als normale Portal-Kategorie übernommen;
- kein zweiter Design-Breadcrumb für `uge_group`;
- 900px-Breadcrumb-/Content-Achse vorhanden.

Der dokumentierte Live-Stand 1.50.472 verändert gegenüber 1.50.469 laut Design-Master weder CSS noch Breadcrumb, Bild, Karten oder Publish-Verhalten.

Kein Umbau des Designplugins.

## Dauerhafte Update-Regel

Keine materiell unterschiedlichen Pluginpakete mehr unter derselben Versionsnummer.

0.2.6 ist deshalb eine echte neue Version mit Rewrite-Schema 5.

Quelle:
`../../../ALLGEMEINGUELTIGE_BAUSTEINE/GLOSSAR/ENTSCHEIDUNG_20260912.md`

## Noch NICHT bewiesen

- reale Installation dieses exakt hashgebundenen 0.2.6-ZIPs im Pferde Atelier;
- realer Sicht-/Funktionsreadback der vier gemeldeten Frontendpunkte;
- exakte Ursache der bisher beobachteten weißen Live-Seite;
- aktueller Astra+Yoast-Kombinationstest, soweit für endgültigen Release erforderlich;
- realer Campus-Wissensdatenbankimport;
- Performance mit größerem echten Begriffsbestand;
- separates zweites reales Portal.

Daher: technischer Kandidat PASS, aber **kein Pferde-LIVE-PASS**.

## Nächster belastbarer Schritt

Ausschließlich `HOBBYRAUM.md` folgen: exakt hashgebundenen 0.2.6-Kandidaten über den geprüften WordPress-Updateweg installieren und danach die vier gemeldeten Punkte plus negative Regressionen real zurücklesen.
