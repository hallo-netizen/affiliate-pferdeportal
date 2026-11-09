# ROBOTIK – EINZIGER KATEGORIE-ARBEITSABLAUF (KISS)
Stand 09.11.2026 | Ziel: maximale vollständige Prüfung bei minimalem Nutzeraufwand

## Grundlage: bestehendes Verfahren, nicht neu erfunden
Nachgeprüft an:
- `PROJEKTE/HOBBYRAUSCH/SEO_KATEGORIEN/ZIELVERTRAG_HD001_AUTOMATISCHE_SEO_HIERARCHIE_20261003.md` (Master → Drei Säulen → DataForSEO → Owner → WP)
- `ALLGEMEINGUELTIGE_BAUSTEINE/KATEGORIENMODELL/CURRENT_STATE.md` (14 Stufen read-only, v1.9.1, getrennter Writer)
- `PROJEKTE/EIGENTUMSSCHUTZ/KONZEPT/KATEGORIEN_NAVIGATION_PORTALSTANDARD_FEHLERLEHREN_20261017.md` (vollständiger Soll/Ist, echte Frontendtests; nicht wieder Altimportläufe aktivieren)
- `PLUGIN/ORIGINAL_AUDIT_20261109.md` (HAB-Plugin enthält Research/SEO/Validation, ABER alte projektgebundene Profile/Writer)

Das Ziel ist KEINE neue Maschine: **dieselbe eine Kategorieplugin-Identität** weiterentwickeln; die allgemeine geprüfte Research-Linie als Funktionsvorlage verwenden; keine Companion-Plugins, keine 5000 manuellen Dateien.

## Einfache fünf Schritte – nur EIN aktiver Ablauf

### 1. Bestand automatisch und vollständig einlesen – Benutzer: ein Klick
Das Plugin liest beim Admin-Aufruf aus **der eigenen WordPress-Installation**, ohne Datei-Uploads: Seiten (einschließlich verschachtelter Seite/Elternrolle), WordPress-Kategorien, Beiträge mit Zuordnung/Status, Magazin/Journal-Taxonomie, HivePress-Listingkategorien und tatsächlich vorhandene Anzeigen/Inserate. Es erkennt **ob HivePress/Journal tatsächlich eingerichtet sind** und zeigt anderenfalls "NICHT VERFÜGBAR/NOCH NICHT PRÜFBAR", niemals einen erfundenen PASS.

Zusätzlich: Affiliate-/Banner-/Werbeflächen nur bei nachgewiesener, lesender Schnittstelle zum tatsächlichen Affiliate-Plugin erfassen, ansonsten "NICHT ANGEBUNDEN". HivePress-Inserate und bezahlte Werbekacheln sind verschiedene Quellen!

Das aktive WordPress ist hier Wahrheit für den **Ist-Bestand**, aber es ist NICHT die fachliche Quelle des Soll-Baumes.

### 2. Chat + allgemeine Research-Funktionen pflegen EINEN Fachmaster
`RECHERCHE/PRODUKTE_V2_20261108.json`: einziger aktiver Robotik-Fachmaster mit stabilen `rb...`-IDs und Quellen; der alte 27er-Bestand ist Archiv. Chat recherchiert Produkte, Nutzungsfälle und **Randthemen** (fehlende Robotertypen, Synonyme, neue Branchen, Fachalternativen, kleine Nischen), markiert ungesicherte Fälle offen und trifft keine unbewiesenen Modell-/Produktgleichsetzungen.

Das Plugin liest den letzten **freigegebenen Revisionstand** des Masters (aus GitHub, nur im Admin beim Klick oder durch geprüften Server-Import), prüft Herkunft/Versionskennung und betrachtet DataForSEO-Keywords, Suchintents und Nachfrage als **Evidenz**, nicht als Quelle für neue Hauptwelten. Die 14 Recherche-/Prüfstufen des allgemeinen Workflows bleiben fachlich maßgeblich. Keine Kostenpflicht ohne explizite Vorprüfung/Freigabe.

