# Pferdeatelier eBay – Zielvertrag/Fehlerhistorie und Gesamtworkflow-Abnahme
Datum: 10.11.2026. **Dokumentation / QA, keine neue Pluginfreigabe und kein WordPress-Eingriff.**

## Verbindlicher Zielvertrag (bereits bekannt, NICHT neu erfunden)
Ein Importweg und kanonischer eBay-Worker, verbindliche Speicherung, ein gemeinsamer Auswahl-/Zuordnungsweg, streng belegte Produktzuordnung je Familie, bestehende letzte sichere öffentliche Ausgabe schützen, überprüfte Live-Produktausgabe auf der konkreten Produktseite. Nur tatsächlich noch fehlende Warenfamilien gezielt bearbeiten; keine unbegrenzten Vollsuchen. KISS: keine neue Tabelle, kein zweiter Worker/Frontend-DB, keine Änderungen an Amazon/idealo/K0/anderen Portalen.

## Historie und wiederholte Ursachen (keine Doppelarbeit)
- 308: Ausgangsquelle, nicht mit GitHub-Current verwechseln. 311/312: BUSINESS-only und Fortschritts-/Wiederanlauf-Fix. 313/314: übereinstimmende Startfreigabe und korrekt dargestellter Status. 315: getrennte Zähler und CSV aller fehlenden Familien. 316: gezielte Nachsuche. 317: einzeln geprüfte Mehrfachzuordnungen. 318: Stopp/Fortsetzen. 319: eigener Bestands-Nachlauf ohne eBay-API.
- Vorbekannt, nicht erneut als neue Ursache ausgeben: sechs Stunden Quellenfrist vs. stundenlange Verarbeitung; falsche 0/298-Anzeige für neuen Teilplan; zu allgemeine Suchwörter; Dubletten pro eBay-Artikel; irreführende grüne Teilphasen.
- Historische Testpakete sind vor allem PHP/WordPress-Mocks. Erfolgreiche Hunderte von Simulationsschritten sind **KEIN** Beweis für Live-Import, MariaDB-Veröffentlichung oder Sichtbarkeit auf echten Seiten.

## Am 10.11.2026 erneut nachgelesene Belege
- Physische Original-Test-ZIP 319, SHA256 b404e613036942e1e83d3739bc9b01bc06631b5df343c3fe779450a46a2ae5ef, 66 Dateien, 23 PHP-Lint PASS.
- Echte 319-Quellstellen: `trait-ppar-ebay.php`: `ebay_local_reuse_key/state/guard/start/one/tick` ab ca. Zeile 10451; `trait-ppar-ebay-run.php`: `ebay_run_save` ca. 631. Die Zusatzfunktion speichert unter eigener WP-Option `ppar_ebay_local_reuse_v319` mit eigenem Start/AJAX-Tick. **Das ist ein zweiter Bearbeitungsweg neben dem kanonischen Workflow und verletzt das Ein-Weg-Prinzip.**
- In 319 liefert `ebay_local_reuse_start` trotz verweigertem `update_option` einen `status=running` zurück; auch `ebay_run_save` gibt bei verweigerter Speicherung ohne Readback ein Array zurück. Vorher/Nachher-Eigensimulation `ebay319_gesamtabnahme_proben.php` reproduziert diese **false-success**-Pfadabweichung. Wichtig: Ein `update_option(false)` allein beweist im echten WP keine Datenbankstörung, da auch unveränderte Werte `false` liefern können. Korrekt ist eine nachfolgende Zustandsprüfung.
- Die Admin-JS-Fehlermeldung `Speichern fehlgeschlagen` wird auch verwendet, wenn AJAX keine strukturierte JSON-Antwort gibt; sie **beweist nicht** die technische Ursache des gescheiterten WordPress-Aufrufs. Der Screenshot 10.11., 09:44, beweist nur: Die gewünschte Aktion ist nicht erfolgreich angelaufen.
- Ein Quell-Audit ergab 298 Pflichtfamilien nach 26 Nicht-Waren-Ausschlüssen aus 324; 28 weitere Sammel-/Baubegriffe bleiben fachlich prüfbedürftig und werden **nicht** ohne Beleg entfernt.
- Nutzerbeleg 09.11. nach sicherem Anhalten: `paused`, gespeichert 114/298, 211 offen. Lauf **nicht** ohne Freigabe fortsetzen oder neu starten.
- Altprüfungen tatsächlich mit 319-Quellkopie erneut ausgeführt: 49 Original-Verhaltenschecks, 333 kanonische Orchestrator-Simulations-Assertions, 17 HTTP-Fälle, 5 Frontend-Quellgate-Fälle, 25 Gate-Assertions, 38 Start-Assertions, 43 Status-Assertions, Bootstrap-Hooks, 23 PHP-Lints PASS. Zusätzlich originalbasierter 319-Schreibfehler-Reproduktionstest 7/7 PASS (diese sieben **bestätigen den vorhandenen Fehler**, keine Freigabe).
- Die alten Tests sind vorwiegend Mocks; ein echtes End-to-End auf installiertem WordPress mit echter eBay-API und veröffentlichter Seite fehlt. **Kein Release-PASS, keine produktive Freigabe.**

