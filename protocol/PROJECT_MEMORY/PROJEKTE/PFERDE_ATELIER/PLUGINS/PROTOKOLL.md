# PLUGINS – PROTOKOLL

STAND: 2026-09-12

Chronik/Belege dieses Büros. Niemals CURRENT_STATE ersetzen.

## 2026-09-12 – Ersteinrichtung / Inventurbaseline

AUSLÖSER:
Der Nutzer verlangt im Pferde-Atelier ein dauerhaftes Büro `PLUGINS`, das den vollständigen WordPress-Pluginbestand, Eigenentwicklungen, Fachzuständigkeiten, Bewertungen und künftige Updateverweise bündelt.

AUSGANGSBEFUND:
Der Campus besaß bereits ein campusweites `WORDPRESS_REGISTER.md`. Dessen bisherige KISS-Regel lautete ausdrücklich: kein eigenes WordPress-Büro, solange keine dauerhafte WordPress-Facharbeit entsteht.

NEUER BEDARF:
Mit 55 installierten Pluginzeilen über mehrere Fachbüros und dem ausdrücklich gewünschten dauerhaften Update-/Lifecycle-Prozess ist erstmals eine wiederkehrende projektweite Plugin-Betriebsarbeit vorhanden.

KRITISCHE ENTSCHEIDUNG:
Ein **dünnes Kontrollbüro** ist sinnvoll. Ein zweites technisches Pluginarchiv mit kopierten Release-, LIVE-, Code- und Fachständen wäre übertrieben und würde die Campusregel `EINE WAHRHEIT` verletzen.

KISS-MODELL:
- PLUGINS = installierter Pferde-Atelier-Bestand, Zuständigkeit, Bewertung, Update-ID/Chronik;
- Fachbüros = Fach-/Release-/LIVE-Autorität;
- WORDPRESS_REGISTER = campusweiter Installer-/Artefaktindex;
- MODULREGISTER = Modulklasse;
- PB ONE Pluginfach = geschäftlicher Eigenentwicklungs-/IP-Katalog.

UPDATE-MODELL:
Ein Update = genau ein `PU-YYYYMMDD-NNN`-Eintrag in `UPDATEPROTOKOLL.md`; betroffenes Fachbüro hinterlegt nur einen Rückverweis auf die PU-ID.

INVENTAR:
- 55 Pluginzeilen erfasst;
- 28 Eigenentwicklungszeilen / 27 unterschiedliche Eigen-/Projektplugins;
- 27 Drittanbieterzeilen;
- 4 sichtbar inaktive Zeilen;
- 6 sichtbare Drittanbieter-Updatehinweise als reine Beobachtung aufgenommen;
- keine Pluginänderung ausgeführt.

SICHERHEIT:
Keine Zugangsdaten/Secrets übernommen oder gespeichert.

ARCHITEKTURGRENZE:
Die Bürodaten wurden auf einem isolierten Campus-Kandidatenbranch angelegt. Die offizielle Campusintegration darf erst erfolgen, wenn die campusweit vorgeschriebene Architektur-WAS/WARUM- und Bauprotokoll-Kopplung an den zentralen Autoritätsstellen vollständig und sicher nachgezogen ist. Bis dahin kein falscher Integrations-PASS.
