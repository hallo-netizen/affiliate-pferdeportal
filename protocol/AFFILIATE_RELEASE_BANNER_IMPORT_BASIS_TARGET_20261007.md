# AFFILIATE-ZENTRALE — VERBINDLICHER ZIELVERTRAG BANNER-IMPORT-BASIS

Stand: 2026-10-07  
Repository: `hallo-netizen/affiliate-pferdeportal`  
Branch: `affiliate-release-current`  
Workstream: `AFFILIATE_ZENTRALE`

Rolle: dauerhafte Ziel-/WARUM-Quelle für den aktuell offenen Banner-Basisblock. **Keine CURRENT-/Status-/NEXT-ACTION-Wahrheit.** Diese steht ausschließlich in `control/release-governance/CURRENT_RELEASE.json`.

## 1. Anlass

Die Live-Folge 6.72.195 bis 6.72.198 hat gezeigt, dass nachgelagerte Reconcile-, Dropdown-, Fixed-Target- und Klassifikationsänderungen nicht ausreichen, solange die importierte Bannerbasis selbst nicht vollständig und beweisbar ist.

Der belegte Quellbefund vor 6.72.199: Der ADCELL-Import baute bei fehlendem Providertitel selbst einen semantisch wirkenden Titel wie `procavallo Banner 393923 – Ausrüstung` und transportierte nur ausgewählte Felder des Providerdatensatzes weiter. Damit konnte nachgelagerte Zuordnung mit einer verlustbehafteten bzw. teilweise synthetischen Datenbasis arbeiten.

**HARD RULE: Erst die vollständige Importbasis beweisen. Vorher keine neue Zuordnungs-/Rankingregel.**

## 2. Zielzustand der Basis

Für jedes importierte reale Banner müssen die tatsächlich verfügbaren Originaldaten des Providers erhalten und ihre Herkunft unterscheidbar bleiben.

Mindestens verbindlich:

- Provider- und Partneridentität;
- Creative-/Promotion-Identität;
- vollständiger vom Provider gelieferter Banner-Rohdatensatz, unverändert gespeichert und per SHA-256 integritätsgebunden;
- echte Providerfelder wie Titel/Name nur dann als solche verwenden, wenn sie wirklich geliefert wurden;
- fehlt ein echter Providertitel, darf kein selbst gebauter Ersatztitel als fachliche Evidenz ausgegeben werden;
- Provider-Kategorie-ID erhalten;
- Provider-Kategoriename über den belegten Provider-Kategorienvertrag auflösen, soweit verfügbar; nicht raten;
- Provider-`information` und sonstige gelieferte Fachfelder erhalten;
- Tracking-URL erhalten;
- reale/decodierte/einmalig beim Import aufgelöste Ziel-URL samt Provenienz erhalten;
- Bildquelle, tatsächliche Maße, Assetprüfung und bestehende technische Verifikation erhalten.

Unbekannte oder künftig relevante Providerfelder dürfen nicht stillschweigend verloren gehen.

## 3. Ziel-URL-Regel — Präzisierung des 6.72.190-KISS-Vertrags

Die Ziel-URL bleibt **gültige und wichtige Evidenz**, ist aber nicht automatisch die einzige fachliche Evidenz.

Beispiele:
- konkrete Shop-Zielseite `/schabracken/` kann eine konkrete Schabracken-Zuordnung stützen;
- breite Zielseite `/ausruestung/` darf höchstens eine entsprechend breite Ausrüstungszuordnung stützen;
- reine/undurchsichtige Tracking-URL beweist kein konkretes Thema;
- konkrete echte Provider-Kategorie oder echte Provider-Beschreibung kann zusätzliche belastbare Evidenz liefern.

Was unverändert bleibt:
- keine Zielbestimmung im Frontend;
- Runtime liest nur gespeicherte Zielkanten;
- kein Frontend-HTTP;
- keine neue Frontend-DB-Abfrage;
- keine erfundene Zuordnung bei Mehrdeutigkeit.

