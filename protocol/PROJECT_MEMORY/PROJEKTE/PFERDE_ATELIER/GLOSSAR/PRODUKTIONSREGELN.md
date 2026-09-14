# GLOSSAR – PRODUKTIONSREGELN

STAND: 2026-09-14
STATUS: VERBINDLICH

## 1. Fachautorität

Die fachliche Wahrheit liegt ausschließlich im zentralen WDB-Aktenschrank:
`../WISSENSDATENBANK/AKTENSCHRAENKE/GLOSSAR/`.

Ein Begriff = ein zentraler Datensatz. WordPress und JSON-Batches sind Ausgabe-/Transportwege und keine zweite Fachwahrheit.

Neue Glossarinhalte dürfen nur aus frisch belegten, ausreichend geprüften WDB-Daten erstellt werden. Keine Ergänzung aus Chatwissen ohne Fachbeleg.

## 2. Themencluster statt isolierter Beziehungen

Sobald bei einem neuen Glossarbegriff fachlich sinnvolle verwandte Glossarbegriffe festgestellt werden, werden diese als technische Beziehungen mitgedacht und – nur bei frisch belegter `GEPRUEFT`-WDB-Quelle – im selben Produktionszusammenhang ergänzt.

Ein Glossar-Produktionslauf gilt erst als vollständig, wenn:
- jeder als verwandt ausgewiesene Begriff als echter Glossarbeitrag existiert oder die Relation bewusst offen bleibt;
- die Beziehungen technisch auflösbar sind;
- die Box `Verwandte Begriffe` nur echte veröffentlichte Glossarbeiträge verlinkt;
- der gesamte Fließtext **0 Links** enthält;
- die passende Portal-Kategorie ausschließlich rechts in `Mehr zum Thema` verlinkt wird;
- kein Linkziel doppelt gesetzt ist.

## 3. Textaufbau

Pflicht für Glossarbeiträge:
- Titel;
- sichtbare Kurzdefinition/Zusammenfassung;
- ca. 150–200 Wörter;
- wenige natürliche Absätze;
- **keine Zwischenüberschriften**;
- **0 Links im Fließtext**;
- verwandte und thematische Links ausschließlich in den rechten Seitenboxen.

Keine H2/H3 im Begriffstext aus SEO-, Schema- oder Gestaltungsmotiven.

## 4. Interne Links

Verbindlich je Begriff:
- im Fließtext **kein Link**;
- verwandte Glossarbegriffe ausschließlich als Links in der rechten Box `Verwandte Begriffe`;
- Portal-Kategorie ausschließlich als Link in der rechten Box `Mehr zum Thema`;
- Journal dort nur ersatzweise, wenn kein passendes Portal-Ziel existiert;
- dasselbe Ziel niemals doppelt auf derselben Einzelansicht.

Details ausschließlich in `TEXT_UND_LINKREGELN.md`.

## 5. Verwandte Begriffe

`Verwandte Begriffe` ist kein Freitext-Friedhof.

Ein Begriff darf dort nur als Link erscheinen, wenn ein echter `uge_term` dazu existiert und das Ziel technisch auflösbar ist.

Fehlt der verwandte Begriff, darf er nur produziert werden, wenn seine WDB-Quelle frisch ausreichend belegt ist. Keine Erzeugung aus Chatwissen oder Alt-Paketen ohne Fachbeleg.

## 6. Pferderassen

**Pferderassen und Ponyrassen sind im Glossar tabu.**

Sie gehören ausschließlich in das separate Pferderassen-System und werden weder als Glossarbeitrag noch als automatisch nachgezogener verwandter Begriff erzeugt.

## 7. Bestehende Glossarbeiträge

Bereits veröffentlichte oder angelegte Glossarbeiträge werden wegen neuer Regeln nicht pauschal gelöscht.

Stattdessen gilt:
1. vorhandenen Beitrag eindeutig per Slug/ID bestimmen;
2. bestehenden Datensatz gezielt aktualisieren, ID und URL erhalten;
3. Inhalt, Kurzdefinition, Metaangaben, Portalbindung und Relationsdaten prüfen;
4. sämtliche Links aus dem Fließtext entfernen; Linktext als normalen Text erhalten;
5. verwandte Links ausschließlich rechts in `Verwandte Begriffe`, Portalziel ausschließlich rechts in `Mehr zum Thema` ausgeben;
6. normale WordPress-Beiträge negativ gegen Veränderung prüfen;
7. erst nach vollständiger technischer und erforderlicher Liveprüfung auf `FERTIG` setzen.

Löschen ist nur zulässig, wenn ein echter Dublette-, Fehl- oder Testdatensatz nachgewiesen ist.

