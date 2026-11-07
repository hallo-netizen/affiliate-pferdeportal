# Pferdeatelier / eBay: systemische Ursachenprüfung vom 07.11.2026 (nur Evidence)
 
## Basis und unveränderte Sperre
- Direkt gelesen: `release/affiliate-zentrale/current/affiliate-portal-router/` + `assets/ebay-portal-catalog-v2.json` auf `affiliate-release-current`.
- Current-Governance: Generation 313; 6.72.211 ist gesperrter Kandidat, AFF-ERR-065 offen. 6.72.308 ist nur getrennte lokale Arbeitslinie; das Original-Installations-ZIP ist in diesem GitHub-Sourcebaum nicht autoritativ hinterlegt. Keine Live-Gleichsetzung.
- Dieser Beleg verändert **keinen** Plugin-Quellcode, keine Freigabe, keine Produktdaten, keine Einstellungen und keine fremden Projektbüros.

## Belegter systemischer Fehler 1: falscher eBay-Bedarf
- Original-Katalog: 334 Produktseiten, 321 `business_concepts`, Pflichtliste `business_supply_contract.required_count=316`, ausschließlich fünf Grundlagen ausgenommen.
- In der **316er Pflichtliste** liegen neun eindeutig nicht als physische eBay-Warenfamilie zu bewertende Ziele:
  1. `concept-futterungsberatung` – Fütterungsberatung
  2. `concept-haftung-im-stall` – Haftung im Stall
  3. `concept-haltungsberatung` – Haltungsberatung
  4. `concept-hufberatung` – Hufberatung
  5. `concept-pferdehaftpflicht` – Pferdehaftpflicht
  6. `concept-sattelanpassung-beratung` – Sattelanpassung Beratung
  7. `concept-stallbau-beratung` – Stallbau Beratung
  8. `concept-transportrecht-pferde` – Transportrecht Pferde
  9. `concept-tuv-beim-pferdeanhanger` – TÜV beim Pferdeanhänger
- Drei zusätzliche **Hub-Suchprofile** sind thematisch Dienstleistung statt Warenfamilie: `hub-concept-wissen-beratung-und-partner`, `hub-concept-wissen-kurse-und-seminare`, `hub-concept-wissen-versicherungen-und-recht`.
- Konkrete Code-Verknüpfung: `trait-ppar-ebay.php::ebay_business_required_product_concept_ids()` liefert diese unbereinigte Liste an Auswahl, Verteilung und `trait-ppar-ebay-run.php::ebay_run_public_business_coverage()`. Nach Fehlen werden gezielt weitere Suchrunden und Abdeckungsprüfungen ausgelöst. `ebay_business_catalog_profiles()` durchsucht bisher sogar alle 321 Konzepte einschließlich fünf bereits ausdrücklich ausgeschlossener Grundlagen, dazu sämtliche 59 Hub-Konzepte.
- Sicher belegbares Korrekturziel für **diese neun**: 316 -> 307 reale Waren-Pflichtfamilien, die restlichen 307 genau identisch; 334 Portalziele bleiben bestehen, nur eBay-Versorgungsbewertung wird abgegrenzt. Weitere unklare Beratungs-/Dokumentthemen erst nach Anbieter-/Originalzeilenbeleg ausnehmen. Die drei Dienstleistungs-Hubs aus der eBay-Suche nehmen. Keine Kategorien im Portal löschen.
- WICHTIG: Die bloße Kürzung der Zahl genügt nicht: dasselbe eine Zulässigkeitsmerkmal muss für eBay-Suche, Lückensuche, Pflichtmenge, Ergebnisprüfung und veröffentlichbare eBay-Produktangebote maßgeblich sein. Keine zweite Parallel-Sperre und keine Sonderregeln je Produkt.
 
