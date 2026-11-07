# Pferdeatelier · PSTE 0.57.144.22 · KISS-Gesamtworkflow und Gegenproben · 07.11.2026

## Wo stehen wir?

Ausgangspunkt ist **der echte WordPress-Stapelbericht der Version 0.57.144.21**, Export 07.11.2026 13:29:30 UTC. Im Report: 48/87 Fälle bearbeitet, 1 PASS, 46 HELD, 1 BLOCKED, 39 PENDING. Von den 18 bereits bearbeiteten Themen auf normaler Fachroute sind 14 `REVIEW_REQUIRED`, 3 `BLOCKED` und 1 `PASS`; die anderen 30 bearbeiteten Fälle gehören zur Redaktionsbüro-/Produktwahlroute (29 + 1).

**Reale Ursache in der vorhandenen zentralen Dublettenprüfung:** `PSTE_Cannibalization::keywordOwnershipCompare` hielt **jedes** Thema zurück, sobald ein alter Artikel derselben Kategorie und Artikelart **ohne gespeichertes SEO-Keyword** existierte. Das galt auch für klar speziellere Quellen wie „horseware regendecken“, „regendecken für ponys“, „regendecken krämer“ und „shetty regendecken“, wenn der ältere Titel nur eine allgemeine Regendeckenauswahl oder einen anderen Schwerpunkt nannte. Ein fehlendes SEO-Keyword ist kein Beleg für identische Suchintention.

## Vereinfachung in exakt einem vorhandenen Entscheidungsort

**Kein neuer Prüfschritt, keine zusätzliche Prüfinstanz:** Nur die bereits existierende Funktion `PSTE_Cannibalization::keywordOwnershipCompare` wurde innerhalb der zentralen `PSTE_Planning_Readiness_Gate` vereinfacht.

- Vorhandenes **gleiches gespeichertes SEO-Keyword** → `BLOCKED`, kein Doppelartikel.
- Vorhandener älterer Titel ohne bekanntes Keyword **mit erkennbar gleichem oder nahem Suchumfang** oder **zu breiter Ausgangsfrage** → `REVIEW_REQUIRED`, keine automatische Artikelfreigabe. Alte Titel erhalten dabei keine erfundene SEO-Keyword-Autorität.
- **Eigenständiger Longtail aus der ursprünglichen Suchfrage**, dessen relevanter Zusatz im alten Titel nicht vorkommt und der nicht hinreichend nahe wirkt → `PASS` dieser einzelnen Dublettenentscheidung. Andere bestehende Gates (Titel, Kategorie, fachliche Regeln) bleiben gültig.

Bei unbekannter SEO-Autorität arbeitet die Entscheidung nur mit **vorhandenen** Suchbegriffen, Kategorien, Typ und Artikelüberschrift. Die Möglichkeit von unsichtbaren gleichen Themen in älteren Artikeltexten lässt sich ohne Body-/Keyword-Beleg **nicht ausschließen**; diese Testversion behauptet deshalb ausdrücklich **keine vollständige semantische Sicherheit**. Gleichbedeutende Formulierungen können trotz unterschiedlicher Wörter eine Restunsicherheit bleiben. Fälle mit erkennbarem gemeinsamen Wortstamm (etwa „Halsteil“/„Halsabdeckung“) bleiben deshalb vorsorglich `REVIEW_REQUIRED`.

## Durchgeführte Tests aus der FINALEN ZIP

Archiv: `/mnt/data/PSTE-0.57.144.22-NUR-TEST.zip`; SHA-256 **`479260fc210683b0e4867588bafa0889a66af3443341c69ec19452d9476b403a`**; **121** Einträge; **83/83** PHP-Lint bestanden. Gegenüber der Original-.21-ZIP sind **genau zwei Dateien** inhaltlich anders: `includes/class-pste-cannibalization.php` und `portal-seo-topic-engine.php` (nur Versionsangabe). K0, PSERC und andere Plugins unberührt.

