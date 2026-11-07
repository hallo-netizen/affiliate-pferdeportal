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

## HISTORISCHE GESAMTSICHT – gegen erneuten Chat-Neustart, 07.11.2026

**Gemeinsames Muster, durch alte Berichte belegbar:** Es werden Erfolge einzelner Arbeitsschritte dokumentiert, aber die eigentliche Käufer-Sichtbarkeit am Ende des Gesamtwegs ist weder bei der älteren Installationskette noch bei 6.72.308 als echte Live-Abnahme bewiesen. Deshalb ist ein PASS einzelner Simulationen kein Ergebnis.

Wesentliche unterschiedliche Originalbefunde:
- **12.10.** Live/Test-JSON desselben Beitrags, beide Plugin 6.72.224: Live-Planzustand `no_output` trotz technisch geeigneten Ersatzbanners; Ranking 0, Importalter 499 Stunden. Test hatte andere Banner-/Kampagnenbestände. Mehrere 6.72.217–.226 „Fix“-Installationen hatten neue Live-Regressionsfehler; selbst Paketversion und interne Versionskonstante waren 6.72.221/.222 nicht einheitlich. Quelle: `PFERDEATELIER_AFFILIATE_UEBERGABE_20261013_OHNE_BIBLIOTHEK(1).md` und offizielles AFF-ERR-065-Register.
- **01.11.** Nutzerbild/Arbeitsbericht zu 6.72.287: nur **104 von 324** damals geforderten Produktbereichen öffentlich versorgt; konkreter Abbruch `business_gapfill_public_invariant_failed` = Auswahl meldete Kandidaten, die öffentliche Ausgabe konnte nicht bestätigt werden. Ursache für den genauen betroffenen Live-Datensatz mangels authentifiziertem Quellabzug offen.
- **02.11.** Original-6.72.287-Code erlaubte falsche Erfolgsmeldungen bei fehlenden Pflichtkennzeichen oder fehlgeschlagenen Speicherschritten; spezifische Fehler wurden als „nicht aktiv“ versteckt. Lokal ROT/GRÜN belegt; diese Fixes sind in der späteren Arbeit dokumentiert. **Nicht erneut als neu ungefixte Ursache erfinden.** Quelle: `AFFILIATE_672287_KISS_PRUEFBERICHT_20261102.txt`.
- **02.11.** Historischer eBay-Abruf: 908 Ergebnisse, nur 5 angenommen; 420 wegen nicht nachgewiesenem `EBAY_DE` ausgeschlossen, 285 in Review. Das ist ein **Such-/Zulassungsengpass**, jedoch keine Aussage über den aktuellen 07.11. Produktbestand. Sichere Markt-/Produktkontrolle niemals pauschal aufheben. Quelle: `EBAY_URSACHENANALYSE_20261102_KISS.txt`.
- **02.11. bis 06.11.** Alte Pflichtliste schrittweise gesäubert, neue Produktbegriffe, EAN-Suche, korrekte Speicherfehler, Plan-/Anzeigeabgleich, öffentlicher Checkpoint, Fortschrittsanzeige, Suchseiten-Nachgang und beschleunigte Coverage bereits **lokal** bearbeitet; 6.72.306 meldet 297, 6.72.308 meldet 298 Pflichtgruppen. Warum die Zählung um 1 abweicht, ist offen. NICHT die veraltete 316er-Pflichtliste erneut reparieren.
- **07.11.** GitHub-Live-Heartbeat Run 42368324052, Job 128391033676 um 11:28 UTC (12:28 MEZ) liefert `status=failed`, obwohl GitHub-Transport `success` meldet. Produktlauf **nicht** erfolgreich belegt; der echte `error_code` wird vom GitHub-Log nicht geliefert.
- **6.72.308-Testbericht** ausdrücklich: kein realer eBay-API-Lauf, kein öffentliches WordPress-HTML, keine echte Datenbank-/Live-Abnahme, kein installierbarer Release. Die lokalen Pass-Zahlen reichen hierfür nicht.

