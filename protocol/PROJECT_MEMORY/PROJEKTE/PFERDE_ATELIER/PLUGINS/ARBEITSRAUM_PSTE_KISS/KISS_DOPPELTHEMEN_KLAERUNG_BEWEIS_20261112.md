# KISS: Zentrale Recherche – Titelgleichheit ist kein Dublettenbeweis

**Unverändert:** PSTE .45, PSERC .69, bisherige zwei Arbeitsänderungen und der erste zentrale Widerspruchsfix. **Eine neue Änderung ausschließlich in der bestehenden PSTE_Runner-Methode**, keine neue Klasse, kein neuer Prüfer, keine neue Tabelle, kein PPM- oder K0-Code.

## Originalfehler (belegt)
Die Originalmethode `PSTE_Runner::applyInternalDuplicates()` erklärte zwei deutlich verschiedene Leserfragen im selben Fachbereich sofort als **BLOCKED / Dublette**, wenn sie zufällig den gleichen Arbeitstitel erhielten. Das ist unzulässig, weil MINI den fertigen Titel laut verbindlichem Sollablauf **erst nach** der zentralen Themenentscheidung schreibt. Ein anderer Wortlaut kann auch echte Dubletten verdecken, deshalb darf man den Titelvergleich nicht einfach streichen.

## Kleinster sicherer Unterschied
Die bereits bestehende zentrale Vergleichsfunktion unterscheidet nach der Änderung **ohne zusätzlichen Vergleichsworker**: (a) Quelle/Suchabsicht selbst beweist Gleichheit → wie bisher **BLOCKED**; (b) *nur* der vorläufige Arbeitstitel deutet Gleichheit an → **REVIEW_REQUIRED (KLÄRUNG)**; (c) nach den bisherigen Regeln kein Hinweis auf Überlappung → **PASS**. Beim Ergebnis `REVIEW_REQUIRED` wird **im selben Schritt** das bisherige `planning_readiness_gate` ebenfalls auf `REVIEW_REQUIRED, ok=false` gestellt. Ein solcher Fall erhält **keinen Artikelauftrag**, bis dieselbe zentrale Recherche die Suchabsicht geklärt hat. Keine zweite Entscheidung in PSERC oder K0.

## Warum notwendig und kein zusätzlicher Gate
Exakter Quellort: `Portal SEO Topic Engine/includes/class-pste-runner.php`, vorhandene Methoden `applyInternalDuplicates`, `sameAnswerIntentSignature`, `sameAnswerIntent`. Einziger neu geänderter Quellpfad gegenüber dem zuvor geprüften QA-Arbeitsstand. Die Klassen-/Funktionszahl und die Eingänge anderer Plugins bleiben gleich. Es ist keine Alternative zum vorgeschriebenen echten vollständigen Bestandsvergleich, sondern eine **Korrektur der ursprünglichen Einmalentscheidung**.

## Originaltests und Nachher-Beweis
- Originale Regel: verschiedene Fragen + gleicher Arbeitstitel ⇒ **BLOCKED**, nachher ⇒ **KLÄRUNG**, niemals automatische Freigabe.
- Echte Gleichheit aus Original-Suchfrage ⇒ unverändert **BLOCKED**.
- Gleiches bestätigtes Intent-Cluster ⇒ unverändert **BLOCKED**.
- Unterschiedliche unabhängige Fragen und unterschiedliche Titel ⇒ unverändert **PASS**.
- Auch bei fehlender Kategorie: Klärfall, identische Frage, getrennte Frage geprüft.
- Nachher **11/11** echte Runner-Methodenproben inkl. Wiederholung und **echtem `PSTE_Repository::automaticPoolStatus`**; **126/126** PHP-Dateien syntaktisch gültig; bisherige Entscheidungsregression unverändert; **18/18** Offline-Gesamtsimulation.

**Grenzen:** Die Online-Themenprüfung, permanente Reservierung im aktuellen PPM vor MINI, MINI-nur-Titel, Wegfall des PSERC-Zweiturteils und realer K0→WP-Import sind damit **noch nicht erfüllt**. Die 18/18-Simulation enthält nachgebildete WordPress-/K0-/MINI-Komponenten. **KEIN Installations-ZIP, kein echter Artikel.**

**Verbindlicher QA-Arbeitsstand im privaten Campus:** `KISS_ZENTRALE_DOPPELTHEMEN_KLAERUNG_NUR_QA_20261112.zip`, erneut zurückgelesen mit SHA-256 `2fc5b1bd7f37d5be433da4c19acb99c4bd597ddd948b247abfe254e78e47a974`, 1.830.750 Bytes, ZIP vollständig intakt. Direkter Nachfolger des vorherigen einheitlichen QA-Pakets SHA-256 `2e1e0c839d99bd00deb34cae9dbacb58d34e5aac78b2e885df4d161c2436d63b`.
