# PFERDERASSEN – AUTORITATIVE FEHLERQUELLE

STAND: 2026-09-16
STATUS: **HISTORISCHE OFFENE BEFUNDE / NICHT AKTIVE NEXT ACTION**

Diese Datei ist die einzige ausführliche Fehlerquelle für den Pferderassen-Aktenschrank. Das zentrale `FEHLERREGISTER.md` bleibt nur Wegweiser. Den aktuellen Arbeitsauftrag ausschließlich aus `../../HOBBYRAUM.md` lesen.

## Nutzerentscheidung 2026-09-16

Der Nutzer hat ausdrücklich entschieden, die beiden Punkte `PR-BREED-001` und `PR-BREED-002` aus der aktiven Aufgabenliste zu streichen. Das bedeutet **nicht**, dass ihre technischen/fachlichen Befunde nachträglich als gelöst gelten. Sie bleiben hier historisch korrekt dokumentiert, sind aber keine aktuelle NEXT ACTION und blockieren den vom Nutzer gewählten nächsten Auftrag nicht.

## PR-BREED-001 – Letzter 13er-Artikelbatch: Rassengruppen nicht autoritativ getragen

STATUS: **OFFEN / VOM NUTZER AUS AKTIVER ARBEIT GENOMMEN 2026-09-16**

Der Schreibvertrag erlaubt `rassengruppe_slug` nur, wenn `typ`/`rassegruppen` des gebundenen WDB-Datensatzes eine der sechs Managergruppen eindeutig trägt. Bei Mehrdeutigkeit darf nicht geraten werden.

Der erzeugte Batch `pferderassen_FINAL_13_manager022.json` enthielt manuell abgeleitete Sechs-Gruppen-Zuordnungen, obwohl die WDB-Datensätze diese Zuordnung nicht eindeutig tragen:
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

Falls dieser Punkt später wieder aufgenommen wird: autoritative Zuordnung ergänzen oder Gruppenmodell verbindlich ändern; keine Ratzuordnung.

## PR-BREED-002 – Veröffentlichungsbestand enthält doppelte WDB-IDs

STATUS: **OFFEN / VOM NUTZER AUS AKTIVER ARBEIT GENOMMEN 2026-09-16**

Rekonstruktion aus WordPress-Export 15.09.2026 plus danach veröffentlichten Batches ergab:
- 196 veröffentlichte `pa_breed`-Posts;
- 194 eindeutige `_prm_source_id`;
- doppelt: `breed-pantaneiro` und `breed-posavje-horse`, jeweils zweimal.

Das ist ein Dateibeleg, kein kanonischer aktueller DB-Readback. Deshalb weiterhin keine automatische Löschung und keine Behauptung, welcher Doppelpost kanonisch wäre.

Falls dieser Punkt später wieder aufgenommen wird: beide IDs direkt in WordPress auslesen, Posts/Slugs/Inhalte/Batches vergleichen und erst dann entscheiden.

## PR-PLUGIN-001 – Relationslogik / Frontend-Regressionskette

STATUS: **CLOSED / 0.2.7 WORDPRESS-LIVE PASS**

Historische Fehlerkette:
- 0.2.2: `Ähnliche Rassen` = gleiche Gruppe;
- 0.2.3: vorhandene alte Relationen nicht zuverlässig ersetzt;
- 0.2.4: rekursiver `get_post_metadata`-Pfad → Frontend-Endlosladen;
- 0.2.5: Vollbackfill auf `init`/Aktivierung → Frontend-Endlosladen;
- 0.2.6: Doppel-IDs im Snapshot kollabiert;
- 0.2.7: jeder reale Post separat, Doppel-IDs gewarnt, Same-Group/Self-Hardlock, Backfill nur Backend, kein `get_post_metadata`-Filter.

Lokale 196-Post-Positiv-/Negativ-/Mutationstests PASS; WordPress-LIVE am 2026-09-15 vom Nutzer PASS bestätigt.
