# eBay: ein Gesamtabnahmevertrag gegen alle dokumentierten Fehler (QA27–QA65)

**Gesamturteil: NICHT BESTANDEN.** Keine weitere Testzählung wird als Live-Lösung bezeichnet.

## Echte Daten
- Ein Run 97507628-4f4d-4527-bd77-fa573bce7067: 2769 Originalereignisse, zuletzt running/gapfill_discovery, 5/283 Familien.
- Auswahl: 155 geprüft, 2 materialisiert, 153 übersprungen.
- Fehlende 278 Familien: 215 im aktuellen Suchteil ohne Einzelabruf, 32 mit angenommenen Angeboten aber ohne Abdeckung, 31 mit Abrufen ohne Annahme.
- 578 bisherige Freigaben sind nach dem WordPress-Screenshot gespeichert, aber NICHT mit aktuell gültigen sichtbaren Angeboten gleichzusetzen.

## Abgleich gegen die historische Fehlerliste
- **QA 27–31,39–43,55,59–65:** GitHub-Wecksignal, REST-Status, Stopp/Fortsetzen, scheinbar aktiver Lauf. **Stand:** Einmalige Tick-Verarbeitung lokal geprüft; regelmäßige reale Zustellung NICHT abgenommen; Main unverändert, PR #759 geschützt.
- **QA 36–41:** Familienkapazität stoppt kompletten Lauf; alte Fehlerläufe nicht wieder aufgenommen. **Stand:** Lokal korrigiert; aktuelle sichere Produktabdeckung nicht bewiesen.
- **QA 48–50:** Gapfill entfernt vorherige Kandidaten, Abschluss/Cleanup konnte 482 von 578 SAFE-IDs verlieren. **Stand:** Lokal korrigiert, QA50 Mock 578→580; echter öffentlicher Bestand nicht gemessen.
- **QA 51–54:** Doppelte Partner-/Portalentscheidungen, unterschiedliche Produktbestandslisten, Verfügbarkeitsworker trifft Fachentscheidung. **Stand:** Lokal vereinheitlicht, Safe-Checkpoint-CAS; realer Gesamtbestand nicht abgenommen.
- **QA 56–58:** Nur 5/283 nach vielen Ticks, 153 abgelaufene ausgewählte Produkte. **Stand:** Lokale gezielte getItem-Neubestätigung; echter Export weiterhin 153 skips.
- **QA 63:** Teilrecherche-Ende fälschlich statt Gesamtabschluss als Startuhr. **Stand:** Lokal korrigiert, kein abgeschlossener Live-Gesamtlauf.
- **QA 29:** PRIVATE-Altanzeigen-Livebereinigung gescheitert. **Stand:** Keine bestätigte Live-Endabnahme.
- **QA laufender Screenshot:** Audit-Speichervorgang fehlgeschlagen. **Stand:** Weiterhin im WordPress-Screenshot gemeldet.

## EIN verbindlicher Gesamtabnahmetest (keine unabhängigen Erfolgsbehauptungen)