Der historische Satz „nur Ziel-URL“ aus `protocol/AFFILIATE_BANNER_TARGET_URL_KISS_20261006.md` ist damit für die **Import-Evidenzgewinnung** superseded. Der KISS-Runtime-Vertrag „einmalig bestimmen → speichern → Runtime liest gespeicherte Karte“ bleibt bestehen.

## 4. Reihenfolge

Verbindliche Reihenfolge:

`Provider-Rohdaten vollständig erfassen → Herkunft/Integrität sichern → reale Ziel-URL samt Provenienz erfassen → Asset technisch prüfen → ERST DANACH Zuordnung`

Die spätere Zuordnung ist ein getrennter Schritt. Sie darf vor bestandenem Basis-Gate nicht weiter verändert oder optimiert werden.

## 5. Altbestand

Bestehende Banner aus 6.72.198 und älter dürfen nicht aus alten synthetischen Titeln oder veralteten, unvollständigen Payloads „repariert“ werden.

Sie müssen über den normalen echten Providerweg frisch eingelesen werden. Erst nach abgeschlossenem frischem Import darf der automatische Bannerbestand neu aufgebaut werden.

## 6. Pflichtnachweise der Basis

Bevor irgendein Installer oder Live-Test angefordert wird, müssen mindestens gemeinsam PASS sein:

1. Provider-Kategorie-ID wird über den belegten Kategorienendpunkt auf den echten Kategorienamen aufgelöst.
2. Vollständiger Provider-Rohdatensatz einschließlich verschachtelter Felder erreicht die Creative Library unverändert.
3. SHA-256 des gespeicherten Rohdatensatzes stimmt.
4. Echter Provider-Bannername wird erhalten, wenn vorhanden.
5. Fehlt ein echter Providertitel, wird kein synthetischer Titel als fachliche Provider-Evidenz erzeugt.
6. Tracking-URL und Ziel-URL-Provenienz bleiben erhalten.
7. Ein realistischer 6.72.198-Altbestand wird durch einen frischen Providerimport ersetzt, nicht durch Raten aus Altmetadaten.
8. Kein Provider-HTTP im Frontend.
9. Negativfall: fehlende/unverifizierbare Providerbasis bleibt fail-closed.
10. Danach vollständiger bestehender Affiliate-Gesamtworkflow/WordPress/MariaDB-Regressionslauf.

Kein PASS nur aus Codeansicht oder aus vorhandenen Testdateien.

## 7. Nicht wiederholen

- Keine weitere Banner-Zuordnungsregel bauen, solange die Importbasis nicht nachgewiesen ist.
- Keine Einzelbanner-Sonderreparatur als Systemlösung.
- Keine manuelle Fixed-Zuordnung als Ersatz für die automatische Basis.
- Keine synthetischen Titel/Kategorien als vermeintliche Provider-Evidenz.
- Keine lokale Fixture-Abnahme als Beweis für reale Providerdaten.
- Keine neue Version nur zur Symptomjagd.
- Kein Hoster-/OPcache-/Serververdacht ohne Beleg.
- Kein weiterer Nutzer-Klickauftrag, bevor die eigene Source-/Testseite vollständig geprüft wurde.


## 8. Bedienanforderungen – Tarifcheck, CHECK24 und händischer Bannerimport

Zusätzlich ausdrücklich vom Nutzer gebunden:

- **Tarifcheck** muss im Backend als eigener auswählbarer Direktpartner sichtbar sein, nicht nur indirekt über „Direktpartner“.
- **CHECK24** muss ebenfalls als eigener auswählbarer Direktpartner verfügbar sein.
- Für CHECK24 wird ohne belegten API-Vertrag **keine API erfunden**. Reale CHECK24-Banner werden über den bestehenden Direktpartner-/Manuellweg aufgenommen.
- Einzelne Banner müssen ohne Sammeldatei händisch erfasst werden können. Pflicht: reale Bild-URL und Tracking-Link. Optional: reale Ziel-URL, Titel, Beschreibung/Tags, Provider-ID sowie Breite/Höhe.
- Der händische Import benutzt dieselbe Creative Library, dieselbe technische Bildprüfung und dieselben gespeicherten Zielzuordnungen wie andere Banner.
- Diese Bedienerweiterung ändert **keine** Ranking-/Zuordnungsregel und hebt das offene Importbasis-Gate nicht auf.


