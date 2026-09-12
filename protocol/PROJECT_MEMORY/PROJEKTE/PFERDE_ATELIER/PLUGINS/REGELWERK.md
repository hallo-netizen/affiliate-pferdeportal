# PLUGINS – REGELWERK

STAND: 2026-09-12
STATUS: KISS-BETRIEBSREGEL

## ZWECK

Dieses Büro löst eine einzige Querschnittsfrage:
**Welche Plugins sind auf dem Pferde-Atelier installiert, wer ist zuständig und was wurde bei Updates tatsächlich getan?**

Es ist bewusst **keine zweite Entwicklungsabteilung**.

## 1. EINE WAHRHEIT

- `PLUGINREGISTER.md` = beobachtetes Pferde-Atelier-Inventar + Zuständigkeit + betriebliche Bewertung.
- `UPDATEPROTOKOLL.md` = einzige Plugin-Update-Chronik dieses Projekts.
- Fachbüro = technische/fachliche Hauptwahrheit des Eigenplugins bzw. der betroffenen Funktion.
- `protocol/PROJECT_MEMORY/WORDPRESS_REGISTER.md` = campusweiter Installer-/Artefaktindex, nicht Projekt-LIVE-Register.
- MODULREGISTER = Allgemeingültigkeits-/Modulklassifikation.
- PB ONE Pluginfach = geschäftlicher Eigenentwicklungs-/IP-Katalog, nicht technische Wahrheit.

Keine dieser Rollen wird kopiert.

## 2. UPDATE-ID

Jedes **tatsächlich ausgeführte** Plugin-Update erhält genau eine ID:

`PU-YYYYMMDD-NNN`

Beispiel: `PU-20260912-001`.

Ein verfügbarer Update-Hinweis ohne Durchführung erhält **keine** PU-ID; er bleibt nur als beobachteter Hinweis im Inventar/CURRENT_STATE.

## 3. PFLICHTDATEN JE UPDATE

- Plugin-ID und exakter Pluginname;
- Eigenentwicklung / Drittanbieter;
- zuständiges Fachbüro;
- Ausgangsversion;
- Zielversion;
- Updatequelle;
- Anlass/Warum;
- betroffene Abhängigkeiten/Schnittstellen;
- Backup-/Rollback-Referenz;
- relevante Fehlerquellen vor der Änderung;
- Positivtest;
- Negativtest, soweit für die Änderung erforderlich;
- Fach-/Regressionstest gemäß zuständigem Büro;
- WordPress-Livebeobachtung nach Update;
- Ergebnis `PASS | FAIL | ROLLBACK | BLOCKED`;
- Referenz im Fachbüro.

Unbekannte Pflichtdaten = `PRÜFEN` bzw. `BLOCKED`, niemals schätzen.

## 4. FACHBÜRO-VERWEIS

Bei jeder Eigenentwicklung und bei funktional relevanten Drittanbieter-Updates gilt:

1. PLUGINS erzeugt/führt den **einen** PU-Eintrag.
2. Zuständiges Fachbüro protokolliert nur eine Kurzreferenz wie:  
   `PLUGIN_UPDATE_REF: PU-20260912-001`.
3. Fachbüro darf zusätzlich seine fachlich notwendigen Test-/Releasebelege führen; das vollständige Updateereignis wird nicht dupliziert.

Damit entsteht eine **bidirektionale Verbindung ohne doppelte Wahrheit**.

## 5. EIGENENTWICKLUNGEN

PLUGINS darf Eigenentwicklungen nach Fachbüro sortieren und deren Zweck/Abhängigkeit beschreiben.

PLUGINS darf **nicht** selbst:
- Fachlogik ändern;
- Release bestimmen;
- Versionsnummer erfinden;
- einen Kandidaten zum LIVE-Stand erklären;
- ein Fachbüro umgehen.

## 6. DRITTANBIETER

Drittanbieter-Updates werden risikobasiert behandelt:

- **KRITISCH**: Kernsystem, SEO, Login, Datenschutz, Cache, Backup, HivePress-Kern → Fachwirkung vor Update prüfen.
- **WICHTIG**: aktive Funktion mit sichtbarer Portalwirkung → Zuständigkeit/Testweg prüfen.
- **HILFSWERKZEUG**: Import, Diagnose, Adminhilfe → Nutzung vor Update/Entfernung prüfen.
- **AUFRÄUMKANDIDAT**: inaktiv/abgelöst/temporär → erst Daten-, Abhängigkeits- und Rollbackprüfung, dann Entscheidung.

`AUFRÄUMKANDIDAT` bedeutet niemals automatisch `LÖSCHEN`.

## 7. UPDATE-ABLAUF – KISS

`Plugin auswählen → Fehler-/Abhängigkeitscheck → Fachbüro → Backup/Rollback → Update → erforderliche Positiv-/Negativ-/Regressionstests → Livekontrolle → PU-Protokoll → Fachbüro-Rückverweis`.

Keine zusätzliche Plugin-Release-Pipeline und kein eigener Runner nur für dieses Büro.

## 8. DEAKTIVIERUNG / LÖSCHUNG

Vor Deaktivierung oder Löschung zwingend prüfen:

- wird das Plugin von einem anderen Plugin benötigt?
- besitzt es relevante Daten/Optionen/Tabellen?
- gibt es Frontend-/Admin-Hooks oder Shortcodes?
- ist es Teil eines dokumentierten Produktions-/Prüfwegs?
- existiert ein Rückweg/Installer/Backup?
- hat das zuständige Fachbüro zugestimmt bzw. die technische Wirkung geprüft?

Unklar = **NICHT ENTFERNEN**.

## 9. INFORMATIONSTIEFE PRO PLUGIN

Das Register darf für jedes Plugin folgende Informationen führen, soweit belegt:

- WordPress-Name / Slug;
- Hersteller/Autor;
- Eigenentwicklung/Drittanbieter;
- installierte Version und Aktivstatus;
- verfügbare Updateversion als Beobachtung;
- zuständiges Fachbüro;
- Zweck;
- Kritikalität;
- direkte Abhängigkeiten und abhängige Plugins;
- relevante Schnittstellen/Shortcodes/Hooks;
- Datenbanktabellen/Optionen/Cronjobs;
- externe Dienste;
- Datenschutz-/Security-Relevanz;
- Backup-/Rollbackquelle;
- Quellcode-/Installer-/Master-/Releasequelle;
- letzte geprüfte Aktualisierung;
- bekannte Fehler-/Regressionen;
- Einschätzung `BEHALTEN | PRÜFEN | HILFSWERKZEUG | AUFRÄUMKANDIDAT`.

Nicht belegte Felder bleiben `PRÜFEN`; sie werden nicht mit Vermutungen gefüllt.

## 10. SECRET-SPERRE

Nie speichern:
API-Key, Token, Passwort, Lizenzschlüssel, Webhook-Secret, private Signierschlüssel oder vergleichbare Zugangsdaten.

Nur neutrale Referenzen auf eine dafür vorgesehene sichere Ablage sind zulässig.
