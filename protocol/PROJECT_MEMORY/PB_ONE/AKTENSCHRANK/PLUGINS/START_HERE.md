# PB ONE – AKTENSCHRANK – SELBSTENTWICKELTE PLUGINS

STAND: 2026-09-12
ROLLE: AGENTUR-/IP-KATALOG + ZENTRALES PLUGIN-UPDATE-KONTROLLPULT

## Zweck

Hier findet PB ONE bestätigte selbstentwickelte Plugins/digitale Eigenentwicklungen und genau einen zentralen historischen Vorgang je tatsächlicher Pluginentwicklung/-aktualisierung.

Das Fach beantwortet:
- Was haben wir selbst entwickelt?
- Wofür ist es gedacht?
- Ist es allgemeingültig oder projektbezogen?
- Wo liegt die technische Hauptquelle?
- Welche tatsächlichen Pluginänderungen/-updates wurden durchgeführt?

## Harte Grenze

**Keine zweite technische Wahrheit.**

Hier werden NICHT eigenständig als aktuelle Fachwahrheit gepflegt:
- aktuelle LIVE-/Releasefreigabe;
- Code;
- technische Fehlerdetails;
- technische Modulklasse;
- dynamischer Branch-Head/NEXT ACTION.

Dafür immer zur autoritativen Quelle:
- `WORDPRESS_REGISTER.md` als Technologieindex;
- `ALLGEMEINGUELTIGE_BAUSTEINE/MODULREGISTER.md` für Modulklasse;
- zuständiges Projekt-/Fachbüro;
- technische Releasequelle.

## Dateien

- `REGISTER.md` → geschäftlicher/IP-Index bestätigter Eigenentwicklungen.
- `UPDATEPROTOKOLL.md` → genau ein zentraler historischer Vorgang je tatsächlicher Pluginentwicklung/-aktualisierung; verweist für Fach-/Release-/LIVE-Wahrheit zurück zur autoritativen Fachquelle.

## Aufnahme

Nur als PB-ONE-Eigenentwicklung aufnehmen, wenn dieser Status belegt oder ausdrücklich bestätigt ist.

Bei Unsicherheit:
**UNGEKLÄRT – nicht aufnehmen.**

## Campusweite Plugin-Hard-Rules

1. **Versionsbasis vor Kandidatenwahl prüfen:** Vor jeder neuen Eigenplugin-Kandidatenversion zuerst den jüngsten vollständig geprüften Stand im zuständigen Plugin-/Fachbestand bestimmen. Keine ältere Linie mit niedrigerer Versionsnummer fortführen, wenn ein neuerer geprüfter Stand existiert. Fachänderungen auf den jüngsten geprüften Stand integrieren und beide Seiten regressieren.
2. **Installierbares Artefakt nur aus kanonischer Source:** Unmittelbar vor Übergabe/Installation das Plugin aus der aktuellen autoritativen Source neu bauen und vollständige Datei-/Hash-/Fresh-Unpack-Identität prüfen. Vorher gebaute oder nur versionsgleich benannte ZIPs sind kein Beleg.
3. **Ein Vorgang, keine zweite Wahrheit:** Jede tatsächliche Entwicklung/Aktualisierung erhält genau eine `PU-YYYYMMDD-NNN`-Akte im `UPDATEPROTOKOLL.md`. Fach-/Release-/LIVE-Details bleiben an der Fachquelle; im PLUGINS-Büro nur Kontroll-/Inventarbezug.
4. **Keine Secrets:** Keine API-Keys, Tokens, Passwörter, Lizenzschlüssel oder sonstigen Secrets im Plugininventar/-protokoll.

Diese Regeln gelten für zukünftige Projekte/Büros ebenso; sie sind keine ADCELL-Sonderarchitektur.
