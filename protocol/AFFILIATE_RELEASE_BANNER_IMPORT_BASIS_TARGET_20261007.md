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

