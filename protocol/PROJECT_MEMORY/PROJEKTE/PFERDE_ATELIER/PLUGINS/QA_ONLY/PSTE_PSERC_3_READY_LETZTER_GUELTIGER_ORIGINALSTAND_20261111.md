# KISS – letzter originalsignierter Dreierplan gesichert; leeren aktuellen Plan nicht überschreiben (11.11.2026)

**Wiederhergestellte Quelldatei (original, nicht neu generiert):** vom 10.11.2026 15:47:48 UTC, PSERC 0.28.61, drei READY, keine WordPress-Schreiboperationen. Datei SHA256: `29638fef9606925b5b6f322fcde695581999ec0c41bd111bca0bcb655fbf1220`.

**Fünf-Felder-Übergabe original:** `PSERC_TEXTMACHINE_METADATA_BATCH_V2`, drei Positionen, SHA256 der Quelldatei `d943ebe3ab65ca53de04b54aca02321c1b2052b3e30e40ab6ff4d5a4cc9b22c9`. Der innerhalb der Original-Gesamtdatei enthaltene Batch ist inhaltlich identisch.

**Original-PHP-Abnahme durchgeführt:** `PSERC_Stable_Json::hash` reproduziert Original-Manifest-Signatur; `PSERC_Metadata_Boundary::validateBatch` meldet `PSERC_METADATA_BOUNDARY_PASS`; `PSTE_Intent_Profile::verifiedPreTypeForRaw` bestätigt die signierten PRE_TYPE-Suchprofile **alle 3/3** und `primary_user_goal=INFORMATIONAL_FOCUS`; alle drei Items ursprünglicher Status `READY_FOR_METADATA_HANDOFF` und `release_decision.ready=true`, jedes Original-Item passt zu seinem Batch-Metadatensatz. Die PHP-Quellklassen wurden unverändert aus den bereits geprüften Paketen ausgeführt.

**Drei Originaltitel:**
1. Horseware-Regendecken und ihre Unterschiede bei Schnitt und Ausstattung
2. Kombinierte Fliegen- und Regendecken für Pferde sinnvoll nutzen
3. Regendecken ohne Füllung für Pferde richtig einsetzen

**Eigens erzeugtes, nur lesendes Sicherungsarchiv**: `Pferdeatelier_3_Artikel_Originalstand_2026-11-10.zip`, 15460 Bytes; SHA256 `3148414adb7afce4435aa49ff8c95a1f0b56b7364e9b1bdf862ea3e9e1484e27`; enthält unveränderte originale Vollplan- und Fünf-Felder-Exportbytes sowie PHP-Prüfreport und ausdrückliche Begrenzung. Im persistenten Pluginbüro `/pferdeatelier/PLUGINS/QA/PFERDEATELIER_3_ARTIKEL_ORIGINALSTAND_20261110_NUR_SICHERUNG.zip` und `PFERDEATELIER_ORIGINALSTAND_3_ARTIKEL_VERIFIZIERT_20261111.json`.

**Nicht mit einem voll abgeschlossenen SEO→K0-Produktionslauf verwechseln**: Der ursprüngliche Vollplan heißt bewusst `ohne-suchintent-nachweis`: Die signierten Profile sind `PRE_TYPE`, kein in der Originaldatei fertig vorliegendes `BOUND_TYPE`. Die vorhandene original signierte Fünf-Felder-V2-Datei ist ein gültiger historischer *Metadatenexport*, kein aktueller K0-Freigabenachweis. Fehlende finale Suchintent-Bindung NICHT künstlich ergänzen. Der nach dem 11.11.-Neulauf aktive leere PSERC-Plan bleibt auf der WP-Testseite real leer, eine ZIP-Sicherung ersetzt ihn nicht. Keine Auto-Importfreigabe, keine K0-Aktion.

**Weiterer KISS-Arbeitsstand:** Nur noch den ursprünglichen Drei-READY-Nachweis über den **bestehenden** PSTE→PSERC-Handoff ohne vollständige Neuberechnung an aktuellen Test-WordPress-Kontext binden, mit exaktem `BOUND_TYPE`-Nachweis für die bereits bekannten drei Quellen und **vor Aktivierung** hart verhindern, dass ein neuer `0 READY`-Plan den letzten gültigen überschreibt. Nicht wieder 5.000 Datensätze bewerten, nicht DataForSEO starten, keine Kleinstplugins, K0 unangetastet. Das ist ein Konzept / offene Implementierung, KEIN erledigter WordPress-Fix.

**Stand:** `THREE_HISTORICAL_SOURCE_ARTIFACTS_AND_SIGNATURES_VERIFIED`, `ACTIVE_WP_ZERO_READY_STILL_OPEN`, `NO_PLUGIN_CHANGES`, `NO_K0_IMPORT`.