| Teil des Gesamtworkflows | Stand | Beweis |
|---|---|---|
| Katalog/Sollfamilien | **PASS** | Katalog 283; echter Lauf 283 Pflichtfamilien; 278 fehlend |
| Ein einziger verlässlich ankommender GitHub-Arbeitsaufruf | **NICHT NACHGEWIESEN** | Main-Workflow */15 + Selbstverkettung; beobachtete ausgefallene geplante Starts nach 10:25; PR 759 blockiert |
| Lauf und Cursor ohne Nullsetzung weiterbearbeitet | **NICHT ABGENOMMEN** | Original CSV: running/gapfill_discovery Fortschritt 474; letzter Nutzerstand Schritt 475, später PAUSIERT |
| Individuell passende Quellen recherchiert | **OFFEN** | 215 fehlende Familien ohne zugeordneten Einzelabruf IM AKTUELLEN SUCHTEIL; 31 abgefragt ohne angenommenes Angebot |
| Nur einmalige Produkt-/Familienentscheidung | **NUR LOKAL GEPRUEFT** | QA54: eine Planner-Entscheidung je Produkt/Portal/Durchgang; reale WordPress-Daten nicht gegengeprüft |
| Ausgewählte Produkte aktuell und veröffentlicht | **NICHT BESTANDEN IM REALEN EXPORT** | 155 geprüft, 2 materialisiert, 153 übersprungen; QA58-Mockfix noch nicht im echten Lauf nachgewiesen |
| Angenommene Angebote erklären die Abdeckung | **NICHT BESTANDEN IM REALEN EXPORT** | 32 fehlende Familien hatten angenommene Angebote im Suchteil; dennoch keine Abdeckung |
| Alte nachweislich gültige Produkte bleiben erhalten | **NICHT LIVE VERIFIZIERT** | 578 gespeicherte Freigaben in WordPress-Oberfläche; kein vollständiger echter Source/Creative/Frontend-Abgleich |
| Öffentliche Abdeckung und HivePress-Ausgabe | **NICHT BESTANDEN IM REALEN EXPORT** | 5/283 Familien im gespeicherten geprüften Kandidatenstand; öffentliche Seiten nicht endabgenommen |
| Protokolle dauerhaft gespeichert | **FEHLER IM LIVE-SCREENSHOT** | WordPress meldet fehlgeschlagenen Protokoll-Speichervorgang; Export kann historische Einträge enthalten, aber nicht vollständig |
| Vollständiger Abschluss und sicherer Folgestart | **NICHT ABGENOMMEN** | Der echte Export endet running/gapfill_discovery, nicht completed; QA63 Abschlussfrist nur lokal getestet |
| Keine schädliche PRIVATE-/Fremdanbieter-Veröffentlichung | **NICHT LIVE ABGENOMMEN** | QA29 PRIVATE-Altlasten-Livebereinigung gescheitert; spätere lokale KISS-Prüfungen ersetzen keine öffentliche Kontrolle |

## Konsequenz
- Ein vorhandener GitHub-Aufruf muss einen gespeicherten kanonischen Lauf nachweislich voranbringen (oder korrekt pausieren), ohne neue Suche/Cursor-Reset.
- eBay-Suche, Produktwahl, aktuelle Angebotsprüfung, einheitliche SAFE-Freigabe, veröffentlichte HivePress-Ausgabe und Bereinigung müssen mit denselben echten WordPress-Produkten bis zum terminalen Ende geprüft werden.
- Für fehlende Familien muss die ECHTE Quelle einer von drei Befunden zugeordnet sein: kein zugeordneter Suchlauf, Suche ohne brauchbaren Treffer, Treffer ohne Publikationsnachweis. Kein unbelegter „Markt leer“-Abschluss.
- Jede einzelne fachliche Prüfung hat genau einen Besitzer; GitHub weckt nur, der kanonische WordPress-Lauf steuert, die öffentliche Freigabe wird einmal festgelegt, die Aktualitätsarbeit ändert keine Kategorie/Produktfamilie.
- Weder ältere SAFE-Kampagnen noch die Lauf-ID oder Cursor dürfen bei fehlerhaften Teilantworten gelöscht werden. Kein neuer Pluginstand auf Grundlage nur synthetischer 130/130-Ticks.

## Quellen und Nachweisgrenze
- `pferdeatelier-ebay-lauf-574cb003b132.csv` (Originalexport), `Pferdeatelier_eBay_fehlende_Produktfamilien_97507628-4f4.csv` (Originalfehlfamilien), `Affiliate_6.72.346_EBAY_GESAMTWORKFLOW_TEST.zip` (gepackter Originalcode; SHA256 `2528ebfa053172cebaa0140200ce4681d0582257a91844a24f1044d6e30d7404`).
- GitHub Änderungsregister QA27–QA65 und echte Heartbeat-Jobs (u.a. Run 43580485610, 43568795402).
- Die WordPress-Datenbank, eBay-API und öffentlichen Produktseiten wurden durch diese Prüfung NICHT verändert oder live neu abgenommen.