## Einzige sinnvolle Reparaturlinie
1. **Eine kanonische Quelle der Wahrheit:** Zusatz-319-Start/Option nicht als zweites Produktionsverfahren weiterführen. Bereits gespeicherte Ergebnisse über den bestehenden kanonischen Ablauf verwenden und sicher am gespeicherten Checkpoint fortsetzen.
2. **Keine unnötige API-Abfrage:** Vor jedem neuen eBay-Suchlauf gesicherte Angebote für die offene Familie einzeln prüfen. Externe Nachsuche nur für anschließend offene Fälle; kein erneuter Vollkatalog. Sicherheits- und Anbieterprüfungen beibehalten.
3. **Atomarer Fortschritt:** Jeder neue Eintrag und jeder Wechsel des Checkpoints wird rückgelesen. Kein „läuft/erledigt“ ohne nachweisbar gespeicherten Zustand. Verweigerte Speicherung stoppt den betreffenden Schritt und liefert den echten Fehlercode.
4. **Einzelbeweis pro Familienzuordnung:** Artikelnummern-Dubletten dürfen neue fachlich gültige Familienzuordnungen nicht verhindern; vorhandene Verknüpfungen und veröffentlichte Last-Known-Good-Karten dürfen nicht verloren gehen.
5. **Öffentliche Endabnahme:** Nur tatsächlich veröffentlichte, aus dem gültigen eBay-Angebot stammende Produktkarten auf der **richtigen konkreten Produktseite** zählen. Separat ausweisen: öffentlich versorgt, vorhandene Treffer fachlich abgelehnt, kein Treffer im geprüften Suchraum, technische Probleme, weitere Auffrischung notwendig.
6. **Alltagstaugliche Bedienung:** Start/Stopp/Fortsetzen am selben Laufstand; Zeit-/Paketlimit, echte Fehlergründe und Fortschritt; keine zusätzlichen Laufknöpfe. Der Nutzer darf den Browser schließen.
7. **Freigabe nur nach Gesamttest:** Tests mit echter WordPress-Options-/Datenbankpersistenz, fachlich geeigneten sowie absichtlich falschen Angeboten, Mehrfachfamilien, Wiederanlauf, 0-Treffer, API-Fehler, Endkontrolle öffentliches Produkt. Kein rein simulierter grüner Gesamt-PASS als Live-Beweis ausgeben.

## Konsequenz
Version 319 ist **nicht als Gesamtworkflow abgenommen**. Kein weiteres blindes 320-Minipatch und keine neue stundenlange eBay-Suche. Erst das Ein-Weg-Integrationsdesign gegen diese Liste abnehmen. Andere Portale bleiben unberührt. Dieses Dokument verhindert die Wiederholung der bereits archivierten Fehlerbefunde.
