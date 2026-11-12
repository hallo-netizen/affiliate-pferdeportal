# Pferdeatelier eBay 6.72.321 QA9 – KISS: Suchen, Anzeigen und Verfügbarkeit trennen

Datum: 10.11.2026. **NUR ISOLIERTE TESTFASSUNG, KEIN LIVE-/CURRENT-RELEASE.** Grundlage ist das vollständig geprüfte QA7-Plugin 6.72.320 mit dem QA8-Pausen-Fix. Produktionsdaten und WordPress wurden nicht angefasst.

## Ziel
Eine pausierte, gescheiterte oder noch laufende eBay-Recherche darf den bereits geprüften, veröffentlichten Produktbestand **nicht** an seiner Anzeige oder Aktualisierung hindern. Neue recherchierte Produkte sollen nach fachlich sicherer Materialisierung **auch vor dem Abschluss der Gesamt-Recherche** sichtbar werden. Bestätigt beendete/ausverkaufte Angebote müssen verschwinden. Die eBay-Frischegrenze von sechs Stunden bleibt bestehen.

## Konkrete Änderungen
1. **Frühere Veröffentlichung im bisherigen sicheren Ausgabepfad:** Nach jeder passenden ursprünglichen BUSINESS-Materialisierung, auch in `gapfill_select`, werden nur bereits wirklich **veröffentlichte** und durch die bestehende Quellen-/Sicherheitsprüfung freigegebene Produktkampagnen an den **einen** bisherigen sicheren öffentlichen Checkpoint angehängt. Der frühere gültige Bestand bleibt. Auch ohne zuvor vorhandenen Checkpoint kann das erste qualifizierte Produkt einen neuen sicheren Grundstock begründen. Ein vorhandener ungültiger Checkpoint wird **nie** überschrieben. Keine zusätzlichen Checkout-/Klassifizierungswege.
2. **Bestehende Produktangebote automatisch aktualisieren:** Der bereits vorhandene getItem-/Refresh-Mechanismus verarbeitet in einer eigenen, begrenzten WordPress-Aufgabe ausschließlich *bereits veröffentlichte BUSINESS-Angebote*: im Normalfall alle zwei Stunden; höchstens fünf Angebote je Arbeitsschritt, bei vorhandenem externen Herzschlag zwei. Bei vielen Produkten läuft dieselbe Aufgabe in kleinen Fortsetzungen. Keine eigenständige Recherche, keine neue Worker-Engine und keine neue Tabelle. Verfügbarkeitsergebnis bleibt getrennt vom gespeicherten Gesamt-Recherche-Cursor. Anhalten/Fortsetzen oder Fehler der Recherche blockieren diese Aufgabe nicht.
3. **Sichere Aktualität:** Bestätigte Nichtverfügbarkeit durch Enddatum, OUT_OF_STOCK oder getItem-Endsignal geht durch den bestehenden Beendigungs-/Ersatzpfad. Temporäre eBay-Fehler beenden ein Angebot nicht künstlich und machen es auch nicht künstlich länger frisch. Vorhandene `fresh_until`-Grenze (sechs Stunden) bleibt unverändert, statt die verbindliche eBay-Frischepflicht auszusetzen.
4. **Pausen-/Fehlstatus:** Bereits in QA8 korrigiert; ein manueller Halt der Recherche wird nicht mehr vom externen Herzschlag als neuer Recherchefehler behandelt. Die Aktualisierung bestehender Produkte darf dennoch arbeiten.
5. **Backend und KISS:** Die in QA5–7 bereits aus dem sichtbaren Backend entfernten redundanten Untermenüs und der beseitigte zweite 319-Controller bleiben entfernt. Statt zusätzlicher Backendseite nur eine kurze, lesende Anzeige des Aktualisierungsstands und des getrennten Recherchestatus. Keine zusätzliche Fachprüfung oder zweite Benutzersteuerung.

## Unverlierbarkeit und Grenzen
- **Kein Löschen, Zurücksetzen oder Neuanlegen** der bestehenden Rechercheoptionen, Quellhistorie, vorhandenen Artikel, Angebote, Zuordnungen, Laufcursor oder bisheriger Checkpoints durch den neuen Weg. Nur eine kleine neue WordPress-Option speichert den Cursor der **Verfügbarkeitsaktualisierung**, niemals Produktdaten.
- Bereits gefundene Produkte bleiben physisch in den bestehenden Speichern. Die bestehende `ebay_refresh_mark_ended`-/Tombstone-Funktion behandelt nur nachweislich abgelaufene Angebote und bewahrt die historische Quelle.
- Sicherheitshalber wird bei fehlender sicherer Produktverifikation nichts als neu verfügbar behauptet. Ein alter, defekter Checkpoint wird nicht überschrieben. „Freigegeben“ bedeutet weiterhin nicht „jedes Produkt auf jeder Kategorie garantiert“.
- WordPress-Cron ist nur dann zuverlässig zweistündlich, wenn WordPress/Serveraufgaben wirklich ausgeführt werden. Externer Herzschlag kann bei pausiertem/fehlerhaftem Recherchelauf einen begrenzten Teil der Verfügbarkeitskontrolle übernehmen.
- Die tatsächlich gespeicherten 109 Produkte, eBay-Antworten, die Datenbank und die öffentlichen Kategorien wurden hier **nicht** in einer realen WordPress-Testinstallation validiert. Darum **nur Test-Plugin**, keine Behauptung eines fertigen Live-Fixes.