- Tarifcheck und CHECK24 dürfen denselben bestehenden Direktpartner-Familienweg für **Versicherungen** bzw. **Kreditvergleich/Kosten** benutzen. Die Partneridentität bleibt getrennt; es wird kein CHECK24-API-Vertrag erfunden.

## 9. Verbindlicher KISS-Bannervertrag – Zuordnung, Format, Verteilung, Lebenszyklus

Nach erfolgreicher Importbasis gilt für die Bannerverarbeitung genau ein einfacher Vertrag:

1. **Tiefstes belastbares Ziel**
   - Jeder Banner wird beim Import/Reconcile genau der tiefsten belastbar bestimmbaren Portal-Kategorie zugeordnet.
   - Evidenzreihenfolge: reale/aufgelöste Ziel-URL -> echte Provider-Kategorie -> echter Bannername/-text.
   - Mehrdeutigkeit wird nicht geraten.
   - Für die gewählte Kategorie wird der vollständige Elternpfad desselben Strangs gespeichert.

2. **Ausspielung nur im eigenen Strang**
   - Ein zugeordneter Banner darf auf seiner tiefsten Kategorie und auf den gespeicherten Elternkategorien desselben Strangs erscheinen.
   - Er darf nicht in fachfremde Seitenzweige ausweichen.
   - Die Frontend-Runtime klassifiziert nicht neu; sie liest ausschließlich die gespeicherte Ziel-/Pfadkarte.

3. **Format vor Verteilung**
   - Zuerst muss der Banner den verbindlichen Slot-/Formatvertrag erfüllen; erst danach darf er in Auswahl oder Verteilung gelangen.
   - Für Glossar-Einzelartikel gilt weiterhin:
     - Desktop: Verhältnis 0,50 bis 1,50, Mindestbreite 310 px, max. 1,10 Upscale;
     - Mobil: Verhältnis 2,50 bis 12,00, Mindestbreite 300 px, max. 1,10 Upscale.
   - Unbekannte oder nur angenommene Maße sind kein Formatbeweis.

4. **Fallback-Verteilung**
   - Gibt es für ein Ziel keinen spezifisch passenden Banner, wird nur aus dem technisch und formatlich zulässigen allgemeinen aktiven Bannerbestand verteilt.
   - Die Verteilung muss stabil und gleichmäßig sein; nicht überall darf derselbe Banner gewinnen.
   - Bestehende deterministische Partner-/Creative-Verteilung wird wiederverwendet. Keine zweite Verteilungsmaschine.

5. **Vergleichsrechner**
   - Kredit-/Kreditvergleich-Banner werden auf **alle realen Kosten-Blattkategorien** gebunden.
   - „Kosten“ ist kein eigener Root-Ast. Maßgeblich ist: echte Blattkategorie und „Kosten“ im realen Kategorienpfad oder Slug.
   - Versicherungsbanner werden auf **alle realen Versicherungs-Blattkategorien** des vorgesehenen Versicherungsbereichs gebunden.
   - Tarifcheck und CHECK24 verwenden dafür denselben fachlichen Familienvertrag bei getrennter Partneridentität.

6. **Regelmäßiger Bestandabgleich**
   - Neue Banner werden über die bestehende Provider-Automation eingelesen, technisch geprüft und anschließend zugeordnet.
   - Nicht mehr gelieferte Banner werden nicht sofort gelöscht: erster vollständiger Fehlzyklus = Quarantäne, zweiter vollständiger Fehlzyklus = `inactive_missing` und automatische Kampagne deaktivieren.
   - Manuelle FIXED-Entscheidungen bleiben getrennt erhalten.

