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

### Nachgewiesener 4a-Anlass
Der aktuelle System-4-Ausgang ist weiterhin speziell gebunden:
- `handoff_transport.py` verlangt exakt sieben Artikel;
- `handoff_transport.py` verlangt für jeden Artikel `article_type == Beratung`;
- `batch_gate.py` setzt `next_required=SIGNED_WORKFLOW_RELEASE`;
- der aktuelle System-4-Ziel-/Handoffvertrag arbeitet dagegen mit `signing_deferred=true`, deaktivierter Signaturprüfung und direktem WordPress-Import.

Damit sind Universalität und ein eindeutiger Endpfad noch nicht bewiesen.

### Historische Sackgassen, die 4a nicht wiederholen darf
1. H7/H8: starke Ein-Tür-Sicherheit, aber viele Räume/Tokens/Receipts/Packages und dadurch neue Übergabeprobleme.
2. Signer-/Producer-Schleifen: derselbe fehlende Anschluss wurde unter neuen Namen wiederholt gesucht; Erklärung wurde mit Fortschritt verwechselt.
3. Alte Workflowgenerationen: neue Runner/Gates/Signer als Reaktion auf einzelne Blocker führten zu Schutzarchitektur statt Produktion.
4. Chat-Drift: textuelle Verbote reichten nicht; der ausführende Chat übernahm trotzdem Planungshoheit.
5. System-4-schlechter 7er-Lauf: zu schwache Recherche-/Fact-Pack-Bindung plus artikelübergreifende Textschablonen; Einzelartikelprüfer allein reichten nicht.
6. Falsche Autoritätsinterpretation: statische Hinweise wurden zeitweise stärker gewichtet als der tatsächlich gebundene aktuelle Prüferzustand.
7. Alte 7er-/Batch-Spezialisierung: feste Stückzahlen und konkrete Artikelarten verhindern universelle Produktion.

### Konsequenz
4a baut keine neue Fachmaschine. Es untersucht ausschließlich, ob Universalität, Außenabschottung, Same-Article-Reparatur und finaler Dateiausgang in einer einzigen Laufzeitautorität zusammengeführt werden können.

### WordPress-/Ausgangsanforderung
Aktuell verifizierter System-4-Zielvertrag nennt als direkten Ausgang JSON / `application/json`, `WORDPRESS_DIRECT_IMPORT`, `Portal SEO Editorial Plan Compiler 0.28.23`, PPM 6.7.9, `direct_wordpress_upload_ready=true` nach allen PASS-Prüfungen, keine erforderlichen Downstream-Komponenten und `publish_allowed=false`.

Die finale 4a-Struktur darf die heute in System 4 hardcodierten `7` und `Beratung` nicht übernehmen. Pro Artikel müssen Identität, Metadaten, finaler Body/Hash, Produktionskontext und echte Prüfbelege erhalten bleiben.

### Teststatus
Noch kein 4a-Code-PASS. Büro-/Ziel-/Hobbyraumstruktur ist Dokumentation und keine Produktionsfreigabe.
