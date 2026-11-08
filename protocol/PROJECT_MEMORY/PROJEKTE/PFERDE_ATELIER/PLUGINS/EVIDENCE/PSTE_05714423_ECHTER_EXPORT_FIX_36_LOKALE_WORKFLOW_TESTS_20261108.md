# PSTE 0.57.144.23 – IST-Fix, lokale Workflow-Simulation und klare Abnahmegrenzen (08.11.2026)

**STATUS: QA ONLY.** Der Nutzer hat bisher die **alten** PSTE 0.57.144.22 und PSERC 0.28.55 auf der WP-Testseite installiert. Die hier gebaute PSTE 0.57.144.23 wurde **nicht** in WordPress installiert oder gegen die echte WP-Datenbank ausgeführt. K0, Produktion, Seiten, Beiträge und aktive Dateien wurden nicht verändert. PR #682 bleibt Draft, ohne Merge.

## Ausgangsbasis – Originaldateien, keine Neuimporte

- PSTE: `PSTE-0.57.144.22-TEST.zip` (634.339 Byte, SHA256 `384203f4971fc6d98eaa7613835c75f2b1ff976471659afa8dae60ac09a08ad1`).
- PSERC: `PSERC-0.28.55-TEST.zip` (266.498 Byte, SHA256 `501959a0ac73a1b81070ed23623935999ed1058385b3ba587e0f8bef9c9816d0`), **unverändert**.
- Echte vom Nutzer gelieferte WP-Exportdatei 15:03:46 UTC: privat `/pferdeatelier/pferdeatelier-mini-ergebnisse-20261108-150347(1).json` (SHA256 `f31e68a5de77be965e384e4b7517ec7a48a7cd1ca8ae6631b9fb5637dd93a2ba`).
- Inhalt: 100 importierte Stichwörter (87 JA, 9 VIELLEICHT, 4 NEIN); 87 externe SEO-Subjekte; Parkhaus 1.179 Datenzeilen: WP 1.024, PSTE 1, neun alte Editorial-Einträge, PSERC 1, PPM679 144. Nach Screenshot wurde der vorhandene PSERC-Metadatensnapshot aktualisiert; Status dort PASS für Snapshot, **nicht** SEO-Freigabe.

## Nachgewiesene Fehler und im TEST korrigierte Ursachen

1. **Literal „Array“:** Sowohl beim Import bestehender Redaktionspläne als auch beim späteren Lesen wurden verschachtelte `title`-Werte mit einem gewöhnlichen String-Umwandlungsversuch zerstört. Neue PSTE-Logik liest ausdrücklich unterstützte verschachtelte Zeichenketten; wählt notfalls ein bereits in derselben Zeile gespeichertes eindeutiges Longtail-Thema; lehnt mehrdeutige Angaben vor Speicherung oder Export ab. Keine erfundenen Titel. Eingelesene Pläne liefern jetzt `status=AVAILABLE` statt trotz Inhalt `NOT_AVAILABLE`. Bereits zerstörte neun Datensätze mit nur noch dem Wort „Array“ **können NICHT aus dem gelieferten Export rekonstruiert werden** und werden deshalb sicher gesperrt.
2. **144 PPM679-Plätze ohne Titel:** Der Export hat bisher gespeicherte `post_id`-Zuordnungen ignoriert, obwohl derselbe Export bereits WordPress-Beitragstitel besitzt. Die neue Logik verknüpft diese ausschließlich anhand identischer numerischer `post_id` – **141 von 144 realen Fällen** sind damit ohne zusätzliche Datenquelle lösbar. Drei nicht im 1.024er-WP-Snapshot enthaltene Referenzen werden **nur einzeln über bestehendes WordPress `get_post`** gelesen (ohne Ganzseiten-Abfrage). Gibt es keinen nachweisbaren Titel, bleibt das gesamte Parkhaus bewusst `complete=false`; kein falsches FREI. Die drei fehlenden IDs aus dem wirklichen Export: 972356, 972414, 972560 (nur Prüfbelege, keine Annahme, sie existierten auf dem Server).
3. **Komplizierte Bedienung:** Das bestehende PSTE-Menü `Themenprüfung` zeigt im TEST jetzt den Normalablauf **Export → extern prüfen → Ergebnis importieren → Status** an erster Stelle; ältere manuelle Rohkeyword-/Diagnoseaktionen sind in einem einklappbaren Abschnitt `Weitere Werkzeuge (nur für Sonderfälle)` aufgehoben. PSERC-Menü und PSERC-Kern bleiben unverändert. Diese reine lokale Admin-Ausgabe wurde getestet, aber **noch nicht im echten WordPress-Browser abgenommen**.

