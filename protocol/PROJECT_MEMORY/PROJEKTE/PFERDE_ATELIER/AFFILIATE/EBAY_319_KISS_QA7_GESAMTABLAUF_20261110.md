# Pferdeatelier eBay – QA7: KISS-Rückbau ohne Funktionsverlust

**10.11.2026 – isolierte Arbeitskopie, nicht live installiert, nicht als Produktionsrelease freigegeben.** Grundlage ist die bereits geprüfte QA6-Kopie; keine neue Plugin-Architektur, kein zusätzlicher Worker, keine neue Datenbanktabelle oder WordPress-Option.

## Gesamtablauf bleibt unverändert

Start → ein zentraler gespeicherter Lauf → vorhandene und neue eBay-Angebote prüfen → BUSINESS-Auswahl mit Mehrfachzuordnung → ausgewählte Angebote verarbeiten → gezielte Nachsuche fehlender Familien → öffentliche Nachweise und sicherer Veröffentlichungsstand. Einzelne Produktfehler stoppen andere Produktfamilien nicht. Pause/Fortsetzen, Zugriffssperre und Schutz des letzten gültigen öffentlichen Bestands bleiben erhalten. Die frühere zusätzliche 319-Steuerung war bereits in QA5 entfernt; sie wurde nicht neu eingebaut.

## Zwei nachweislich überflüssige Bestandteile entfernt

1. **Zweiter Options-Leseaufruf nach erfolgreichem Speichern:** `ebay_run_save` vergleicht den **gesamten** geschriebenen Zustand mit dem aus WordPress zurückgelesenen Zustand und meldet einen echten Speicherfehler. `ebay_run_phase_state_save` las danach denselben gespeicherten Zustand nochmals ausschließlich für den Vergleich eines Teilabschnitts. Jetzt wird derselbe Teilabschnitt aus dem *bereits erfolgreich vollständig verifizierten* Zustand verglichen – **kein erneuter `get_option`-Aufruf**, gleiche Rückgabe. Die entscheidende Kontrolle gegen fehlgeschlagene Schreibvorgänge wurde **nicht** entfernt.
2. **Nicht erreichter privater Wrapper:** `ebay_private_public_post_allowed` war im gesamten Plugin nur einmal vorhanden: als eigene `private`-Definition. Die tatsächlich verwendete private Prüfregel `ebay_private_public_post_allowed_base` bleibt unverändert, inklusive aller bestehenden öffentlichen Sicherheitsfilter. Keine Schnittstelle und keine öffentliche Funktion entfernt.

## Physische Kontrollen und reproduzierbare Tests

- QA6 → QA7: **66/66 ZIP-Dateien** vorhanden und CRC-PASS; nur zwei bekannte eBay-Trait-Dateien geändert, **64/66 Dateien bytegleich**. PHP-Syntax **23/23 PASS**. Kein Anbieterwechsel, keine Änderung an Katalogen, Bildern, historischen Sicherungen, Zugangsdatenpfaden oder WordPress-Core.
- Die **fünf bereits bestehenden Fachtestprogramme** an der aus der **fertigen QA7-ZIP** entpackten Originalquelle ausgeführt: **61/61 PASS** (16 zentrale Auswahl, 13 Fehlerisolation, 11 direkte Materialisierung, 10 zusammenhängender Testablauf, 11 dauerhaftes Speichern).
- **13/13 direkte QA6/QA7-Vergleiche identisch:** vier öffentliche Nachweisfälle sowie neun Nachsuch- und Auswahlfälle; Status, gespeicherte Ergebnisse und Aktionen identisch.
- **8/8 zusätzliche Speicher-Rückgabevergleiche identisch**, einschließlich fehlgeschlagener Speicherung, altem Schema, ungültigem Schlüssel und ungewöhnlichen Eingabewerten. Bei fünf erfolgreichen Speichervorgängen wurde genau **ein zusätzlicher `get_option`-Aufruf entfernt**; bei Fehlerwegen gab es keine Änderung.
- Alle Tests in der isolierten PHP-Umgebung mit nachgestellten WordPress-Funktionen; **kein realer WordPress-/MariaDB-/eBay-End-to-End-PASS** daraus abgeleitet.

## Dateien / Ablage

- QA7-ZIP in der persönlichen Library: `/pferdeatelier/PLUGINS/QA/EBAY_319_KISS_QA7_KISS_DOPPELTE_LESUNG_WEG_NICHT_INSTALLIEREN_20261110.zip`.
- ZIP SHA256: `9d5a9a37ee9a268bfde914449c6736ef7313271e01973082ca265393a3e41f4c`.
- Änderungspatch SHA256: `9ee3b191e26507b78883c6bc24d523b175d0ddc5b9f013c40299f099c6ad5c7f`.
- Prüfbelege: `EBAY_319_KISS_QA7_RUECKBAU_NUR_BEWIESENES_20261110.patch`, `EBAY_319_KISS_QA7_REGRESSION_20261110.json`.

