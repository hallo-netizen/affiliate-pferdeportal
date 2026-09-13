# BÜRO PLUGINS

STAND: 2026-09-12
STATUS: INVENTAR-/UPDATEBÜRO DES PFERDE-ATELIERS

## 1-KLICK-ÜBERSICHT

**WAS IST DAS?**  
Die zentrale Betriebsakte für alle auf der Pferde-Atelier-WordPress-Installation beobachteten Plugins: Bestand, Herkunft, zuständiges Fachbüro, Abhängigkeiten, Bewertung, Prüfbedarf, Aufräumkandidaten und Update-Nachweise.

**HIER BIST DU RICHTIG, WENN …**  
du wissen willst, welches Plugin installiert ist, ob es eine Eigenentwicklung ist, wer fachlich zuständig ist, ob es behalten/geprüft/aufgeräumt werden soll oder was bei einem Plugin-Update passiert ist.

**DU DARFST …**  
den installierten Pluginbestand inventarisieren, Fachzuständigkeiten verlinken, Risiken und Prüfbedarf markieren, Update-Ereignisse protokollieren und zu den autoritativen Fach-/Releasequellen weiterleiten.

**DU DARFST NICHT …**  
Fachlogik, Code, Release- oder LIVE-Status eines Plugins in diesem Büro neu erfinden; Plugins allein aufgrund einer Bewertung löschen/aktualisieren; Fachbüro-Wahrheiten kopieren; API-Keys, Passwörter, Tokens, Lizenzschlüssel oder andere Secrets speichern.

**ALS NÄCHSTES …**  
`CURRENT_STATE.md` → `HOBBYRAUM.md` → `PLUGINREGISTER.md` → bei Updates `UPDATEPROTOKOLL.md`.

## EINE WAHRHEIT – ROLLENTRENNUNG

Dieses Büro ist **Kontrollpult und Karteikasten**, nicht Eigentümer der Fachlogik.

- Installierter Pferde-Atelier-Bestand + betriebliche Bewertung → `PLUGINREGISTER.md`.
- Aktueller Bürostand → `CURRENT_STATE.md`.
- Aktuelle Arbeit / NEXT ACTION → `HOBBYRAUM.md`.
- Update-Chronik → `UPDATEPROTOKOLL.md`.
- Update-/Pflegeregeln → `REGELWERK.md`.
- Campusweiter Plugin-/Installer-Dateibeleg → `protocol/PROJECT_MEMORY/WORDPRESS_REGISTER.md`.
- Fach-/Release-/LIVE-Wahrheit → jeweils zuständiges Fachbüro bzw. dessen technische Originalquelle.
- Allgemeingültigkeit/Modulklasse → `protocol/PROJECT_MEMORY/ALLGEMEINGUELTIGE_BAUSTEINE/MODULREGISTER.md`.
- Geschäftlicher Eigenentwicklungs-/IP-Katalog → `protocol/PROJECT_MEMORY/PB_ONE/AKTENSCHRANK/PLUGINS/`; keine technische Statuskopie hieraus ableiten.

## FACHBÜROS

- `../TEXT/START_HERE.md` → Textmaschine / SEO / Produktion.
- `../PRODUKTVERGLEICH/START_HERE.md` → Produktwissen / Produktvergleich.
- `../DESIGN/START_HERE.md` → Design / Template / Frontend.
- `../BILD/START_HERE.md` → Bildzentrale.
- `../AFFILIATE/START_HERE.md` → Affiliate-Zentrale.
- `../HIVEPRESS/START_HERE.md` → HivePress / Anzeigenmarkt.
- `../GEMEINSAM/START_HERE.md` → projektweite Querschnittstechnik.

## PFLICHT VOR JEDER TECHNISCHEN PLUGIN-AKTION

1. `CURRENT_STATE.md` und `HOBBYRAUM.md` lesen.
2. `protocol/PROJECT_MEMORY/FEHLERREGISTER.md` → relevante autoritative Fehlerquelle prüfen.
3. Zuständiges Fachbüro + dessen CURRENT_STATE/HOBBYRAUM lesen.
4. Bekannte Wiederholungsfehler, Abhängigkeiten, Rollback- und Testgrenzen prüfen.
5. Erst danach Update, Deaktivierung, Löschung, Austausch oder Installation im zuständigen Arbeitsweg.

**Treffer in einer bekannten Fehler-/Sperrklasse = nicht erneut ausprobieren.**

## UPDATE-GRUNDSATZ

Jedes tatsächlich ausgeführte Plugin-Update erhält **genau einen** kanonischen Update-Eintrag `PU-YYYYMMDD-NNN` in `UPDATEPROTOKOLL.md`.

Das zuständige Fachbüro legt bei fachlich/technisch relevanten Updates nur einen kurzen Rückverweis auf diese PU-ID ab. Kein zweites vollständiges Updateprotokoll.

## SECRET-SPERRE

In diesem Büro niemals Zugangsdaten oder Secrets speichern. Erlaubt ist nur ein neutraler Verweis wie `SECRET_REF: externe sichere Ablage`.

## Globale Arbeitsort-Sperre

**Tresor, Archiv, Backup und Git-Mirror sind niemals Werkbank oder Runner-Quelle.**  
Autorität: `protocol/PROJECT_MEMORY/BAUCONTAINER/EINGANGSSTANDARD.md`.