**Wichtige Grenze heute:** Robotik 0.2.0 kann GitHub-Master und DataForSEO noch NICHT einlesen. Technische Integration ist ein noch offener Auftrag, kein vorhandener Knopf.

### 3. Eine vollständige Gesamtkontrolle für alle Säulen – Benutzer: ein Klick
Das Plugin erstellt aus zentralem Fachmaster (**Soll**) und WordPress (**Ist**) EINE Abdeckungsübersicht:
- **CORE-Seiten:** Hauptbereich → Zwischen-Seiten → letzte Seite = konkreter Robotertyp; richtige Eltern, eindeutige Produkt-ID, Slug, URL und sichtbare Navigation.
- **WP-Kategorien:** ausschließlich unter DER letzten Produktseite; flach, keine Kategorie-unter-Kategorie; pro fachlich sinnvoller Kategorie 3+ wirklich unterschiedliche potenzielle Beitragsthemen, kein bloßes Hochzählen von Synonymen.
- **Beiträge/Inhalte:** tatsächliche WP-Beiträge und Bindungen zählen; fehlende, verwaiste, doppelte, fachlich falsche oder alte Beiträge als **Prüffälle** markieren. Tiefe fachliche Textqualität nur mit gesondert verifizierter Textanalyse, niemals durch das bloße Zählen behaupten.
- **Magazin/Journal:** eigener Themen-/Suchintent-Owner; thematische Lücken, Verweise zu Produktseiten, keine Konkurrenz zum CORE-Produkt-Owner.
- **HivePress:** getrennte Listingkategorien und tatsächliche Inserate; gewerbliche Anbieter, Installation, Wartung, Mietangebote etc. ohne Zwang zu einem zweiten Produktbaum.
- **Anzeigen/Affiliate:** belegte tatsächliche Werbeslots/Bannerzuordnungen und fehlende Monetarisierungswege nur nach Schnittstellen-Audit; nie Anzeigen und HivePress-Inserate verwechseln.
- **Randthemen:** Research-Restliste mit neuen, unklaren, seltenen oder überschneidenden Themen; NICHT still löschen, nicht als unfertiges Produkt veröffentlichen.
- **Global:** je Suchintent genau EIN fachlicher Haupt-Owner, identische Begriffe können relationale Verweise sein; Alt-/Neubestand gemeinsam prüfen.

Der Bericht muss `OK / FEHLT / KONFLIKT / UNGEPRÜFT / NICHT ANGEBUNDEN` pro Prüfbereich unterscheiden, mit Grund, Quelle und konkreter Handlung. **UNGEPRÜFT gilt NIEMALS als OK.** Ein zusammengefasster Freigabebildschirm statt hunderter Einzeldateien.

### 4. Geprüfte Vorschläge entscheiden – Benutzer: nur Sammelfreigabe oder Ausnahme
Das System zeigt in einem Bildschirm ausschließlich **Deltas und echte Konflikte**: neue/umbenannte/verschobene/zusammenzuführende Produktseiten, Kategorien, Magazin-/HivePress-Rubriken, Artikel-Lücken, offene Randthemen. Chat erarbeitet fachliche Vorschläge; das Plugin blockiert technische Unvereinbarkeiten. Freigabe erst nach fachlicher Prüfung; automatische Beratung ersetzt die Freigabe nicht.

Keine automatische 1:1-Übernahme der 68 ungeprüften Robotertypen. Kein künstliches Auffüllen von 3+ Beiträgen, keine starre Maximalanzahl an Produkt- oder Kategorien-Leafs. Struktureller Sollbaum wird AUSSCHLIESSLICH aus freigegebenen Master-IDs abgeleitet; er ist kein eigener, frei mutierender Forschungsbestand.

