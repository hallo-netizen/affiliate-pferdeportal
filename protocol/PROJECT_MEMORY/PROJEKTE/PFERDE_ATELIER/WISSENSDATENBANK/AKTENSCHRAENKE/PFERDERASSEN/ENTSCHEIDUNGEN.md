# PFERDERASSEN – DAUERHAFTE WAS/WARUM-ENTSCHEIDUNGEN

STAND: 2026-09-15
ROLLE: Fachliche Ergänzung zum campusweiten Änderungs-/Erklärungsregister; keine CURRENT-/Fehler-/Zielwahrheit.

## PA-BREED-REL-001 – Rassengruppe und ähnliche Rassen sind zwei verschiedene Beziehungen

WAS:
- `Zur gleichen Rassengruppe` kommt ausschließlich aus `pa_breed_group`.
- `Ähnliche Rassen` kommt ausschließlich aus strukturierten `_prm_related_source_ids`.
- Self-Relationen und jede Rasse derselben `pa_breed_group` sind bei `Ähnliche Rassen` hart ausgeschlossen.
- Es gibt keine zufällige Auffüllung ohne positives Ähnlichkeitssignal.

WARUM:
Der reale Frontendtest am Aegidienberger zeigte, dass die erste Relationsimplementierung exakt dieselben Rassen in beiden Modulen ausgab. Damit hatten die beiden Module keinen unterschiedlichen fachlichen Zweck.

ZIELQUELLE:
`ZIELVERTRAG_RELATIONEN.md`.

## PA-BREED-REL-002 – Relationsreparatur niemals im normalen Frontendpfad

WAS:
Vollbestands-Neuaufbau/Migration von Relationsdaten ist ausschließlich eine explizite Backend-Aktion. Kein Frontend-`init`, keine Aktivierungsreparatur und kein `get_post_metadata`-Filter darf einen Vollbestandslauf oder rekursiven Meta-Read auslösen.

WARUM:
0.2.4 erzeugte durch rekursiven Meta-Read reales Endlosladen. 0.2.5 entfernte die Rekursion, startete aber weiterhin den Vollbestandslauf im normalen Requestpfad und verursachte erneut Endlosladen. Wartungslogik muss deshalb außerhalb des Seiten-Renderpfads liegen.

ALLGEMEINER REGRESSIONSSCHUTZ:
`../../../PLUGINS/SYNC_VERTRAG.md` verlangt bei Laufzeitänderungen seit 2026-09-15 ausdrücklich den unveränderten Frontend-/Read-Pfad als Negativtest.

## PA-BREED-REL-003 – Stabile Fremd-IDs dürfen reale Doppelposts nicht still verschlucken

WAS:
Der Reparaturlauf hält jeden realen WordPress-Post separat nach `post_id`. `_prm_source_id` dient der fachlichen Zielidentität, darf aber nicht als Schlüssel verwendet werden, der mehrere reale Posts still auf eine Zeile reduziert. Doppelte WDB-IDs müssen sichtbar gewarnt und separat bereinigt werden.

WARUM:
Die Abschlussprüfung gegen den rekonstruierten realen Bestand fand 196 veröffentlichte Posts bei nur 194 eindeutigen `_prm_source_id`. 0.2.6 kollabierte die beiden Doppel-ID-Paare und meldete trotzdem Erfolg, obwohl je ein Post unrepariert bleiben konnte.

ALLGEMEINER REGRESSIONSSCHUTZ:
`../../../PLUGINS/SYNC_VERTRAG.md` verlangt bei Plugins mit stabilen/externalen Identitäten – soweit im realen Bestand möglich – Doppel-/Kollisions-Negativtests.
