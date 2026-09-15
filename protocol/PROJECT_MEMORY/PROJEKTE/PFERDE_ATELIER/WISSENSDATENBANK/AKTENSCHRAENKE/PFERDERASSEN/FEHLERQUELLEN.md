# PFERDERASSEN – AUTORITATIVE FEHLERQUELLE

STAND: 2026-09-15
STATUS: AKTIV / BLOCKED

Diese Datei ist die einzige ausführliche aktuelle Fehlerquelle für den Pferderassen-Aktenschrank. Das zentrale `FEHLERREGISTER.md` bleibt nur Wegweiser.

## PR-BREED-001 – Letzter 13er-Artikelbatch: Rassengruppen nicht autoritativ getragen

STATUS: OFFEN / BLOCKIERT ARTIKEL-PASS

Der Schreibvertrag erlaubt `rassengruppe_slug` nur, wenn `typ`/`rassegruppen` des gebundenen WDB-Datensatzes eine der sechs Managergruppen eindeutig trägt. Bei Mehrdeutigkeit darf nicht geraten werden.

Der im Chat erzeugte Batch `pferderassen_FINAL_13_manager022.json` enthält für alle 13 Artikel eine manuell abgeleitete Sechs-Gruppen-Zuordnung, obwohl die frisch gelesenen Datensätze diese Zuordnung nicht eindeutig als eine der sechs Managergruppen ausweisen:
- `breed-akhal-teke` → ausgegeben `vollblueter`; Datensatz: orientalisches Reitpferd / Ausdauerpferd;
- `breed-anglo-arabian` → `vollblueter`; Datensatz: Sportpferd / arabisch-vollblütige Kreuzungsrasse;
- `breed-caballo-deporte-espanol` → `warmblueter`; Datensatz: Sportpferd;
- `breed-hackney` → `warmblueter`; Datensatz: Fahrpferd / Showpferd;
- `breed-henson` → `robust-landrassen`; Datensatz: Freizeitpferd / französische Rasse;
- `breed-hispano-arabian` → `vollblueter`; Datensatz: iberisch-arabische Kreuzungsrasse / Sport- und Gebrauchspferd;
- `breed-irish-cob` → `kaltblueter`; Datensatz: Cob / Fahr- und Reitpferd;
- `breed-knabstrupper` → `warmblueter`; Datensatz: Reitpferd / Spezialrasse;
- `breed-leonharder` → `warmblueter`; Datensatz: Reit- und Freizeitpferd / Kompositrasse;
- `breed-slovak-trotter` → `vollblueter`; Datensatz: Traber / Rennpferd;
- `breed-trotador-espanol` → `vollblueter`; Datensatz: Traber / Rennpferd;
- `breed-trotteur-francais` → `vollblueter`; Datensatz: Traber / Rennpferd;
- `breed-waler-horse` → `robust-landrassen`; Datensatz: Arbeitspferd / Heritage breed / Reit- und Fahrpferd.

FOLGE:
Der 13er-Batch ist trotz technischer JSON-/Strukturprüfung **nicht als Schreibvertrags-PASS** gültig. Vor einer fachlichen Freigabe muss für diese Identitäten eine autoritative Zuordnung zu den sechs Managergruppen ergänzt oder das Sechs-Gruppen-Modell verbindlich erweitert werden. Keine erneute Ratzuordnung.

## PR-BREED-002 – Veröffentlichungsbestand enthält doppelte WDB-IDs

STATUS: OFFEN / WORDPRESS-DIREKTREADBACK ERFORDERLICH

Rekonstruktion aus dem WordPress-Export vom 15.09.2026 plus den danach veröffentlichten Batchdateien ergibt:
- 196 veröffentlichte `pa_breed`-Posts;
- 194 eindeutige `_prm_source_id`;
- doppelt: `breed-pantaneiro` und `breed-posavje-horse`, jeweils zweimal.

Die Rekonstruktion ist ein harter Dateibeleg, aber noch kein direkter aktueller WordPress-Datenbank-Readback. Deshalb keine automatische Löschung und keine Behauptung, welcher Doppelpost kanonisch bleiben soll.

NEXT:
Direkt in WordPress beide IDs auslesen, beide Posts/Slugs/Inhalte/Batches vergleichen und erst dann den nichtkanonischen Doppelpost kontrolliert bereinigen.

## PR-PLUGIN-001 – Relationslogik / Frontend-Regressionskette

STATUS: 0.2.7 LOKALER KANDIDAT / LIVE OFFEN

Historische Fehler dieses Chats:
- 0.2.2: `Ähnliche Rassen` wurden lediglich aus derselben Rassengruppe befüllt; dadurch semantisch identisch mit `Zur gleichen Rassengruppe`.
- 0.2.3: Same-Group-Ausschluss eingeführt, vorhandene alte Relationen aber nicht zuverlässig ersetzt; Frontend zeigte weiter identische Karten.
- 0.2.4: `get_post_metadata`-Filter rief innerhalb des Filters erneut `get_post_meta()` auf dasselbe Feld auf → echte Rekursion / Frontend-Endlosladen.
- 0.2.5: Rekursionsfilter entfernt, aber kompletter Relations-Neuaufbau blieb an `init`/Aktivierung gebunden → teurer Vollbestandlauf im Frontend / erneutes Endlosladen.
- 0.2.6: Frontendarbeit entfernt und ein Snapshot eingeführt; Abschlussprüfung entdeckte jedoch, dass Snapshot-Zeilen nach `source_id` kollabierten. Bei den real vorhandenen Doppel-IDs wurde je ein Post nicht repariert, obwohl `ok=true` zurückkam.

Aktueller Kandidat 0.2.7:
- jeder veröffentlichte Post bleibt separat nach `post_id` im Reparaturlauf;
- Relationskandidaten bleiben als eindeutige WDB-Identitäten geführt;
- Doppel-IDs werden gewarnt, nicht verschluckt;
- Same-Group- und Self-Hardlock bleiben;
- Backfill nur explizite Backend-Aktion;
- kein `get_post_metadata`-Filter;
- lokale 196-Post-Positiv-/Negativ-/Mutationstests PASS.

OFFEN:
WordPress-LIVE-Test nach Installation 0.2.7. Bis dahin kein LIVE-PASS und kein Plugin-CURRENT-Sync.