## Belegter systemischer Fehler 2: langlaufende Frische gegen Abschluss
- `trait-ppar-ebay.php::ebay_upsert_item()`: `fresh_until=now+6h`; `ebay_business_selection_concept_rows()` und `ebay_run_public_business_coverage()` verlangen Frische zum späteren Zeitpunkt. Daten können während `Discovery -> Refresh -> Auswahl -> Gapfill -> Public Verify` veralten. Der Code verhindert zu Recht veraltete öffentliche Angebote; **nicht** willkürlich sechs Stunden verlängern.
- Ob das beim letzten fehlgeschlagenen Live-Lauf der konkrete finale Fehlercode war, kann aus den gespeicherten GitHub-Heartbeat-Ausgaben **nicht** bewiesen werden.

## Belegter systemischer Fehler 3: Worker-Endzustand wird als GitHub-Erfolg gezeigt
- GitHub Action `Pferde Atelier eBay heartbeat`, Run 42342325416 / Job 128312512929 am 07.11.2026: 27 Statusantworten, darunter `busy`, `advanced`, danach um 05:50:42 UTC `status=failed`.
- GitHub Action `conclusion=success` bedeutet hier **nur funktionierenden Heartbeat-Transport**, keine abgeschlossene eBay-Verarbeitung. `failed` ist terminal; der HTTP-Status allein liefert nicht den gespeicherten eBay-`error_code`. Keine unbelegte Behauptung zur letzten Fehlerursache.
- Im kanonischen Code `trait-ppar-ebay-run.php::handle_ebay_external_tick` stoppt bei gespeichertem `failed` der Folgelauf bis zum erlaubten Wiederanlauf. Richtige Reparatur hängt am konkreten gespeicherten Fehlerzustand, nicht an neuen Neustart-/Umgehungsregeln.

## Verbindlicher KISS-Fixkorridor / vor Live-Freigabe
1. Einen **gemeinsamen** eBay-tauglichen Katalogvertrag nutzen. Versicherungen, Beratungen und reine rechtliche Leistungen bleiben Portal-Inhalte, niemals eBay-Pflichtversorgung. Alle Suche/Gapfill/Abdeckung/Veröffentlichung lesen denselben Umfang.
2. Die **eine** bestehende Aktualisierungsstrecke so nachführen, dass echte, rechtzeitig erneuerte Angebote das abschließende Safety-Gate erreichen können; keine Fake-Frische und kein Aufweichen der Source-/End-/Policy-Prüfungen.
3. Originale Live-Rundaten des fehlgeschlagenen Laufs einschließlich `error_code`, `run_uuid`, Phase, Provider-Freshness, Quellen, Auswahl, Abdeckungsfehlgründen und Public Checkpoint gemeinsam abgleichen; danach nur bewiesene weitere Wurzel im vorhandenen Worker korrigieren.
4. Gegenprüfungen: 9 Non-Warenfamilien und 3 Dienstleistungs-Hubs verursachen keine eBay-Pflicht-/Discovery-Lücken; die 307 übrigen werden unverändert gesucht; valide frische Angebote in einer echten WordPress/MariaDB-Gesamtsimulation sichtbar; zu alte/manuell gesperrte/nicht verfügbare bleiben gesperrt; GitHub-Transporterfolg kann nie als Produktlauf-PASS gelten.
5. Erst mit realer gesamter Live-/Testquellen-Bindung, WordPress/MariaDB-E2E, öffentlichem HTML, gültigen Manifest-/Release-Gates kann ein installierbares Plugin freigegeben werden. Kein Sofort-Patch, kein neues Parallelplugin und keine Liveänderung aus diesem Bericht.

**Beweisgrenze:** Alle neun falsch geführten Pflichtfamilien und die fehlende Suchabgrenzung sind am autoritativen 6.72.211-Quellstand sicher reproduziert. Die **konkrete** Ursache des eBay-Live-Fehlcodes am 07.11. ist durch das GitHub-Heartbeat-Log noch nicht identifiziert. Weder eine freigegebene Reparatur noch steigende öffentliche Produktabdeckung wird behauptet.
