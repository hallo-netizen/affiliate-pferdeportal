# HOBBYRAUSCH – PLUGINS – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-09-28
STATUS: HD-001 V1.8.8 PERSISTENT GUIDED FLOW BEREIT

## Rolle

Einzige aktuelle Zustandsautorität des Scopes `HOBBYRAUSCH_PLUGINS`.

## Aktueller belastbarer Stand

V1.8.8 ersetzt den manuellen Datei-Pingpong im normalen Kategorie-Ablauf durch einen persistenten serverseitigen Arbeitsstand.

Neu:
- DataForSEO-Verbindungs-PASS bleibt gespeichert, solange Credentials/Markt/Sprache unverändert sind;
- Zwischenpakete werden serverseitig gespeichert und intern wiederverwendet;
- normale Ansicht zeigt nur aktuellen Status und nächste Aktion;
- neue externe Korrekturdatei muss nur einmal übernommen werden;
- technische Alt-/Einzelwerkzeuge bleiben als Notfallansicht vorhanden.

Keine Research-, Qualitäts-, Review-, Deployment-, Readback-, Drift- oder Rollback-Funktion entfernt.

Tests:
- 229/229 PASS;
- Fresh-Unpack 229/229 PASS;
- Runtime PHP 17/17 PASS;
- Runtime-Parität 22/22 PASS.

## NEXT ACTION

V1.8.8 installieren und den bereits signierten Initial-Draft einmalig in den persistenten Arbeitsstand übernehmen. Danach Global-Coverage direkt aus dem gespeicherten Stand starten.
