# Hobbydepot Texterstellung – tatsächlich sichtbarer Recherche-Stand, 19.11.2026 09:45

Beleg: Betreiber-Screenshot `hobby-depot.de/wp-admin/admin.php?page=texterstellung-recherche`. Maßgebliche aktuell ausgehändigte ZIP unverändert 0.4.24.5.

## Beobachtet (kein geratenes WordPress-DB-Ergebnis)
- Bisherige Migrations-/Sandbox-Blockermeldungen **nicht mehr auf der gezeigten Rechercheoberfläche sichtbar**; stattdessen normaler Kategorie-Recherchebereich.
- `RECHERCHE GESTOPPT`, Grund `PLUGIN_ACTIVATED_MANUAL_START_REQUIRED`, „Kein automatischer Neustart.“ **Kein kostenpflichtiger Lauf automatisch gestartet.**
- **379 noch nicht recherchierte Themenbereiche**, **0 recherchiert**, **0 mit Fehler/gesperrt**.
- Die angezeigten **379 Themenbereiche** stammen laut Oberfläche aus **2.241 Artikelkategorien (alle 2.241 zugeordnet)**; WordPress aktuell **3.520 Kategorien**.
- Nächstes Thema **3D-Bogenschießen**; voreingestellte Anzahl **5**, Checkbox für kostenpflichtige DataForSEO-Recherche **nicht markiert**; Recherche-Button sichtbar, **nicht angeklickt**.
- `Auftragsregal: 0`, `Bereits gespeicherte Originaldaten: 0 Themen`.
- Die Oberfläche allein ist kein Nachweis, dass sämtliche migrationsinternen Integritätsprüfungen auf dem echten Server vollständig protokolliert sind. Insbesondere ist keine neue Diagnose/DB-Zugriff vorhanden. Die im aktuellen WordPress laufenden Plugin-Bytes wurden nicht direkt ausgelesen.

## Aktuelle Plugin-Bytes verifiziert und in beiden Büros unverändert aufbewahrt
- `/Hobby Depot/Plugin-Büro/Texterstellung_Hobbydepot_0.4.24.5_SANDBOX_LEERBESTAND_FIX.zip`.
- `/hobbydepot/TEXTERSTELLUNG/INSTALLATIONSKANDIDATEN/Texterstellung_Hobbydepot_0.4.24.5_SANDBOX_LEERBESTAND_FIX.zip`.
- **ZIP aus zentralem Pluginbüro zurückgelesen und technisch geprüft**, 506.541 Bytes, SHA256 `42f648b59a99fda0b1684c0e174a9430f4d9d131eaa8d98548157c5d8e09e2ba`, ZIP CRC 87/87, 78 PHP, 8 JSON, WordPress Hauptdatei `texterstellung-hobbydepot/texterstellung.php` meldet Version 0.4.24.5. **Keine neue ZIP und kein neuer Code.**
- Eigene Current-Akte `/Hobby Depot/Plugin-Büro/Texterstellung-CURRENT.md` aktualisiert (globales CURRENT anderer Plugins unangetastet); Standbericht `/Hobby Depot/Plugin-Büro/Texterstellung_Stand_20261119_0945.md` hinterlegt; Fachkopien ebenfalls geschrieben.

## Schluss / nächster Schritt
Die Einrichtung scheint nun weit genug, dass die normale Kategorien-Recherchebedienung angezeigt wird. Aber **379 Themenbereiche warten noch**. Bevor bezahlte DataForSEO-Recherche ausgeführt wird, ist eine **bewusste Kostenentscheidung** erforderlich. Nicht per Protokoll oder ohne Userklick ausführen. Die vorher nachgewiesene K0-Artikelarten-/Portalzuordnungssperre bleibt durch diesen Screenshot unaufgehoben. Keine Artikelproduktion behaupten.

**Verbindlich:** Bei jedem neuen Live-Befund genau einen aktuellen Projekt- und Bürostatus pflegen und genau die neueste tatsächlich geprüfte ZIP unverändert aufbewahren. Keine parallelen Neu-/Umbauten.