## Lokale Testdurchführung – echtes Dateimaterial, kontrollierte Ersatzdaten

- Build ausschließlich aus echtem vollständigem Original-ZIP; 121/121 ZIP-Einträge, CRC vollständig bestanden. **Exakt vier** geänderte PHP-Dateien (einschließlich Header-Versionssprung 0.57.144.22 → 0.57.144.23), keine neuen Tabellen/Worker. **83/83 PHP-Dateien** bestanden `php -l`.
- Test verwendet die **echten 1.179 Snapshot-Einträge**, echte 100/87 Stichwortentscheidungen, echte 144 PPM-Planplatzzuordnungen, echte PSERC-Quellzeile und die real mit IDs zugeordneten 141 Beitragstitel. PHP-Simulation durch echte Methoden `PSTE_Snapshot`, `PSTE_Mini_Workflow::readParkhausForMini`, `acceptSingleOwnerSeoDecisions`, `singleOwnerSeoFor` sowie **echten** `PSERC_SEO_Reader::normalizeCandidate` aus PSERC 0.28.55.
- **36 PASS**: verschachtelter Titel positiv, fehlerhafte 9er-Titelfälle negativ, gespeicherter Planstatus, tatsächliche drei fehlende Posts fail-closed, vollständiger Testbestand, kein WP-Optionsschreiben, alle drei Freigabefächer, Quell-/Slot- und Planfingerprint, falscher Owner, doppelte Slots, gefälschte BELEGT-Referenzen, keine Freigabe bei fehlendem Handoff, PSERC akzeptiert verifizierte externe Quelle und hält veraltete zurück, übrige alte PSERC-Themen unverändert, drei Admin-Ansichten (Start, offener Stapel, 100 abgeschlossen).
- **Kritische Ehrlichkeitsgrenze:** Für den lokalen **positiven vollständigen Parkhausfall** erhielten ausschließlich die drei im echten Export nicht auffindbaren Post-IDs in der Simulation **synthetische** nachweisbar gekennzeichnete Titel. Das beweist den Codeweg, **nicht**, dass diese drei Posts in WordPress existieren oder ihre echten Titel bekannt sind. Für die echte fehlerhafte Quelle wurde `complete=false` getestet. Die neun wörtlichen „Array“-Titel wurden nicht erfunden/repariert.
- Kein echter WordPress-MySQL-End-to-End-Lauf, kein externer fachlicher SEO-Owner-Lauf, kein Rückimport und keine echte K0-Übergabe. Kein erfolgreiches Produktionsrelease behaupten.

## Binärpakete, echte Archivierung

- **Neu:** `/pferdeatelier/PLUGINS/PSTE-0.57.144.23-EXPORTFIX-NUR-TEST.zip` (634.545 Byte, SHA256 `dcf1f181d8b438f057476970237f888782312f60450f215e69713c203d0449b0`, Library `libfile_2e47f904ff44819185ccd46ff06b65f0`).
- **Paar:** `/pferdeatelier/PLUGINS/PFERDEATELIER-PSTE-05714423-PSERC-02855-QA-PAAR.zip` (875.972 Byte, SHA256 `154cbf04dc4a9b99ad1487e0bcd19fa90317b39c350c7b0dae8a965a56c78008`, Library `libfile_f6bc32a9041c8191a6986bf3d00370e3`).
- GitHub enthält `QA_ONLY/PSTE_05714423_EXPORTFIX/` mit textbasiertem vollständigem 4-Dateien-Diff, Testcode, Paketbauprüfung, Prüflog und Manifest. **ZIP-Binärdateien sind in der persistenten Library, nicht als GitHub-ZIP-Binärblobs.** Keine Ersetzung von `/Campus-Plugins/.../CURRENT.zip`.

## Der einzige nächste echte Freigabeschritt

Der TEST enthält den Fix. Noch offen sind die **neun nicht rekonstruierbaren alten Editorial-Planzeilen** und die **drei auf dem Server unbekannten Post-IDs**. Vor einer echten externen SEO-FREI-Entscheidung muss die neue Version auf isolierter Testseite an den vorhandenen Originaloptionen ohne Löschen/Neuanlegen nachweisen, ob die neuen Leser die Quellwerte auflösen können; andernfalls bleibt die Sicherheitsfreigabe gesperrt. **Keine neue 5.016er-Gesamtdiagnose, kein Keyword-Neuimport, kein K0-Schreibzugriff.**
