# Pferdeatelier · PSTE 0.57.144.21 · KISS-Prüfprotokoll · 07.11.2026

## Ausgangspunkt und tatsächliche Ursache

Basis ist der echte WordPress-Export von Version 0.57.144.20 (42/87 erledigt, 45 offen), und der ausführbare PHP-Quellcode aus der lokal bereits getesteten 0.57.144.20 ZIP. In diesem Bericht sind **7** Titel als `PRE_TITLE_ACTIVE_TITLE_CONTAINS_SOURCE_QUERY` gesperrt, **ohne dass der Bericht die tatsächlichen übereinstimmenden WordPress-Beiträge nennt**. Die sieben Live-Treffer können daher nicht anhand dieses Berichts unabhängig inhaltlich bestätigt werden.

In `PSTE_Planning_Readiness_Gate::preTitleDuplicate` hatte die alte Version aus einem im Titel vorkommenden vollständigen Suchsatz **sofort** einen harten Dublettenbeleg gemacht. Die nachfolgende semantische Prüfung wurde dann gar nicht ausgeführt. Zusätzlich ließ `PSTE_Cannibalization::keywordOwnershipCompare` bei gleicher Familie/Artikelart ohne gespeichertes SEO-Keyword spezifische Suchsätze ungeprüft als `PASS` durch. Beide Regeln sind nicht belastbar: ein Titel kann gleich klingende Wörter mit anderer Absicht tragen; eine anders formulierte Antwort kann denselben Suchbedarf haben. Die bestehende Quellen- und Kategorienprüfung ist dagegen kein Anlass für einen neuen Prüfbesitzer.

## Eine einzige bestehende Entscheidung mit drei Ergebnissen

**Die vorhandene zentrale Planungsprüfung bleibt der EINZIGE Eigentümer.** Sie liefert:

- `PASS`: kein belegter Konflikt mit den gebundenen Daten; freigabefähig, *sofern alle anderen bestehenden Workflowbedingungen erfüllt sind*.
- `BLOCKED`: gleiche gespeicherte SEO-Suchanfrage oder ein anderer eindeutig festgestellter Sperrgrund; keinen zweiten Artikel erstellen.
- `REVIEW_REQUIRED`: Suchsatz steht bloß im Alttitel oder bei einem bestehenden Artikel derselben Familie/Art fehlt der SEO-Suchbegriff; weder eine echte Dublette behaupten noch unbelegt freigeben. Vorhandene Quelle/Titel bleiben erhalten. `next_action=RETAIN_UNTIL_DISTINCT_SEARCH_QUERY_PROVEN`. Optional **ein neuer eigenständiger Suchbegriff** aus der normalen Keyword-Recherche; für diesen gelten wieder die normalen Regeln. **Nur Titel umformulieren ist keine neue Suchintention.** Keine neue Schleife und keine automatische KI-Umschreibung.

Beim Wiedereinstieg werden die alten Gründe der VORHERIGEN zentralen Prüfung **gelöscht, bevor ihr neues Urteil abgelegt wird**; echte fremde Gründe bleiben erhalten. Das verhindert eine Phantom-Dublettensperre aus Version .20. In der schon vorhandenen Berichtsfunktion werden der gespeicherte nächste Schritt und bis zu drei bereits vom EINEN Owner erfasste Treffer als **lesender Nachweis** ausgegeben (Beitrags-ID, Titel und Belegart). Keine zweite fachliche Prüfung.

## Ausgeführte lokale Tests – final aus der ZIP entpackt

- Archiv SHA-256: `e7c31de26437c52ce80962a2ce46782641d518b30d7974ff462c40c8ae37dc7e`; **121 Einträge, 83/83 PHP-Lint fehlerfrei**, genau **5** gegenüber `.20` geänderte Dateien: `class-pste-planning-readiness-gate.php`, `class-pste-cannibalization.php`, `class-pste-repository.php`, `class-pste-admin.php`, Plugin-Version. K0 und PSERC nicht verändert.
- **13/13 positive und negative Gegenproben** der originalen PHP-Zentralprüfung erfolgreich, einschließlich exakt gleichem SEO-Keyword, mehreren gleichzeitig vorliegenden Belegen, bloßem Titeltext, anderer Zielgruppe, semantischer Umschreibung ohne SEO-Beleg, bekanntem abweichendem Keyword, fremder Familie, nicht veröffentlichtem Artikel und bewusst unterschiedlichen Longtails. Wiederholtes `apply()` hält Quellenfrage/Titel unverändert.
- **87/87 echte Plugin-Reanalysefunktionen**, danach **87/87 erneuter Durchlauf** mit nachgebildeter WordPress-Datenbank: Titel/JA erhalten, 63 weiter Kategorie-Redaktionsbüro, 24 normale Kategorien. Ohne echte WordPress-Beitragsdaten ist dies **KEIN** Nachweis von 24 Live-Freigaben.
- **87/87 erneut** mit einem synthetisch hinzugefügten Altartikel ohne SEO-Keyword (mit ausdrücklich **simulierter** Herkunft): 10 `PASS`, 10 `REVIEW_REQUIRED`, 4 sonstige `BLOCKED` unter den 24 normal zugeordneten Fällen; alle unklaren Fälle bleiben nicht produzierend; nach zweitem Durchlauf unverändert.
- **Ein echter v20-Sperrgrund** `BROAD_SCOPE_EXISTING_SEO_KEYWORD_UNKNOWN_FAIL_CLOSED` wird im lokal gespeicherten Szenario beim v21-Reentry entfernt und durch den aktuellen Status `REVIEW_REQUIRED` ersetzt, ohne Phantom-`ALREADY_COVERED`-Rolle. 87er-Altzustände mit fehlendem Produktivbestand sind damit **nicht** einzeln live verifiziert.
- Kontext-Aktualisierung aus originalem PHP: 87 gespeichert, 63 Redaktionsbüro, 24 normal; **0** erneute Bestandsabrufe bei gezielter Aktualisierung. Kategorieentfernung korrekt erkannt. Die bestehende Admin-Berichtsfunktion exportiert den vorhandenen Trefferbeleg **ohne zweite Prüfung**, keine neuen Provideraufrufe.
- 13 nicht extern autorisierte MINI-Entscheidungen/Quellenfälschungen bleiben abgewiesen; K0/PSERC unverändert.

## Grenzen / nächste echte Kontrolle

**Nicht 1:1 gegen die Live-WordPress-Datenbank getestet.** Die aktuelle Liste konkreter Treffer-Beitrags-IDs/Titel der 7 bisherigen Planungssperren lag in bisherigen Exporten nicht vor. Erst ein neuer Lauf und der ergänzte Stapelbericht mit `existing_match_evidence` kann direkt zeigen, ob die zentralen Befunde im echten Portal korrekt sind. Ein Alttitel ohne gespeicherten SEO-Begriff kann keine sichere automatische inhaltliche Abdeckung beweisen. Die konservative dritte Antwort kann zusätzliche Themen zunächst zurückstellen; das ist absichtlich keine freie Artikelproduktion. Es wurden KEINE alternativen Keywords ohne Suchbeleg oder neue K0-Titel erfunden.

**Ergebnis:** KISS-Entscheidung und lokale Gegenproben bestanden; Live-Bewertung der tatsächlichen 87 bleibt offen. **Testversion**, kein behaupteter WordPress-Livetest.