## Artefakt und Prüfungen
- ZIP `Pferdeatelier_Affiliate_6.72.321_QA9_KISS_NUR_STAGING_TEST.zip`; 66 Dateien, **62 davon byteidentisch** zu QA7 6.72.320, nur vier bearbeitet: zwei eBay-Traits, Plugin-Hauptdatei und Readme.
- Version `6.72.321` im WordPress-Header, Plugin-Konstante und Readme konsistent.
- ZIP-Dateiprüfung 66/66; **23/23** PHP-Syntaxprüfungen bestanden; **61/61** bestehende PHP-Fachtests gegen **QA9-Quelldateien** bestanden, zusätzlich **19/19** gezielte PHP-Tests (mocked WP-/DB), darunter leerer Grundstock, Bestandsschutz, manuell pausierter Lauf, Fortsetzungen, Nicht-Überschreiben defekten Checkpoints und Auth-Ausfall.
- ZIP SHA256: `4a84696bdd10d5c32f3ab5d4e4583fc9029ef673403f43eebfe2217ffd72e47a`, Größe 5.370.718 Bytes.
- Vollständiger Patch gegen 6.72.320, maschinenlesbare Datei-für-Datei-Prüfung und die ausführbaren Tests liegen in `PLUGINS/EVIDENCE` im QA-Branch.

**Abnahmeschritt vor Live:** dieselbe Test-ZIP auf getrennter WordPress-Instanz mit vorhandener Recherchehistorie einspielen. Nachweisen: erste schon geprüfte eBay-Kachel trotz pausierter Recherche, aktualisierte Quelle innerhalb zwei Stunden, beendet ausgeblendete Ware, erhaltene Historie, keine falsche Kategoriezuordnung oder doppelte Kampagne. Ohne diesen Nachweis keine Current-/Produktivfreigabe.

## Reale Screenshots 17:35–17:40 Uhr – Fortschritt ja, Backend langsam

**Neue Beobachtung aus vom Nutzer bereitgestellten Screenshots (10.11.2026, Browser pferde-atelier.de):**
- 17:35 Uhr: kanonischer Lauf **running** in `gapfill_discovery`, rund **340 Pakete / 345 echte Schritte**.
- 17:40 Uhr: derselbe Lauf **running**, rund **360 Pakete / 365 echte Schritte**. Damit innerhalb dieser fünf Minuten **20 zusätzliche Pakete und 20 Fortschrittsschritte**; kein bestätigter Stillstand. Der Bildschirmausschnitt zeigt keine Abschaltung und keine Datenlöschung.
- Gespeicherte öffentliche BUSINESS-Kategorieabdeckung **154/298**, offene Familien **144**; separat **232 gespeicherte eBay-Freigaben** (nicht gleich tatsächlich sichtbare Produktkacheln). Auswahl-Teilstatus **complete**, **310 Quellen geprüft, 299 aktiv/materialisiert**; dies ist nicht der öffentliche Gesamtabschluss.
- Das Frontend zeigte zwischenzeitlich mindestens **eine sichtbare eBay-Produktkachel** auf der Schabracken-Kategorieseite; ein vollständig repariertes Frontend ist dadurch nicht bewiesen.
- Weiterhin **„Produktverfügbarkeit noch nicht geprüft“**: Es gibt in den Screenshots **keinen Nachweis** eines erfolgreichen Durchlaufs der neuen zweistündlichen QA9-Verfügbarkeitskontrolle.
- Nutzer meldet **„Backend ist unfassbar langsam“**. Ein genauer Seitenzeit-/SQL-/Serverlast-Messwert fehlt. Darum **die neue Verfügbarkeitskontrolle nicht als bewiesene Ursache bezeichnen**.