**Ableitung – kein weiterer Symptomen-Fix:** Die Systemgrenze zwischen „gefunden“, „fachlich zulässig“, „gespeichert“ und **„tatsächlich sichtbar“** muss vom selben vorhandenen eBay-Lauf durchgehend belegbar sein. Keine weitere eigenständige Prüfung/Architektur, kein neues Sammelplugin und kein erneuter Dreitageslauf auf Verdacht. Ein falscher echter PASS darf nicht entstehen, wenn die öffentliche Ausgabe fehlt. Bei realer externer Angebotslücke darf umgekehrt kein fiktiver erfolgreicher Import behauptet werden.

**Exakter nächster Prüfpunkt (kein neuer Produktabruf):** Bestehenden fehlerhaften Lauf mit seinen ORIGINALEN WordPress-Laufdaten, Fehlercode, tatsächlich zugelassenen eBay-Warenkategorien und der aktuellen öffentlichen Produktausgabe zusammenführen. Erst dann die *eine dort belegte* Engstelle innerhalb des bisherigen Ablaufs beseitigen. Die bereits erledigten Korrekturen nicht neu programmieren. Keine Freigabe ohne nachgewiesenen Gesamtweg.

**Wahrheitsgrenze:** Die Historie beweist diesen methodischen und ablaufbezogenen Gesamtmangel. Sie liefert **noch keinen sicheren individuellen Fehlercode des letzten 07.11.-Laufs** und keine Bestätigung, dass eine konkrete neue Codeänderung ihn beheben würde.
## Nachtrag 07.11.2026 16:35 MEZ – vorhandener Fehlergrund wurde vom Heartbeat unterdrückt

**QUELLBELEG / klarer Schnitt der zwei Fehlerarten:** Die vorhandene 6.72.297-Original-PHP `includes/trait-ppar-ebay-run.php::handle_ebay_external_tick()` liefert bei `status=failed` ausdrücklich `error_code`, `phase` und `restart_required=1` im vorhandenen `external_tick_v2`-Response. Der tatsächlich laufende GitHub-Scheduler `.github/workflows/pferde-atelier-ebay-heartbeat.yml` parse/printet aus derselben Antwort **nur** `status server_time`; der CASE `idle|completed|failed|disabled` beendet `failed` mit `exit 0`. Dadurch erscheint der GitHub-Transport grün, obwohl die eBay-Gesamtoperation fehlgeschlagen ist, und der vorhandene konkrete Fehlercode erreicht das Github-Protokoll nicht. Das ist ein **nachgewiesener Informationsverlust in der bestehenden Ablaufüberwachung**, nicht die bewiesene Ursache der fehlenden Produkte.

**Reproduktions-/Schutzversuch (KEIN LIVE-MERGE):** PR #681 betraf ausschließlich diese bestehende GitHub-Workflowdatei, keine Plugin-, WP-, eBay-, API-, Katalog- oder Workeränderung; bestehender Scheduler-KISS-Selbsttest **16/16 PASS**. Aber **übergeordneter unveränderbarer Sicherheitshardlock** wurde in Github Actions Run 42387164620, Job 128446878147, mit `IMMUTABLE_SECURITY_PATH_CHANGE_BLOCKED` **FAIL**. Kein Sicherheits-Bypass zulässig. PR #681 daher explizit **geschlossen ohne Merge**. Die Original-Workflowdatei auf `main` wurde nicht geändert. Niemals Erfolg oder installierte Korrektur behaupten.

**Wichtig für Fortsetzung:** Die eBay-Version 6.72.308 ist weiterhin eine unfreigegebene lokale Testgrundlage; ihr Live-Zustand und tatsächlicher `error_code` sind *nicht* durch die 6.72.297-Quellprüfung bewiesen. Kein neuer ZIP-Fix und kein künstlich behaupteter Gesamt-PASS. Nicht erneut versuchen, den gesperrten GitHub-Workflow auf anderem Weg umzuschreiben. Die bestehende WordPress-Run-State-Anzeige/Originaldaten für den zuletzt gescheiterten Kanonischen Lauf sind der fehlende bindende Beleg. Erst danach den **bestehenden** eBay-Gesamtweg (Suche → Zulassung → Speicherung → veröffentlichte Kampagne → sichtbare Ausgabe) gegen reale Daten und alte Negativfälle vollständig prüfen.

**Einmalige Links:** https://github.com/hallo-netizen/affiliate-pferdeportal/pull/681 ; https://github.com/hallo-netizen/affiliate-pferdeportal/actions/runs/42387164620
