# DataForSEO-Gate-Vertrag V1.6.1

## Rolle
DataForSEO liefert Evidenz und Lückensignale. Architektur-Owner bleibt Chat/Master unter bindendem Master. DataForSEO darf keine Kategorie autonom anlegen, löschen, verschieben, zusammenführen oder umbenennen.

## Endpoints
- `/v3/appendix/user_data` – Verbindungstest.
- `/v3/dataforseo_labs/google/keyword_ideas/live` – Global-/Cluster-Discovery.
- `/v3/dataforseo_labs/google/keyword_overview/live` – exakte Namen/Primärkeywords.

## Kosten- und Freigabesperren
- Verbindungstest: 0 Keyword-Recherche.
- Global-Preflight: 0 Requests und nur nach gültiger Erst-Sichtfreigabe.
- Global-Coverage: genau 1 bestätigter Paid Call.
- Detail-Preflight: 0 Requests und nur nach gültiger Global-Gap-Sichtfreigabe.
- Detailresearch: genau 1 Keyword-Ideas-Call je Cluster + notwendige Overview-Batches.
- Finalprüfung: 0 Provider-Requests.

## Global-Coverage
Jeder ausgewählte relevante Core muss vor Detailresearch endgültig einen der Zustände haben:
- im korrigierten Draft abgedeckt;
- MAIN_TOPIC;
- SUBTOPIC;
- ARTICLE_ONLY;
- OUT_OF_SCOPE.

`DEFERRED` ist ein temporärer Zustand und blockiert Detailresearch.

## Detail-Coverage
Relevante unbesetzte Cluster-Cores benötigen Owner, ARTICLE_ONLY oder EXCLUDED. `DEFERRED` blockiert READY/FINAL.

## Longtails
Finales Content-Blatt: mindestens 3 reale, node-gebundene DataForSEO-Longtails. Doppelte Ownership oder Kollision mit Primärkeywords anderer Knoten = BLOCK.