### 5. Freigeben → ein Writer → Nachprüfung
Schreibfreie Vorschau (add/rename/move/merge/archive) gegen tatsächlichen Bestand. Nach ausdrücklicher Freigabe **genau ein** kontrollierter WordPress-Writer für freigegebene Seiten und Kategorien; **keine** Artikelproduktion im Kategorieplugin. Inhalts- und Anzeigenplugins bleiben für ihre eigenen Inhalte zuständig. Reale WP-Seiten, Kategorien, HivePress, Original-Frontend/Design (Desktop und Mobil) erneut einlesen und Abweichungen statt falschem "fertig" melden. Alte Durchläufe nicht erneut starten.

## Das minimiert wirklich die Arbeit
- **Normalbetrieb:** im Backend `Gesamtprüfung starten` → einen Bericht mit offenen Ausnahmen ansehen → `Freigegebene Änderungen übernehmen`. Keine Einzeldatei-Uploads.
- **Chat/Plugin-Abstimmung:** Chat pflegt GitHub-Master; Plugin zieht dieselbe **nachweisbare Master-Revision**. Änderungen aus WordPress werden niemals still in den Master zurückgeschrieben.
- **Bis die technische Datenverbindung gebaut ist:** maximal EINE maschinenlesbare Gesamtbericht-Datei je benötigtem Chat-Review, nicht tausende einzelne Dateien. **Null-Datei-Austausch mit Chat ist derzeit technisch NICHT eingerichtet**; dies ist kein Versprechen.
- **Keine zusätzliche DB-Tabelle**, kein Frontend-Netzwerkabruf, keine automatischen Bezahl-API-Calls, keine Neben-Plugins/zweiten Writer und keine verdeckten Portal-Fremdprofile.

## In dieser Reihenfolge technisch umsetzen
1. **Read-only-Bestandsaufnahme WP** und Felder/aktive Plugins belegen; ein Gesamtbericht im Admin. Erst auf frischer Robotik-Testinstallation mit tatsächlichen Plugins testen; nicht verfügbare Quellen offen ausweisen.
2. **GitHub-Master-Revisionsabgleich** im Admin anbinden (read-only, manuell ausgelöst). Bei fehlender/alter Revision blockieren, nicht aus lokalem Altentwurf fortfahren. Keine zusätzliche WordPress-Produktliste aufbauen.
3. **Bestehende allgemeine Recherche-/SEO-/Gap-Prüfung** in dieselbe Robotik-Pluginidentität übernehmen. Bezahlte Recherche separat freigeben.
4. **Drei Pilot-Robotertypen** gegen alle drei Säulen und einen echten Hersteller-/Quelle/Intent-Fall mit positiver UND negativer Prüfung testen. Ergebnis auf WordPress sichtbar nachlesen.
5. Erst dann den **bestehenden kontrollierten Importmechanismus** für Robotik und die korrekte *WordPress-Seitenerzeugung* adaptieren: die historische allgemeine V1.8.0 konnte nur Taxonomie-Objekte schreiben. Keine bestehende Writerfähigkeit für Seiten erfinden.

**Freigabetests:** Prüft das System 0 und 1000+ echte WP-Objekte? Alte/neue Objekte? drei Säulen? eingeschränkte Plugins? veralteter GitHub-Master? ungültige Zuordnungen, Fake-Beitragskapazität, Intent-Dubletten, absichtlich nicht belegte Anzeigen, abweichende WP-Ist-Daten? Dry-run, Wiederholungssperre, Readback? Fehlerfall muss sichtbar sein. Kein Live-PASS nur durch lokale Tests.

## Derzeitiger Status
**BESCHLOSSENER ARBEITSABLAUF, NOCH KEINE TECHNISCHE UMSETZUNG DER OBIGEN VOLLAUTOMATIK.** Die installierte 0.2.0 zeigt nur gültige/ungültige JSON-Entwürfe. Kein automatischer WP-Bestandsscan, kein GitHub-Lesen, kein kompletter Drei-Säulen-Check, keine Affiliateprüfung, kein automatisierter Import. Diese Grenzen dürfen niemals als erledigt gemeldet werden.
