# TEXTSYSTEM 4A – PROTOKOLL

## 2026-09-13 – Büroanlage / Architekturprüfung

### Frisch geprüfter System-4-Stand
- PR #238 offen, Draft, nicht gemergt.
- Branch `hobbyroom/system4-true-single-room-v1`.
- Head bei Prüfung: `77c02a9df1745a28157fcc27f65f74e9c4fb1153`.
- Aktueller Status laut System-4-README: BLOCKED bis kompletter aktueller Unittest- und E2E-Nachweis.
- Einzelartikelkern inzwischen: kanonischer State, feste Phasen, Research/Facts/Context/Draft/Fullcheck/Repair, Same-Article-Repair, Content-/Design-Guard intern, echter Production-Fullcheck zentral.

### Wichtige Korrektur gegenüber früherer 4a-Idee
Separate Python-Module sind nicht automatisch echte Handoffs. `content_guard` und `design_guard` werden im aktuellen System-4-Controller direkt als interne Prüfer aufgerufen. Die Existenz mehrerer Dateien allein ist daher kein ausreichender Grund für 4a.

### Korrektur nach Nutzerprüfung
Die aktuell in System 4 noch vorhandene feste Bindung auf sieben Artikel und `Beratung` ist **kein Entscheidungskriterium für 4a**. Diese Bindungen werden in System 4 separat entfernt und dürfen daher nicht als struktureller Vorteil von 4a gewertet werden.

Auch ein Signing-/Direct-Import-Widerspruch ist zunächst ein konkreter Anschlussfehler und kein Beweis dafür, dass die gesamte System-4-Architektur schlechter ist.

### Gültiger 4a-Prüfmaßstab
4a muss gegen ein **bereinigtes System 4** bestehen. Maßgeblich sind nur:
1. echte Laufzeit-/Zustandsautoritäten;
2. echte Übergabegrenzen mit Re-Bindungs-/Interpretationsrisiko;
3. Außenfreiheit bzw. Möglichkeit externer Workflow-Steuerung;
4. Vollständigkeit des Weges Produktionsanstoß → Recherche → Fakten → Text → echte Prüfer → Repair → Querschnitt → WordPress-Datei → Elternchat;
5. unveränderte Inhalts-, Design- und Qualitätsautorität;
6. Flexibilität für neue Beitragsarten;
7. Automatisierbarkeit und Wiederanlauf ohne Neustart des Gesamtprozesses.

### Historische Sackgassen, die 4a nicht wiederholen darf
1. H7/H8: starke Ein-Tür-Sicherheit, aber viele Räume/Tokens/Receipts/Packages und dadurch neue Übergabeprobleme.
2. Signer-/Producer-Schleifen: derselbe fehlende Anschluss wurde unter neuen Namen wiederholt gesucht; Erklärung wurde mit Fortschritt verwechselt.
3. Alte Workflowgenerationen: neue Runner/Gates/Signer als Reaktion auf einzelne Blocker führten zu Schutzarchitektur statt Produktion.
4. Chat-Drift: textuelle Verbote reichten nicht; der ausführende Chat übernahm trotzdem Planungshoheit.
5. System-4-schlechter 7er-Lauf: zu schwache Recherche-/Fact-Pack-Bindung plus artikelübergreifende Textschablonen; Einzelartikelprüfer allein reichten nicht.
6. Falsche Autoritätsinterpretation: statische Hinweise wurden zeitweise stärker gewichtet als der tatsächlich gebundene aktuelle Prüferzustand.

### Konsequenz
4a baut keine neue Fachmaschine. Es untersucht ausschließlich, ob der komplette identische Fachworkflow mit weniger echten Zustands-/Übergabegrenzen und stärkerer Außenabschottung ausgeführt werden kann als ein bereinigtes System 4.

### WordPress-/Ausgangsanforderung
Aktuell verifizierter System-4-Zielvertrag nennt als direkten Ausgang JSON / `application/json`, `WORDPRESS_DIRECT_IMPORT`, `Portal SEO Editorial Plan Compiler 0.28.23`, PPM 6.7.9, `direct_wordpress_upload_ready=true` nach allen PASS-Prüfungen, keine erforderlichen Downstream-Komponenten und `publish_allowed=false`.

Die finale 4a-Struktur muss dieselben fachlich erforderlichen Artikel-/Prüfdaten erhalten. Universalität für Artikelzahl und Beitragsart ist Pflicht, aber kein Vergleichsvorteil gegenüber System 4, weil diese Hardcodes dort separat entfernt werden.

### Teststatus
Noch kein 4a-Code-PASS. Büro-/Ziel-/Hobbyraumstruktur ist Dokumentation und keine Produktionsfreigabe.
