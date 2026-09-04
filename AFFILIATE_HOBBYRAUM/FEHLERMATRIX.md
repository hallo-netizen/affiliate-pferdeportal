# AFFILIATE-HOBBYRAUM – VERBINDLICHE FEHLERMATRIX

Regel: Vor JEDEM Lauf gegen alle Einträge prüfen. Bei einem neuen Fehler wird zuerst diese Matrix ergänzt, erst danach darf ein neuer Versuch starten.

| ID | Bisheriger Fehler | Woran er erkannt wird | Verbindliche Gegenregel |
|---|---|---|---|
| AF-001 | STARTMASTER/Textmaschine in Affiliate-Arbeit gezogen | Artikel-/STARTMASTER-Schritt taucht im Affiliate-Run auf | Fremd-Workstreams vollständig sperren |
| AF-002 | Globalen Cloud-Entry-Gate für Affiliate benutzt | Affiliate-Aufgabe wird an fremde Capsule gebunden | Kein Cloud-Entry-/Capsule-Weg im Hobbyraum |
| AF-003 | Lokalen Codex-Branch mit Release-Branch verwechselt | Codex läuft auf `work`, obwohl Release-Identität `affiliate-release-current` ist | Lokaler Branchname ist keine Release-Autorität |
| AF-004 | `git switch affiliate-release-current` verlangt, obwohl Ref lokal nicht existiert | `fatal: invalid reference` | Kein Branchwechsel im Hobbyraum |
| AF-005 | `origin` vorausgesetzt | `origin does not appear to be a git repository` | Kein Remote/Origin voraussetzen |
| AF-006 | `FETCH_HEAD` vorausgesetzt | `FETCH_HEAD is not a valid reference` | Kein Fetch-/FETCH_HEAD-Weg |
| AF-007 | Stalen Codex-`work`-Checkout als kanonisch behandelt | lokale Dateien/Manifest weichen vom Release-Stand ab | Nur explizit freigegebene, vorher gebundene Eingabedateien verwenden |
| AF-008 | Kaputtes Manifest nicht vor Start validiert | SHA-256-Eintrag hatte nur 63 Zeichen | Jede Autoritätsdatei vor Nutzung strukturell validieren |
| AF-009 | 63-stelligen Manifest-Hash als gültigen SHA-256 übernommen | Hashlänge != 64 | Jeder SHA-256 muss exakt 64 Hex-Zeichen haben |
| AF-010 | Symptome umgangen statt Root Cause zu beheben | Branch-Check deaktiviert, danach nächster Guard-Fehler | Erst konkrete Root Cause beheben; keine Kaskade von Bypässen |
| AF-011 | Bereits bestandene PASS-Gates erneut geöffnet | Partner Analytics/Deal Radar/eBay usw. werden ohne Regression neu geprüft | Hash-identische PASS-Gates nicht wiederholen |
| AF-012 | DS24-Automatik/Discovery erneut verfolgt | automatische Partner-/Marketplace-Suche wird Voraussetzung | DS24 automatische Discovery bleibt OUT OF SCOPE |
| AF-013 | Vorhandene DS24-Daten erneut angefordert | CSV/Partnerliste/Screenshots werden nochmals verlangt | Bereits vorhandene Inputs nicht erneut verlangen |
| AF-014 | Architektur/Provider-Scope während Fix erweitert | neue Providerlogik, neue Plugins oder neue Wege ohne Auftrag | Nur die eine Task-Aufgabe; keine Architekturänderung |
| AF-015 | Codex-Artefakt als normal herunterladbar angenommen | ZIP liegt nur in flüchtigem Codex-Workspace | Vor Übergabe sicherstellen, dass Ergebnis auf tatsächlich downloadbarer Oberfläche liegt |
| AF-016 | Lokalen Codex-Commit als auf GitHub vorhanden angenommen | Commit-ID ist über GitHub nicht auffindbar | Push/Persistenz nie behaupten ohne GitHub-Nachweis |
| AF-017 | Base64-/Block-Transfer als Ersatzweg erfunden | viele Textblöcke für eine ZIP | Keine Base64-Übertragung außer ausdrücklich angeordnet |
| AF-018 | Bereits geprüfte ZIP neu rekonstruiert statt saubere Übergabe zu lösen | erneutes Zusammensetzen aus historischen Dateien | Keine historische ZIP-Rekonstruktion |
| AF-019 | Projektweite Suche statt gezielter Task-Dateien | große Repo-/Library-Suchen ohne unmittelbaren Bedarf | Hobbyraum sieht nur explizite Inputs |
| AF-020 | Mehrere Ersatzwege nach einem Fehler ausprobiert | Branch → Fetch → Bypass → Manifest → Rekonstruktion | Fehler => genau eine Root-Cause-Prüfung, dann ein gezielter Fix |
| AF-021 | Download-Problem mit Entwicklungsänderungen vermischt | Übergabeproblem führt zu Source-/Architekturarbeit | Transportproblem bleibt Transportproblem; Source unverändert |
| AF-022 | Falsche Sicherheit behauptet | „kann nicht mehr auftreten“ ohne echten Lauf | PASS nur nach tatsächlich ausgeführter Prüfung behaupten |
| AF-023 | Source/Manifest-Bindung verändert ohne alle Bindungen nachzuziehen | Manifest, Governance und Runner zeigen auf verschiedene Hashes | Bindungen atomar gemeinsam aktualisieren und gegeneinander prüfen |
| AF-024 | Final-/Live-Kandidat-Regeln vermischt | temporäre Live-ZIP und finale Release-ZIP werden gleich behandelt | Live-Kandidat darf gebaut werden; Finalrelease erst nach allen Final-Gates |
| AF-025 | Ein Fehler führte zu Tagen mit Meta-Arbeit statt Zielergebnis | Guard-/Protokoll-/Branch-Arbeit verdrängt die eigentliche Aufgabe | Hobbyraum: 1 Ziel, 1 Inputmenge, 1 Output, kein Meta-Ausbau während des Runs |
| AF-026 | ZIP-Dateiname/Releasekandidat höher als interne WordPress-Pluginversion | WordPress meldet beim Installieren eine niedrigere Version; Header/const/readme stimmen nicht mit Kandidat überein | Vor jeder Live-ZIP zwingend Plugin-Header, const VERSION und Stable tag gegen Kandidatenversion prüfen; neue Version muss über der belegten installierten Vorversion liegen |
| AF-027 | Neue Versionsnummer gewählt, ohne die tatsächlich installierte WordPress-Version als Untergrenze zu verwenden | Kandidat 6.64.2 lag unter der real installierten 6.72.0 | Vor jedem Versionsfix gilt die vom Nutzer/WordPress belegte installierte Version als harte Untergrenze; nächster Kandidat muss exakt darüber liegen, hier 6.72.1 |

## Dauerregel
- Jede neu festgestellte Fehlentscheidung erhält sofort die nächste AF-ID.
- Kein zweiter Versuch, bevor der neue Fehler hier eingetragen ist.
- Die Matrix selbst ist im Lauf read-only.
- Ein Task, der eine bekannte Gegenregel verletzt, wird vor Ausführung BLOCKED.
