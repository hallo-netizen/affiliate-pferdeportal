# Pferdeatelier eBay – bereinigter, versionsgetrennter Gesamtbefund 07.11.2026
**READ-ONLY-EVIDENCE / KEIN PLUGIN-RELEASE / keine Current-Quelländerung.**
 
## Wichtig: Nicht mehr den alten Katalog reparieren
Quellen verbindlich trennen:
- Formale GitHub-Release-Autorität `affiliate-release-current`: 6.72.211, weiterhin AFF-ERR-065 / release_allowed=false. Dieses ALT-Quellpaket enthält 316 Pflichtfamilien und noch 321 Suchkonzepte. Die sichtbare falsche Einordnung von Haftpflicht/Rechts-/Beratungsthemen ist hier **historisch**.
- Lokale Pferdeatelier-Arbeit 6.72.296: 324 -> 314, zehn eindeutig nichtwarenförmige Bereiche entfernt; Bericht `EBAY_672296_KISS_PRUEFBERICHT.txt`.
- Spätere dokumentierte 6.72.306-Test-ZIP: exakt 297 geprüfte physische Pflicht-Warenziele (berichtet in `AFFILIATE_ZENTRALE_6.72.306_PRUEFBERICHT.json`).
- Aktueller `EBAY_KISS_6.72.308_GESAMTABLAUF_PRUEFBERICHT.json`: **298** `required_product_groups`. Diese Zahl ist das jüngste explizite Versionsbelegfeld; warum 297 -> 298, ist in den bisher geöffneten Belegen **nicht** geklärt. Deshalb NICHT blind auf 307, 297 oder 294 setzen.
- Bei 6.72.308 betreffen die jüngsten gesicherten vierfachen Quelländerungen eBay-Suche, Lauf/Abdeckung, Löschmeldungen und Router. Keine freigegebene Installation oder neue aktuelle ZIP im Autoritäts-Release-Branch.
- **Folge:** Die alte 316er-Definition ist NICHT als aktueller eBay-Engpass zu zählen und darf nicht erneut durch einen separaten Kategorien-Fix „korrigiert“ werden. Die Portalstruktur bleibt vollständig bestehen. Bei tatsächlicher Produktabdeckung NUR die im 6.72.308-Katalog nachweislich eBay-tauglichen Pflichtgruppen als Nenner verwenden; den noch unaufgelösten Unterschied 297/298 nicht verschweigen.

## Belegter eigentlicher Live-/Historien-Engpass
Historischer originärer eBay-Bericht 02.11.2026 (in `EBAY_URSACHENANALYSE_20261102_KISS.txt`):
- 220 Suchprofile, 908 gefundene Treffer, 420 `ebay_marketplace_mismatch`, 285 fachlich zurückgestellt, 5 akzeptiert.
- Dies waren HISTORISCHE Rohwerte, nicht der 07.11.-Live-Zustand. `deliveryCountry:DE` bedeutet Lieferbarkeit, nicht eBay-DE-Marktplatz. `X-EBAY-C-MARKETPLACE-ID: EBAY_DE` wurde bereits gesendet; die Herkunftssperre nicht blind abschalten.
- Suchbegriffe in 6.72.296 für vier aus Originaldaten belegte Produktfamilien bereits verbessert; GTIN/idealo-Crosscheck eingeführt. Nicht noch einmal denselben Fix vorschlagen.
- 6.72.308-Sammelpatch hat für Produktgruppen maximal eine bedingte zweite Suchseite, eine zusammengefasste Quell-/Creative-Abdeckungsprüfung, begrenzte Inbox-Suche und feste Retry-Zeit; lokaler Test ist KEIN Live-Nachweis. Original 6.72.308-Quell-ZIP nicht im autorisierten GitHub-Release-Sourcebaum verfügbar. Keine blinde Änderung an 6.72.211 als „6.72.308“ ausgeben.

## Live-Scheduler: neuer geprüfter Beleg
- GitHub Actions am 07.11.: `Pferde Atelier eBay heartbeat`, Run 42342325416, Job 128312512929.
- Statusfolge `busy`/`advanced`, dann um 05:50:42 UTC `status=failed`. Workflow selbst zeigt `conclusion=success` – dies bestätigt nur erfolgreichen HTTP-/Schedulertransport. **Weder erfolgreicher eBay-Abgleich noch neue öffentliche Produktversorgung.**
- Aus diesem Log ist der genaue WordPress-`error_code` nicht sichtbar. Ohne diesen kein Nachweis, welcher der bekannten Fehler im jüngsten Lauf terminal auftrat.

## Versionsübergreifende Frische/Abschluss-Kollision
- Der ältere originalverfügbare Quellstand 6.72.211 setzt `fresh_until` bei Quellenabruf auf +6h, Auswahl und öffentliche Abdeckung verlangen später frische Originalquelle. Ein großer `Discovery -> Refresh -> Auswahl -> Nachsuche -> öffentliche Freigabe`-Lauf kann deshalb Kandidaten bis zur endgültigen Freigabe verlieren.
- Das ist ein **nachgewiesener Ablaufkonflikt im alten Code**, aber NICHT als konkreter Endfehler des 07.11. oder unbesehen als Fehler im 6.72.308-Codesatz auszugeben. Sechs Stunden ohne Providerbeleg nicht verlängern.
- In 6.72.297 sind Artikelpläne/öffentliche Freigaben und neue Checkpoints bereits lokal harmonisiert worden; nicht erneut als offene unbehobene Ursache listen ohne aktuellen Gegenbeleg.

## Jetzt echte nächste Arbeit, nicht Symptome
1. **Aktuelle 6.72.308 Quelle und Prüfbericht** als einzige Basis; 298er Manifest und tatsächliche 6.72.308 Suchprofile verifizieren; keine Ausschlüsse aus altem 6.72.211 übertragen.
2. Aus dem gespeicherten echten, fehlgeschlagenen eBay-WordPress-Lauf den exakten `error_code`, Phase, `run_uuid`, quellseitige Zeitstempel, fachliche Ablehnungszählungen, Auswahl, gespeicherte öffentliche Kampagnen und Checkpoint-Status auslesen. NICHT aus reinem Scheduler-`success` schließen.
3. Die **gesamte bestehende Strecke** als eine Einheit nachstellen: Suchprofile -> Liefer-/Marktplatzcode -> echte Warenerkennung -> Qualität/Quellenfrische -> Kampagnenspeicherung -> Public Gate -> Kategorie/Artikel-Produktkarten. Den ersten **tatsächlich reproduzierten** systemischen Abbruch im selben vorhandenen Worker korrigieren, keine weitere Architektur.
4. Gegenbeweise: nicht-eBay-taugliche Kategorien **null** Pflichtgruppen, bekannte gute Produkte nicht irrtümlich verworfen; falscher Marktplatz, fehlende Herkunft, veraltete Daten und unpassende Angebote weiterhin blockiert. Nur nach echtem WordPress/MariaDB-E2E und tatsächlicher öffentlicher Ausgabe Plugin freigeben.
 
**Korrekturhinweis:** Die zunächst hier gesicherte, vom alten 6.72.211 abgeleitete Forderung `316 -> 307` war ein Versionsfehler und wurde ausdrücklich verworfen. Das jüngere 6.72.308-Testprotokoll weist bereits 298 Pflichtgruppen aus. Daher ist kein alter 316er-Katalog-Fix durchzuführen.