**Direkt aus QA9-Quelltext überprüfte Belastungspfade:**
1. Die bestehende Selbstfortsetzung `ebay_run_handle_self_drive_request` führt das jeweilige Arbeitspaket aus und löst bei `advanced` oder `retryable_error` die nächste gleichnamige Fortsetzung aus; der kanonische Arbeitslauf läuft daher unabhängig davon weiter, ob die Backend-Seite geöffnet ist.
2. Die auf der eBay-Adminseite eingebundene **45-Sekunden-AJAX-Statusabfrage** `ppar_ebay_canonical_tick` nennt sich lesend, kann aber in `run_ebay_admin_ajax_tick` nach **180 Sekunden nachweislichem Stillstand** selbst **einen echten Arbeitsschritt** ausführen und wieder fortsetzen. Dies ist ein **belegter zusätzlicher Last-/Seiteneffekt** des Statuspfads, aber keine Erklärung des normalen laufenden Fortschritts.
3. QA9 legt neu eine Verfügbarkeitsaufgabe `ensure_ebay_refresh_schedule` mit Ersttermin **60 Sekunden nach geplantem Cron-Anlauf** an; höchstens **5 eBay-Angebote je Paket**, bei voll besetztem Paket ein Fortsetzungstermin nach **90 Sekunden**. Die Backend-Anzeige „noch nicht geprüft“ legt aber nahe, dass zumindest **noch kein Prüf-Batch erfolgreich protokolliert** wurde. Ein Cron-Rückruf könnte vorher mit `disabled`, `compliance_pending`, `storage_unavailable` etc. enden, ohne `last_batch_at` zu setzen; **exakten Runtime-Grund nicht raten**.
4. Die Adminseite `render_ebay_page` lädt bei jedem Aufruf mehrere gespeicherte Statusoptionen, eine begrenzte Review-Liste und baut den vollständigen **fehlende-Familien-CSV-Datensatz bereits während des Seitenaufbaus**, selbst bei zugeklapptem Detailbereich; das ist ein belegter, unabhängig zu optimierender Leseweg, sein Zeitanteil aber noch unbekannt.

**Verbindlicher KISS-Auftrag für die nächste Plugin-Version (noch nicht als erledigt ausgeben):**
- **Kein aktuelles Plugin deaktivieren / keinen Lauf zurücksetzen, solange Nutzer dies nicht will.**
- Backend-Status strikt **nur lesen**; keinerlei synchroner Worker-/Selbstfortsetzungsversuch durch normales Öffnen/Status-Pollen. Den bestehenden Hintergrund-Taktgeber weiterverwenden; Fehlerbehandlung nicht schwächen.
- Bei zugeklapptem Report keine teuren Vorbereitungen, unnötige Options-, Katalog- oder DB-Lesewege zurückbauen und Quellen nur einmal einlesen. Keine neue Backend-Seite.
- Separate Verfügbarkeit auf **begrenzte Serverlast** prüfen; Pakete/Weiterleitung nicht mit Recherche konkurrieren lassen, ohne wieder von der Recherche abhängig zu werden. Sechs-Stunden-Frische und 2h-Prüfziel beibehalten.
- **Vorher/nachher in echtem WordPress messen** (Backend-Ladezeit, AJAX, Cron-Job, Abdeckung, aktuelle Freigaben); ohne Messung keine Aussage „Backend-Langsamkeit behoben“.
- Alle recherchierten Produkte, Zuordnungen, Laufcursor, öffentliche Checkpoints und historischen Daten erhalten; andere Portale unangetastet.

### Reales Backend-Folgefoto 17:48 Uhr

Quelle: weiterer Nutzerscreenshot vom 10.11.2026 um 17:48 Uhr (WordPress `pferde-atelier.de/wp-admin/admin.php?page=affiliate-portal-ebay`).

- Derselbe laufende kanonische eBay-Gesamtlauf, Phase `gapfill_discovery`, weiterhin **running**.
- **Pakete 360 → 399, reale Fortschrittsschritte 365 → 404** seit Screenshot ca. 17:40 Uhr. Das sind 39 Pakete und 39 Schritte in acht Minuten; **kein Laufstillstand nachgewiesen**.
- **Öffentliche Familienabdeckung 154/298 (144 offen) unverändert**, **232 gespeicherte Freigaben unverändert**. Aus laufender Nachsuche allein folgt kein veröffentlichter Gewinn; daraus kann weder Markt-Nichtverfügbarkeit noch ein Veröffentlichungsfehler für jede einzelne Familie geschlossen werden.
- **Verfügbarkeitsstatus weiterhin „noch nicht geprüft“**. Kein dokumentierter erfolgreicher Durchlauf der neuen QA9-Verfügbarkeitsaufgabe.
- **Lease: frei**, **Selbstfortsetzung: aktiv**. Benutzer hatte zuvor sehr langsames WordPress-Backend gemeldet, in diesem Folgefoto keine Antwortzeitmessung.
- **Nächste Version, nicht als erledigt ausgeben:** Status-Polling wirklich lesend, teure Berichte nur auf Anforderung, Hintergrund-Taktung/Last sauber begrenzen. Bestehende Recherche, Angebote, 232 gespeicherte Freigaben, Checkpoint und Cursor nicht zurücksetzen. Kein weiterer Plugin-/Daten-Eingriff aus dieser Beobachtung.