7. **Performance-/Datenbank-Hardlock**
   - Kein Provider-HTTP im Frontend.
   - Keine neue Frontend-DB-Abfrage für Zielbestimmung oder Verteilung.
   - Keine Ziel-/Text-/URL-Neuklassifikation im Frontend.
   - Reconcile ausschließlich im Hintergrund in kleinen Batches mit hartem Zeitdeckel.
   - Keine neue Tabelle oder zweite Bannerarchitektur, solange die vorhandene Creative Library und gespeicherte Zielkarte ausreichen.

Kurzform:
`Import -> technisch prüfen -> tiefstes Ziel bestimmen -> Elternpfad speichern -> Format prüfen -> passende Banner wählen -> sonst stabil verteilen -> Bestand regelmäßig nachziehen`.

## 10. Verbindlicher KISS-Vertrag – Tarifrechner/Widget im Beitrag

Dieser Punkt ist fachlich getrennt von der Banner-Zuordnung.

- Ein Rechner wird zentral unter `Affiliate-Zentrale -> Tarifrechner` mit stabiler ID, aktiv/inaktiv und vertrauenswürdigem HTML-/Widget-Code verwaltet.
- Der Beitrag enthält ausschließlich den stabilen Platzhalter `[affiliate_rechner id="<id>"]`.
- Eine gültige ID bedeutet: derselbe Schlüssel existiert in der zentralen Rechnerliste, der Rechner ist aktiv und sein gespeicherter HTML-/Widget-Code ist nicht leer.
- Bei einem normalen klassischen Beitrag muss WordPress diesen Platzhalter beim Rendern durch genau den aktuell zentral gespeicherten Rechnercode ersetzen.
- Umbenennen ändert die stabile ID nicht. Inaktiv, gelöscht, unbekannt oder leer bleibt fail-closed mit leerer Rechnerausgabe.
- Die Sichtbarkeit des Rechners hängt **nicht** von Banner-Zielkarte, Banner-Kategorie, Banner-Ranking oder Banner-Reconcile ab. Ein Bannerfix ist kein Ersatz für einen funktionierenden Rechner-Shortcode.
- KISS/Performance: keine neue Tabelle, keine Artikelmutation, kein Provider-HTTP; die bestehende nicht-autoloadende Rechneroption und der Request-Cache bleiben der einzige Speicher-/Leseweg.

Kurzform:
`zentraler Rechner -> stabile ID -> Platzhalter im Beitrag -> Shortcode rendert zentralen Code`.



## 11. Verbindlicher KISS-Pflegevertrag – Aufräumen und Vereinfachen ohne Funktionsumbau

Nutzerentscheidung 08.10.2026:

Das funktionierende Affiliate-System wird **nicht neu gebaut und nicht fachlich umstrukturiert**. Aufräumen bedeutet ausschließlich: Altlasten entfernen, Bedienung vereinfachen und unnötige Dauerlast reduzieren, soweit dabei kein funktionierender Prozess verändert wird.

Verbindlich:

- Neue Banner bleiben im bestehenden automatischen Provider-/Importweg. Standard-Automation bleibt der bestehende 2-Wochen-Zyklus; ein manueller Start ist nur für sofortige Synchronisation nötig.
- Bestehende technische Prüfung, Zielzuordnung, Materialisierung, Ranking, Verteilung und Renderer bleiben erhalten.
- Bestands-Rückversicherung bleibt zweistufig: erster vollständiger Fehlzyklus = `quarantine_missing`; zweiter vollständiger Fehlzyklus = `inactive_missing` und nur die automatische Kampagne wird deaktiviert. Manuelle FIXED-Entscheidungen bleiben erhalten.
- Der separate Health-Check bleibt als zusätzliche technische Rückversicherung erhalten.
- Backend: normale Bedienoberfläche so klein wie möglich; historische/Spezialseiten dürfen aus der sichtbaren Navigation verschwinden, solange notwendige Direkt-/Interneinstiege erhalten bleiben.
- Technische Routing-/Aktivierungsdetails müssen nicht in der normalen KISS-Oberfläche erscheinen, wenn sie intern weiterhin vollständig erhalten sind.
- Alte Recovery-Optionen/-Cronzustände dürfen durch das bestehende bounded Housekeeping entfernt werden, sobald sie obsolet sind.
- Dateien, Recoverydaten oder Kompatibilitätspfade dürfen **nicht** gelöscht werden, solange ein aktueller Runtime-/Incident-Fallback sie noch referenziert.
- Keine neue Tabelle, keine neue Frontend-DB-Abfrage, kein Frontend-HTTP und keine zweite Automations-/Health-/Verteilungsarchitektur für reine Aufräumarbeit.
- Ein bestehender möglicher Performance-Hotspot darf nicht im Rahmen „Aufräumen“ durch einen neuen Prozess ersetzt werden. Prozessänderungen brauchen einen eigenen belegten Auftrag.
- Datenbankpflege bleibt bounded und darf aktive/offene Jobs, aktive Providerdaten, veröffentlichte Ausgaben oder manuelle Freigaben nicht löschen.

