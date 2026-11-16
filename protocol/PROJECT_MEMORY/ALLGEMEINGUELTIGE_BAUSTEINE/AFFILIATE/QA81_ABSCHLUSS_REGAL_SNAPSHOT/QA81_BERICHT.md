# QA81 – KISS eBay: begründete leere Regale schließen, bestätigten Endstand behalten
Stand 16.11.2026. **Originalcode lokal geändert; kein Live-Eingriff, keine WordPress-Installationsfreigabe.**

## Ergebnis – bereits vorhandener Abschluss
Der Original-PHP-Controller der bestehenden QA80-Testlinie führt den EINEN kanonischen Gesamtlauf mit offenen Produktfamilien zu `completed`, statt für fehlende Angebote endlos wieder zu suchen. Im explizit simulierten Original-PHP-Gesamttest: **283 Familien, 259 versorgt + 24 offen** und für alle 24 `safe_supply_gap_open`; dies sind **Modellwerte**, keine heutigen echten WordPress-Veröffentlichungen. Die bereits vorhandene zentrale Entscheidung `ebay_run_business_safe_supply_gap_contract` kennt drei unterschiedliche Ursachen: `safe_supply_gap_open` (im geprüften Ausschnitt kein sicher auswählbares Angebot), `technical_supply_unverified` (technisch nicht gesichert), `selected_not_publicly_verified` (ausgewählt, noch nicht öffentlich bestätigt). Keine Kategorie wird deshalb pauschal „nicht auf eBay erhältlich“ genannt. **Diese korrekt vorhandene Abschlussentscheidung wurde nicht neu gebaut.**

## Nachgewiesene gemeinsame Ursache und wirkliche QA81-Codeänderung
Im bisherigen `ebay_sync_finalize` wird schon beim **untergeordneten Suchjob** `last_sync` auf dessen `summary` gesetzt und die gesamte Option aktualisiert. Damit gehen bei neuen Läufen sowohl der vollständige letzte öffentliche Familiennachweis als auch die maßgebliche Zeitinformation als anzeigbarer Abschluss verloren; ältere Codes setzten zudem die Suchfrist zu früh.

QA81 ändert **nur die beiden bestehenden** eBay-PHP-Traits der QA80-Quelllinie:
1. `ebay_run_complete` speichert **erst nach echtem finalem SAFE-Public-Commit** die vom vorhandenen Abschluss-Gate bereits entschiedene Abdeckung mit Produktfamilienzählung und den alten individuellen Lückengründen in `last_sync['last_public_family_result']`. Keine zweite Entscheidung, kein Provider-Request, keine neue Tabelle.
2. `ebay_sync_finalize` überschreibt diesen Schlussstand und dessen Fertigzeitpunkt **nicht**, solange ein kanonischer Suchlauf aktiv ist. Der alte eigenständige Suchpfad bewahrt den letzten öffentlichen Familiennachweis ebenfalls.
3. Die bestehende Backend-Seite zeigt **den letzten fertigen öffentlichen Familienstand getrennt vom laufenden neuen Lauf** und kann in einer lesenden Tabelle je Familiennamen die Zahl der öffentlich bestätigten Produkte und die gespeicherten Gründe offener Fächer zeigen. Keine erneute Auswahl oder Datenbank-Abdeckungsrechnung.
4. Bestehende Suche, Wiederaufnahme, SAFE-Public-Gate, Frische- und Quellprüfung, einmaliger Cleanup und fachliche Entscheidungen bleiben unverändert. Ein ausgelaufener/technisch ungeklärter Treffer erhält keine falsche öffentliche Freigabe.

## Echte lokale PHP-/Originaldatenprüfungen, Grenzen
- PHP-Syntax für beide Quelltraits **PASS**.
- **26.967/26.967** QA80 Gesamtregrssions-Assertions mit unveränderten Original-CSV und QA81-Quellcode **PASS**, hauptsächlich Protokoll- und Modelltests.
- Direkter Abschlussfall: **259 + 24 = 283**, alle 24 mit begründetem SAFE-Gap, Lauf `completed`, keine Endlossuche.
- Der Folge-Run, `refresh` und ein aufgeschobener öffentlicher Commit **können den gültigen Abschlussbericht nicht löschen**.
- Echte `ebay_sync_finalize`-Methode: untergeordneter Suchjob bewahrt `last_sync.finished_at` und den bisherigen öffentlichen Regalstand, auch wenn sein Teiljob erfolgreich endet.
- Acht volle PHP-Controller-Szenarien: normal, Alt- und Neuprodukt blockiert, Angebotswechsel, keine neuen Produkte enden in `completed`, drei echte technische Speicher-/Datenbankfehler korrekt in `failed`; ursprüngliche SAFE-Liste bleibt.
- Gemeinsamer Original-PHP-Trait-Test: 21/21 simulierte Quellchecks genau einmal, zwei Such-/Controllerpakete, derselbe Run und SAFE-Bestand.

**Verbleibende Grenze:** Die früheren Originalexporte enthalten nicht den gesamten aktuellen WordPress-/eBay-Quellbestand und keine echten GetItem-Ergebnisse der heutigen Produktkacheln. Die aktuell installierte Version ist unbestätigt. Der Altabschluss kann nicht rückwirkend mit erdachten Produktresultaten gefüllt werden; der bestätigte öffentliche Regalnachweis entsteht in diesem Code erst bei einem WIRKLICH komplett beendeten neuen Lauf. Bestehender GitHub-Hardlock unverändert, kein neuer Livejob. **QA69 LIVE-Abnahme noch NICHT BESTANDEN.**

Lokal erzeugtes reproduzierbares Test- und Quellcodearchiv: `QA81_EBAY_KISS_ABSCHLUSS_ARCHIV_NUR_LOKALE_KORREKTUR.zip`, SHA256 `7dfae62e9b3a654800e998b7b6ef9545cfa7186989ef72ee5f15e11f7636ea92`; im Gespräch bereitgestellt, **KEIN WordPress-Plugin**.