## 8. Portal-/SEO-Gates

Für neue Glossarkandidaten gilt vor Produktion:

1. gegen echte WordPress-Kategorien und starke veröffentlichte Portal-Landingpages prüfen;
2. Portal-Hauptseiten können normale hierarchische WordPress-Seiten (`post_type=page`) sein;
3. bei echter Kategorie-/Portal-Kollision keinen konkurrierenden Glossarbeitrag produzieren;
4. normale Beiträge bleiben Teil der Kannibalisierungsprüfung, sind aber nicht automatisch Portal-Landingpages;
5. bestehende veröffentlichte Glossarbeiträge werden durch neue Kandidatenregeln nicht pauschal gelöscht.

## 9. Neuer verbindlicher Produktionsweg – JSON statt autonome Textautomation

Der Produktionsweg ist ab jetzt:

`WDB-Aktenschrank -> Chat-Texterstellung nach festen Regeln -> JSON-Batch -> Glossar-Importer -> WordPress-Draft -> Readback -> manuelle/gesonderte Freigabe`

Verbindlich:
- das Plugin schreibt den Text nicht frei selbst;
- Chat liefert fertige Glossarbeiträge als JSON-Datei;
- Plugin validiert Vertrag, WDB-ID/Begriff, Slug, Textregeln, Relationen und Metadaten;
- Write zunächst ausschließlich als Draft;
- definierte Felder werden nach WordPress-Write real zurückgelesen;
- Readback-Mismatch muss fail-closed enden und neu angelegte Batchwrites zurückrollen;
- kein Auto-Publish als Normalweg;
- normale WordPress-Posts/-Pages dürfen durch den Import nicht verändert werden;
- Batchgröße wird im neuen Importvertrag hart begrenzt und getestet;
- Reimport/Dublette muss blockiert oder kontrolliert als Bestandsupdate behandelt werden.

Konzeptionelle Referenz:
`Pferde Atelier – Pferderassen Manager 0.2.0`.

## 10. JSON-Batch – Zielvertrag für den Umbau

Der neue Glossar-Importer erhält einen eigenen festen Batchvertrag. Mindestens je Begriff vorgesehen:
- stabile WDB-`source_id` / `term-*`;
- `begriff`;
- `slug`;
- `oberbereich`;
- optional `unterbereich`;
- `titel`;
- `kurzdefinition`;
- `artikeltext`;
- `verwandte_source_ids`;
- primäres Portalziel / gebundene Ziel-ID;
- `meta_title`;
- `meta_description`.

Der exakte JSON-Vertrag wird beim Pluginumbau versioniert festgelegt und positiv/negativ getestet. Bis dahin keine JSON-Datei als Produktionsfreigabe behaupten.

## 11. Autoritatives Produktionsregister

Die Produktionswahrheit `OFFEN / JSON_GEPRUEFT / DRAFT / DRAFT_READBACK_PASS / VEROEFFENTLICHT / GESPERRT` soll künftig aus zentralem WDB-Bestand plus realem WordPress-Bestand abgeleitet werden.

`BEGRIFFSREGISTER.md` bleibt bis zur importergebundenen Migration bestehender Statusweg; keine zweite parallele Erledigt-Liste anlegen.

## 12. Abgelöster Automationsweg – nur Historie

Die frühere autonome Kette mit PSTE-Discovery, Retained/Planning, WP-Cron, Loopback-Worker, Research-Paket und Auto-Publish ist **abgelöst** und keine aktive Produktionsregel mehr.

Historische technische Belege bleiben in:
- `FEHLERQUELLEN.md`;
- `CURRENT_STATE.md` nur als abgelöster Vorstand, falls nötig;
- vorhandenen Testreports/Pluginpaketen 1.3.5–1.3.8.

Insbesondere gilt nicht mehr als NEXT ACTION:
- 1.3.8 installieren, um Loopback/Planning weiterzutesten;
- Auto-Publish-Strecke fertigbauen;
- Worker-/Cron-/Planning-System weiter ausbauen.

## 13. PASS-GRENZE für den neuen Weg

Kein Produktions-PASS, bevor der neue JSON-Importer real bewiesen hat:
- gültiger Batch → Draft;
- ungültiger Batch → BLOCK;
- Dublette/Reimport → kontrolliert BLOCK/Update gemäß Vertrag;
- 0 Bodylinks;
- keine Pferderassen im Glossar;
- Relation nur zu gültigen Begriffen;
- WordPress-Readback vollständig;
- absichtlich korrupter Readback → Rollback/BLOCK;
- normale Posts/Pages unverändert;
- exakte fertige ZIP positiv/negativ/regressiv geprüft.
