# PSTE 0.57.144.15 – ein zusammenhängender KISS-Fix und lokale Gesamt-100-QA

**06.11.2026. NUR TEST. Nicht als WordPress-/PSERC-/K0-LIVE-PASS behandeln.**

## Paket
- Vollständiges Plugin: `protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/PLUGINS/INSTALLATIONS_PAKETE/PFERDEATELIER_PSTE_0.57.144.15_GESAMTTEST_NUR_TEST.zip`.
- SHA256: `7a025006025907f54533c4c24a77b3d243e7f019ccd78f5ac04309045ea86d8d`.
- Git-Blob (Soll): `227b41ccdc9415d38314c2c5389f0dc72fba64c7`.
- 629499 Bytes, 121 eigentliche Dateien und 4 unveränderte Verzeichniseinträge. Aus kompletter 0.57.144.14 zusammengestellt. Exakt **vier** bereits bestehende PHP-Dateien geändert: `class-pste-mini-workflow.php`, `class-pste-repository.php`, `class-pste-admin.php` und Plugin-Hauptdatei (Versionsstand). **117/121** Dateien inhaltsgleich. K0 und PSERC gar nicht im Plugin.

## Ursachen
- 0.57.144.13-Fix weiterhin enthalten: sechs alte erneute Sprachtitelanforderungen werden durch gültigen quellengebundenen Titelbeleg nicht mehr ausgelöst; drei veraltete Rezension-/Titelbeleg-Konflikte akzeptieren nur einen eigenständig gültigen neuen Titelbeleg.
- 0.57.144.14-Fix weiter enthalten: MINI bietet für geänderte Versionen den vorhandenen Wiederanlauf-Knopf ohne erneuten Import.
- **Neu 0.57.144.15:** JA-Entscheid aus dem authentifizierten MINI-Import wird **zusammen mit der originalen Suchfrage** als bestehender Relevanznachweis an denselben Relevanzowner gebunden. Der eigene bestehende Relevanzprüfer konsumiert diesen Beleg, statt die externe fachliche JA-Entscheidung erneut anzufordern. **Keine Artikel-/Kategorie-/Produktionsfreigabe durch bloßes JA.**
- Laufende Wiederprüfungen: bereits erledigte 87er-Schlüssel dürfen bei ausdrücklich versionsbedingt erneutem Lauf nochmals eingeplant werden; gewöhnliche Wiederholung vermeidet Doppelarbeit, andere laufende Themen bleiben erhalten.

## Tatsächlich ausgeführte lokale Prüfungen
- **100 echte Originaleinträge** aus `PFERDEATELIER_MINI_100_ENDSTAND_20261106.json`: 87 JA, 9 VIELLEICHT, 4 NEIN; 97 Titel, 10 zweite Ideen.
- 87/87 originalen Ersttitel samt unveränderter ursprünglicher Suchfrage anerkannt; keine erneute Titelanforderung. **87** fehlende Titelbelege und **87** manipulierte ursprüngliche Suchfragen zurückgewiesen.
- 87 MINI-JA tatsächlich in bestehender Repository-Funktion mit isoliert nachgestelltem WP-Datenbankspeicher gespeichert; wiederholter Aufruf erzeugt keine neuen Schreibvorgänge; gefälschte Herkunft/Quellfrage wird blockiert. Keine Beitrags-/Kategorie-/K0-Schreibvorgänge.
- 87/87 durch **echte bestehende Relevanz-Gate-Klasse** mit quellengebundenem JA-Nachweis bestätigt; 13 nicht-JA nicht akzeptiert; 87 fremde Suchfragen können den Beleg nicht wiederverwenden.
- Echtes MINI-`forwardToPlan()` im isolierten WordPress-Stubszenario: 87 Titel schon im vorherigen Speicherstand, daher 0 neu geschrieben; 87 vorhandene JA samt Relevanzbeleg an vorhandenen Owner, 87 zur erneuten Prüfung eingeplant; 9 VIELLEICHT + 4 NEIN + 10 zweite Titel nicht freigegeben.
- Warteschlangentest: 40 vorher als DONE, 47 pending → nach Versionswiederanlauf 87 pending, 0 verlorene; erneuter normaler Queue-Aufruf ohne Duplikate; fremde laufende Arbeit bleibt erhalten.
- Bestehende Planungs-Gate-Klasse mit künstlichem Bestandsinventar: echtes gleiches SEO-Keyword geblockt; bestehender aktiver Titel deckt Quelle ab → geblockt; fremdes Thema → frei. **Keine** breite Freigabe der zwölf echten Planungsfälle, deren aktueller WordPress-Bestand fehlt.
- 16 zusätzliche Sprach-/Altbeleg-Gegenproben PASS; **83/83 PHP-Syntaxprüfungen PASS**; ZIP-Inhalt exakt mit getesteten Dateien abgeglichen.

## Grenzen / NEXT ACTION
Das ist eine **lokale Simulation**, kein echter WordPress-/MySQL-Betrieb. Die 50 offenen Kategoriezuordnungen müssen im bestehenden Redaktionsbüro gesammelt werden, nicht zu fiktiven Zielkategorien umgedeutet. 12 Planungssperren müssen in echter WP-Bestandsaufnahme durch den einzigen bestehenden Planungsowner geklärt werden; echte Dubletten nie einfach entsperren. Zwei andere Fälle ebenfalls offen. Die lokalen Titel-, Übergabe- und Quellenprüfungen begründen noch keinen PSERC-/K0-/LIVE-PASS.

**Nächster benutzbarer EINMALIGER Schritt:** Nur diese eine TEST-ZIP installieren, zuvor keine ältere .13/.14; WordPress → SEO Themenengine → Themenprüfung → **Bereits übergebene Titel nach Plugin-Update erneut prüfen**. Danach in Produktion die **Gesamtdiagnose herunterladen** und genau diese neue JSON auswerten. Keine neue Recherche, kein Neuimport, keine Produktionswelle, kein K0-/LIVE-Eingriff.