1. **23/23 positive/negative Prüfbeispiele** mit tatsächlicher PHP-Zentralfunktion `PSTE_Planning_Readiness_Gate::evaluate`/`apply`: Gleiches SEO-Keyword, Synonymähnlichkeit, allgemeine Alttitel, konkrete Marken-/Zielgruppen-Longtails, andere Artikeltypen und Familien, fehlerhafte Kandidaten, gelöschte Beiträge, gespeicherter zweiter Durchlauf.
2. **87/87 echte PHP-Reanalyseaufrufe** in nachgebildetem WP-Tabellen-/Index-Kontext; **87/87 ein zweites Mal** auf denselben gespeicherten Zeilen. 87 Ursprungsfragen, JA-Belege und Titel unverändert; 63 Kategorien offen, weiterhin ins bestehende Redaktionsbüro, 24 normale Kategorierouten, keine neuen Kategorien und keine externe Providerabfrage. Unter einem zusätzlich **synthetischen** Artikel mit unbekanntem SEO-Keyword: 18 PASS, 2 REVIEW_REQUIRED, 4 andere BLOCKED (24 Fachfälle). Das beweist Logik/Stabilität, nicht die produktive WordPress-Kategorieliste.
3. **Reale WordPress-Titelnachweise aus dem .21-Export** wurden einer ausdrücklich **simulierten gleichen Kategorie/Artikelart und fehlenden SEO-Kennzeichnung** zugeordnet (die echten Quellartikel-Metadaten stehen nicht vollständig im Report). Unter dieser absichtlich strengen Annahme: **18 Fachfälle: vorher 1 PASS, 14 REVIEW_REQUIRED, 3 BLOCKED; nachher 6 PASS, 9 REVIEW_REQUIRED, 3 BLOCKED**. Fünf konkrete Longtails werden aus der pauschalen Zurückstellung herausgenommen; die sieben direkt treffenden alten Titelformulierungen bleiben zurückgestellt. **Das ist eine lokale Gegenprobe, kein behaupteter neuer Live-Bericht.**
4. **Alte .21-Sperrbelege wurden von der echten .21-PHP-Funktion erzeugt**, gespeichert und anschließend mit der .22-Zentralfunktion erneut abgearbeitet: 5/5 Fälle korrekt, davon 4 zu PASS, 1 weiterhin REVIEW_REQUIRED. Keine alten Sperrgründe als Phantomblock, Quelle/Titel/Kategorieroute unverändert; nochmaliger identischer Durchlauf stabil.
5. FINAL-ZIP entpackt und **sämtliche Tests erneut genau gegen die enthaltenen PHP-Dateien** ausgeführt, statt nur die Arbeitskopie zu prüfen.

## Ehrliche Grenzen und nächster Schritt

**Nicht ausgeführt:** WordPress-1:1-Datenbanklauf gegen das echte Hosting, Artikeltext-Vergleiche oder automatisches Erzeugen neuer suchvolumenbelegter Keywords. Die 39 PENDING aus dem .21-Export sind nicht automatisch zu PASS geworden. `REVIEW_REQUIRED` bleibt nur **gespeichert/gesperrt**, bis tatsächlich eine andere belegte Quellsuchanfrage existiert. Die vorhandenen Sperren `QUESTION_TITLE_NOT_FAQ`, `CATEGORY_HEAD_INTENT_COLLISION`, `NON_EDITORIAL_TRANSACTIONAL_QUERY` und der Sonderweg Produktwahl bleiben unverändert. Kein Beitrag wurde direkt produziert.

**Nach der Testinstallation** einmal den 87er-Wiedereinstieg mit dieser Version ausführen und den aktuellen Stapelbericht auswerten. Wenn weiterhin unplausible Review-Fälle auftreten, ist der konkrete WordPress-Treffer samt Quelle nötig – nicht ein weiterer pauschaler Fix.