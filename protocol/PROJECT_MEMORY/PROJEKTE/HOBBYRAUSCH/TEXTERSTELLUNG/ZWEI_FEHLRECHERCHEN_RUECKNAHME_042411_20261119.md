# 19.11.2026 – Hobbydepot 0.4.24.11: Zwei Fehlrecherchen gezielt zurücknehmen

## Bewiesener Zustand
Nutzerdiagnose `texterstellung-diagnose-20261119-125014.json` in echter WordPress-Installation 0.4.24.10: **Automodellbau** ist `COMPLETE` / `ANALYZED_NO_ELIGIBLE_CANDIDATE`, 100 Rohkeywords, 89 Kandidaten, 0 PASS, 85 NO_MATCH, davon viele Hobby-Wohnwagen/Tier-Hobby-Daten; **production** = `api.dataforseo.com`. Vorige Diagnose `texterstellung-diagnose-20261119-114324.json`: **3D-Bogenschießen** ist `COMPLETE`, 9 Kandidaten, 0 PASS, ursprünglich Sandbox-Responses zu Pizza/Telefon. Screenshot vom 19.11. 13:50: **377 offen, 2 recherchiert**.

**Weitere echte Ursache im alten PHP bewiesen:** `PSTE_Category_Context::researchContext("Automodellbau", ..., "Hobby Depot")` in 0.4.24.10 erzeugt `effective_seed="Automodellbau Hobby"`. Quelle und Test belegen die automatische Beifügung des generischen Website-Worts. Dies entspricht dem Suchdatenbild, beweist aber nicht jeden einzelnen Fremdtreffer.

## Exakt ein KISS-Release
- `Texterstellung_Hobbydepot_0.4.24.11_ZWEI_RECHERCHEN_ZURUECKNEHMEN.zip`
- SHA256 `f7e5a5e03100af5dc7c7921886716c584b429fd303202fc9112869323b9e0280`, **509989 Bytes**. Root identisch `texterstellung-hobbydepot/`, WP-Hauptplugin-Version **0.4.24.11** > 0.4.24.10.
- **84/87 Dateien byteidentisch.** Nur drei bestehende Quelldateien geändert: `texterstellung.php` (Adminaktion/Anzeige/Versionsnummer), `original/pste/includes/class-pste-repository.php` (eine atomare gesicherte Statusrücknahme in bereits zuständigem Repository), `original/pste/includes/class-pste-category-context.php` (für neue Hobbydepot-Suchen nur exakten ursprünglichen Hobbybegriff an Anbieter, keinen Portalnamen).
- Auf dem **bereits vorhandenen** Menü `Texterstellung → Recherche` gibt es eine kleine aufklappbare Sektion `Die beiden Fehlrecherchen zurücknehmen` und **EINEN** Button `Beide Fehlrecherchen zurücknehmen (kostenlos)`. Nur sichtbar, solange mindestens 2 Kategorien als `ANALYZED` markiert sind.
- Rücknahme erfordert **exakt** zwei eindeutige heutige Familien aus Baseline `3D-Bogenschießen` und `Automodellbau`; **je genau ein** originaler gespeicherter Run mit Status `ANALYZED_NO_ELIGIBLE_CANDIDATE`, entsprechender Kategoriebindung und **9/89 BLOCKED**, **0 PASS**; keine laufende Queue, kein aktiver Forschungsjob. Abweichung = **kein Write**.
- Ein gemeinsamer Datenbanktransaction setzt **nur je ein Statusfeld** der beiden Original-Research-Runs auf `RETRACTED_NO_ELIGIBLE_CANDIDATE`. Damit erkennt Original `PSTE_Repository::categoryProgress()` **beide wieder als `NOT_ANALYZED`** und `PSTE_Breadth_Research_Queue::openFamilies()` bietet beide wieder als offene Kategorien an. Beide oder keiner, kein Halbzustand.
- **Keine Löschung der ursprünglichen Ergebnisse.** Die Rohkeywords, die 98 alten Kandidaten, Source-Rechts-/Kostenbelege, Originaljobs und signierte Queue bleiben als Verlauf im Speicher. UI zeigt alten letzten Run als **`ZURÜCKGENOMMEN (ARCHIV)`** und kennzeichnet gespeicherte Originaldaten ausdrücklich einschließlich historischer. Ohne Löschung/keine neuen DataForSEO POSTs, keine zweite Entscheidung. **Die beiden Abschlüsse werden zurückgenommen, nicht physisch sämtliche Alt-Daten gelöscht.**
- Beim Installieren und Zurücknahme-Klick keinerlei kostenpflichtige Datenrecherche; **für spätere neue Recherche weiter separat vorhandener `cost_ack`**. Alte gesperrte Kandidaten bleiben gesperrt und werden nicht pauschal freigegeben. K0/Multi/PSERC unberührt.

## Testbelege
- **47/47** reale Repository-PHP-Mockprüfungen mit transienter Datenbank und Originalfunktionen (Status-Reopen, ursprüngliche Originaldaten intakt, `categoryProgress` zweimal offen, 13 Negativfälle einschließlich Rollback beim zweiten DB-Write, anderer Eigentümer, veränderte 9/89, PASS, laufender Job, zweite Aktion, kein Anbieterauftrag).
- **20/20** originale `PSTE_Category_Context::researchContext()`-Tests mit fünf verschiedenen Hobbybegriffen und Pfaderhaltung.
- **20/20** Productivmodus- und WordPress-UI-Simulation; **38/38** echte DataForSEO-PAA-ID-Klassenprüfungen; **31/31** Archiv-/Fortsetzungs-Tests. Zusammen **156 lokale PASS**, PHP 78/78, JSON 8/8, ZIP CRC 87/87, 84/87 Originaldateien identisch.
- **Keine WordPress/MySQL-Liveausführung in diesem Schritt**. Realer DB-Status wird erst durch den Admin-Klick verändert. Bei einer unerwarteten Live-Abweichung verweigert das Plugin die Rücknahme.

## Gesicherte Ablage / Benutzerweg
Library-Upload erfolgreich in **`/Hobby Depot/Plugin-Büro/`** und `/hobbydepot/TEXTERSTELLUNG/INSTALLATIONSKANDIDATEN/` sowie Current-/Prüfberichte (MD+JSON).
**Backup → ZIP 0.4.24.11 in WordPress über bestehendes Plugin ersetzen → `Texterstellung → Recherche → Die beiden Fehlrecherchen zurücknehmen → Beide Fehlrecherchen zurücknehmen (kostenlos)` EINMAL.** Erwartet 379 offen/0 recherchiert, falls keine weiteren Recherchen seit screenshot. Danach gezielt `3D-Bogenschießen` und `Automodellbau` in **Bestimmte offene Kategorien auswählen** sichtbar. Neue Recherche **nicht** automatisch gestartet; wieder kostenpflichtig mit ausdrücklichem Haken.