Kurzform:

`Funktionierenden Prozess einfrieren -> nur sichtbare/tote Altlasten entfernen -> vorhandenes Housekeeping/Health nutzen -> Performance messen -> keine Architekturänderung`.


## 12. Verbindlicher KISS-Vertrag – allgemeine Affiliate-Textlinks mit Platzhaltern

Nutzerentscheidung 08.10.2026:

Textlinks sind **kein Banner-Sonderfall und keine LeadAlliance-Sonderarchitektur**. Sie werden allgemein für beliebige Affiliate-Partner nach demselben zentralen Platzhalterprinzip wie Tarifrechner verwaltet.

Verbindlich:

- Textlinks werden zentral im bestehenden Rechner-/Platzhalterbereich verwaltet.
- Pro Textlink werden mindestens Partner/Programm, interne Bezeichnung und aktiv/inaktiv gespeichert. Für die Ausgabe gilt genau eine von zwei Eingabeformen: **(A)** vollständiger vertrauenswürdiger Original-Partnercode oder **(B)** sichtbarer Linktext plus Affiliate-/Tracking-Link. Eine reale Ziel-URL darf optional nur zur Dokumentation gespeichert werden.
- Der Beitrag enthält ausschließlich den stabilen Platzhalter `[affiliate_textlink id="<id>"]`.
- Der Schreibchat darf nur vorhandene aktive Platzhalter verwenden und niemals Affiliate-URLs oder Textlink-IDs erfinden.
- Ein aktiver Platzhalter rendert ausschließlich den zentral gespeicherten sichtbaren Linktext mit dem zentral gespeicherten Tracking-Link.
- Inaktiv, gelöscht, unbekannt, leer oder ungültig bleibt fail-closed mit leerer Ausgabe.
- Ausgabe erfolgt als normaler Affiliate-Link mit `rel="sponsored nofollow noopener"`; keine automatische Keyword-Verlinkung.
- Keine Bildprüfung, Bannerformatprüfung, Banner-Slots oder Banner-Ranking für Textlinks.
- Keine neue Tabelle, kein neuer Cron, kein serverseitiger Frontend-HTTP-Aufruf, kein neuer Provideradapter und keine zweite Textlink-Automationsarchitektur. Bei vollständigem Partnercode dürfen vom Partner bewusst gelieferte Browser-Ressourcen wie Tracking-Pixel Bestandteil der Ausgabe sein.
- Speicherung erfolgt in einer kleinen nicht-autoloadenden zentralen Option mit Request-Cache; normale Seiten ohne Textlink-Platzhalter laden diese Daten nicht.
- LeadAlliance ist lediglich ein möglicher erster Partner dieses allgemeinen Textlink-Systems und wird nicht fest in die Architektur codiert.

Kurzform:

`zentralen Textlink anlegen -> vollständigen Partnercode ODER Linktext+Tracking-URL speichern -> stabile ID -> Platzhalter im Beitrag -> Shortcode rendert die aktuelle aktive Partnerausgabe`.
