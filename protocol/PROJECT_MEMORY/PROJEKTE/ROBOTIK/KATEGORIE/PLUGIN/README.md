# PLUGIN – ROBOTIK KATEGORIE (NEUTRALSTART 0.1.0)

**Datei:** `CURRENT.zip` – installierbares WordPress-Plugin mit eigenem Verzeichnis `robotik-kategorie-workflow`.

**Funktion heute:** Admin-Menü „Robotik Kategorie“, getrennte Darstellung der drei Säulen, JSON-Strukturprüfung, Entwurf speichern. 0 vorgefüllte Knoten. Keine automatische Verbindung zu Fremdseiten, APIs oder Datenbanken außerhalb des neuen WordPress.

**Absichtlich noch NICHT enthalten:** Kategorie-/Seiten-/HivePress-Live-Importer, Bearbeiten oder Löschen bestehender WP-Objekte, automatisches Keyword-Rechercheprogramm, Frontend-Navigation. Die bewährte kontrollierte Importstrecke wird erst nach dem beschlossenen Robotik-Fachbaum mit frischem Portalprofil eingebunden und separat getestet. Dies ist kein Ersatz für einen vollständig getesteten Produktions-Workflow.

**Installation:** WordPress → Plugins → Plugin hinzufügen → Plugin hochladen → `CURRENT.zip` → aktivieren → Menü „Robotik Kategorie“.

**Prüfung am 08.11.2026:** ZIP 2.589 Bytes, SHA-256 `9aea1cae303f432205489efd8cb43f6edbfc56d59fca4173bfd55895276669a0`; PHP-Lint PASS; ZIP-CRC PASS; keine Namen alter Portale im PHP; kein Live-Test.

**Kein zweites Kategorie-Plugin parallel auf der neuen Site installieren.** Vor spätem Import entscheiden, welcher eine Writer verbindlich ist.

## Testkandidat 0.2.0 – 08.11.2026
**Datei:** `INSTALLATIONSKANDIDAT_0.2.0.zip`, 4038 Bytes, SHA256 `ee09b6b88342cd1d77594d4490d4d468f3bcfbf43c15c8e0ba6882910dbeee9d`.

**Original 0.1.0 bleibt als CURRENT.zip unangetastet**, da noch keine reale WordPress-Freigabe. Die 0.2.0 baut auf derselben Plugin-Identität/Ordnerstruktur auf und ist für die erste **Testinstallation** geeignet; NICHT für das Anlegen eines WordPress-Kategoriebaums.

Verbessert: `role=group` für Sammelseiten, `role=product` für letzte konkrete Produktseite, ausschließlich darunter `content_category`; global eindeutige Kategorie-Slugs; Unterscheidung `phase=draft` / `phase=final`, im finalen Stand 3 unterschiedliche grobe Themenrichtungen (`topic_directions`) je Inhaltskategorie. Keine echten Artikeltitel erforderlich.

Lokale Prüfung: PHP-Lint PASS, ZIP-CRC PASS (2 Dateien), 16 positive/negative Strukturtests PASS. PHP ohne alte Portalbegriffe/URLs und ohne API-, Import-, Cron- oder DB-Schreibfunktionen außer normaler WordPress-Entwurfsoption. Ein echter WordPress- und HivePress-Test steht aus.

**Grenze:** DataForSEO-, Keyword-Recherche-, semantische Entdopplungs- und WP-Importfunktionen der historischen Kategorie-Engine sind NOCH NICHT portiert. Keine Verwechslung von syntaktischer Validierung mit fachlicher Recherche. Die Testinstallation darf ausschließlich einen leeren/Probe-Entwurf prüfen; keine alten Zielprofile importieren.

## Pflicht-Audit vor Übernahme alter Funktionen
[ORIGINAL_AUDIT_20261109.md](ORIGINAL_AUDIT_20261109.md): vollständiges HAB-ZIP nicht neutral; alte Importprofile/-Wellen dürfen nicht übernommen werden. Der allgemeine 14-Stufen-Read-only-Prozess ist die fachliche Referenz. Keine Behauptung einer fertigen Robotik-Research-Integration.