**Einziger offener Gesamtbeweis:** Die getrennte IONOS-WordPress-Testinstallation `Pferdeatelier-Technik-Test` muss einen realen gespeicherten Altstand mit WordPress/MariaDB bis zur richtigen Produktkachel durchlaufen. Die temporäre System-Domain oder ein verbundener WP-Testzugang liegt in diesem Arbeitskontext nicht vor. Deshalb weder eine Live-Änderung noch eine Installationsfreigabe behaupten. Bis dahin QA7 Staging, ursprüngliche Version/Release-CURRENT und K0 unangetastet.


## Reale WordPress-Screenshots vom 10.11.2026 – offene Familien und fehlende eBay-Kacheln

**Beobachtet, nicht simuliert:** Im produktiven WordPress-Backend ist der *kanonische eBay-Gesamtlauf* seit dem letzten echten Fortschritt **09.11.2026 17:47:42** manuell pausiert, Phase \`gapfill_select/business_prune\`, nach **771 Arbeitspaketen**, bei **Schritt 774 / 1280**. Der gespeicherte Gesamtbeleg zeigt **114/298**, daneben **211 als fehlend**; die laufende **separate Nachsuchteilphase** hat **50 Familien**, **9.160 Quellen geprüft**, **109 aktiv / 109 materialisiert**, während **Lokaler BUSINESS-Recovery: failed / checked 25 / reused 0 / review 21 / blocked 4** angezeigt wird. Benutzer meldet und zeigt auf der Schabracken-Kategorieseite ausschließlich Idealo-/Amazon-Produktkacheln, keine eBay-Kacheln; er bestätigt dasselbe für Beiträge.

**Was der *wirklich installierte* PHP-Code grundsätzlich tut (6.72.320 QA7):**
- \`ebay_business_selection_coverage\` zählt lediglich die aktuellen Gewinner des Auswahlplans. Das ist **nicht** die öffentliche Abdeckung. \`ebay_run_public_business_coverage\` zählt nur gültige **veröffentlichte** eBay-BUSINESS-Kampagnen, deren Quell-, Policy-, Creative-, Klassifikations- und Zielseiten-Nachweise zusammenpassen. Eine erfolgreiche Materialisierung (109) beweist daher **keine** öffentliche Abdeckung.
- Zusätzlich verweigert \`ebay_business_campaign_source_allows_delivery_base\` die **öffentliche Anzeige** einer eBay-BUSINESS-Produktkampagne, wenn \`fresh_until <= time()\` oder harte Quell-/Policy-/Routenbedingungen nicht erfüllt sind. \`ebay_business_upsert_source_row\` setzt bei einer tatsächlichen frischen eBay-Abfrage \`fresh_until = now + 6 * HOUR_IN_SECONDS\`. Ein länger dauernder, pausierter Gesamtlauf und eine 6-Stunden-Frischeprüfung können so trotz zuvor angelegter Kampagnen zu fehlenden öffentlichen Kacheln führen. **Dass alle konkreten produktiven Datensätze abgelaufen sind, ist ohne Live-Datenbanklesung nicht belegt.**
- Die **211** der gespeicherten Nachsuche und die **114/298** aus dem vorherigen Gesamtstand sind unterschiedliche Phasen/Snapshots. Sie sind nicht arithmetisch als \(298-114=211\) zu lesen. „Fehlend“ heißt **fehlender veröffentlichter/fachlich geprüfter Nachweis**, nicht „auf eBay existiert kein Produkt“.
- Der Status \`local BUSINESS recovery failed\` und \`reused 0\` belegt, dass die lokale Übernahme zu diesem Zeitpunkt *keinen vorhandenen Kandidaten neu nutzbar gemacht hat*; die Ursachen der einzelnen 21 Prüf- und vier Blockfälle wurden im Screenshot nicht aufgeschlüsselt.

**Die einzig noch offene Ursache-Nachweislücke:** Aus der produktiven WordPress-Datenbank eine **einmalige, schreibfreie zusammenfassende Auswertung** der schon gespeicherten eBay-Ausgabeobjekte + Kandidaten mit den **bereits existierenden Ablehnungsgründen** (\`source_stale\`, \`source_missing\`, \`target_mismatch\`, \`campaign_not_public\`, \`creative_missing\` usw.) und Quell-Alterswerten lesen. Erst danach lässt sich fachlich trennen, wie viele Familien **wirklich ohne geeignete Angebote**, **falsch zugeordnet**, **unveröffentlicht** oder **nur veraltet** sind. Nicht 211 einzelne Fehlversuche bauen, keine Familien pauschal als nicht erhältlich klassifizieren, keine Sicherheits-/Frische-Regel blind entfernen.

**Grenze:** Der Chat hat keinen verbundenen WordPress-Datenbank-Lesezugang; der aktuelle Screenshot allein beweist **nicht**, welche der genannten technischen Ausschlussgründe auf wie viele Produktivkampagnen zutreffen. Daher keine Release- oder Reparatur-Erfolgsmeldung. Produktionsdaten, gespeicherter Lauf und Plugin bleiben unverändert.


## Verbindliche Korrektur: Suchentscheidung vom 10.11.2026 nicht erneut analysieren

Der Nutzer hat wiederholt zu Recht beanstandet, dass die bereits durchgeführte Ablehnungs-/Suchgrundauswertung fälschlich als nächster Arbeitsschritt vorgeschlagen wurde. **Diese Aufgabe ist bereits erledigt; keine neue Auswertung, kein erneuter 211er- oder 298er-Vollscan.**

**Im tatsächlich ausgelieferten QA7-Code direkt bestätigt:**
1. `ebay_missing_family_diagnostic_rows` liest ohne eBay-Aufruf die vorhandenen `profile_stats` und ihre drei gespeicherten Grundgruppen `hard_reasons`, `technical_reasons`, `review_reasons`. Die bestehende Adminseite bietet dazu bereits eine CSV-Liste; kein neuer Report nötig. Die Aussagen gelten ausdrücklich für den gespeicherten Suchteilabschnitt, nicht für den gesamten Marktplatz.
2. Die vorhandene Logik unterscheidet sechs Befunde: zulässige Treffer ohne Abdeckung → **Veröffentlichung/Zuordnung prüfen**, technische Störung → **nicht als Marktlücke werten**, angebotene aber abgelehnte Treffer → **Ablehnungsgrund beachten**, null Treffer im abgeschlossenen Suchausschnitt → **diesen Suchausschnitt als ergebnislos abschließen**, laufender Teilabschnitt → **denselben Lauf fortsetzen**, kein Einzelabruf → **keine Marktaussage**.
3. `ebay_run_business_safe_supply_gap_contract` akzeptiert nach einmaliger begrenzter kanonischer Nachsuche **ausdrücklich offene sichere Versorgungslücken** (`safe_supply_gap_open`) und technische Ausnahmen (`technical_supply_unverified`). **298/298 ist keine verpflichtende Veröffentlichungsquote.** Technisch ungeprüfte Fälle werden nicht zu sicher fehlenden Angeboten erklärt; vorgemerkte Nachprüfung gehört zum nächsten regulären Gesamtlauf, nicht zu unendlichen Sofortwiederholungen.
4. `ebay_run_schedule_new_business_gap_revalidation` nimmt *nur tatsächlich neu fehlende* Produktfamilien und erweitert den bisherigen Zielkreis höchstens bis zum festen Katalogumfang. Der bereits geschriebene Auswahl-/Fehlerkatalog darf nicht separat ein zweites Mal entschieden werden.
5. Wichtig zur tatsächlichen Störung: Die vorliegenden **produktiven Screenshots** belegen fehlende eBay-Kacheln, einen *manuell pausierten* Gesamtlauf, frühere öffentliche Abdeckung und lokale Bestandsübernahme ohne neu akzeptierte Kandidaten. Daraus folgt **nicht**, dass eine erneute 211er-Recherche die Anzeige reparieren würde. Der Quellcode hat zusätzlich eine 6-Stunden-Frische-Schranke für einzelne öffentliche Angebote; die genaue Verteilung der produktiven Sperrgründe ist in den vorliegenden Screenshots nicht sichtbar. **Nicht erneut per Schätzung eine konkrete Datenbankursache behaupten.**

**Folgerichtiger weiterer Arbeitsfokus ist kein neuer Such-/Ablehnungsreport, sondern die bereits bestehende Übergabe von geeignet ausgewählten Angeboten zu gültigem öffentlichem Checkpoint und sichtbaren Produktkacheln – mit Bestandsschutz und ohne neue Regel oder neuen Worker.** Die heute früher gelieferte Behauptung, man müsse zuerst Ablehnungsgründe erneut sammeln, ist ausdrücklich widerrufen. Keine neuen ZIPs oder Änderungen an Produktion auf Basis dieses reinen Protokollabgleichs.
