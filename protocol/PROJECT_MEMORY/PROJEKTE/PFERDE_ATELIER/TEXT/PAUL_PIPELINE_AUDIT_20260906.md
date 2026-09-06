# PAUL PIPELINE AUDIT – PRÜFKARTE 2026-09-06

ROLLE: READ-ONLY-Prüfkarte / keine zweite Fehlerwahrheit.

QUELLE:
Nutzerübergebener Paul-Bericht „PBone Pipeline Inspection“, 2026-09-06.
Der beliebige Beispielartikel („Duschhocker kaufen“) dient nur als Testdatensatz; geprüft wurde unser System-/Plugin-/Workflowtyp.

AUTORITÄT:
- aktueller TEXT-Stand → CURRENT_STATE.md
- aktuelle Arbeit → HOBBYRAUM.md
- Fehlerwahrheit → FEHLERREGISTER → autoritative Fehlerquelle
- Ziel → ZV-TEXT-001

## KERNAUSSAGE

Die wichtigste neue Fehlerklasse ist nicht „alte Regel = schlecht“, sondern:
**zwei jeweils sinnvolle Module/Gates können gemeinsam widersprüchlich werden, wenn sie verschiedene Zustände desselben Artefakts erwarten oder nicht exakt dasselbe Artefakt prüfen/weitergeben.**

Das passt direkt zu B01:
gültiger semantischer Kategorievertrag vs. nachträglich verlangte numerische WordPress-ID vor realem PPM.

## PRIORITÄT A – VOR / INNERHALB DES AKTUELLEN 107007→107008-ZIELS PRÜFEN

### Vertrags-/Gate-Kollisionen
- F1 – Router erzeugt Wert, den Schema nicht akzeptiert.
- F2 / A6 / A12 – Gate-Reihenfolge bzw. unresolved/resolved HTML widersprüchlich.
- F7 / A7 – Tabellenpflicht kann für betreffenden Artikeltyp unerfüllbar sein.
- F9 – Artikeltyp-/Affiliate-Vertrag kann unerfüllbar sein.
- A5 – Gate prüft falsche Schemaform.
- A9 – Blocker nach Vorverarbeitung teilweise nicht mehr erreichbar.
- A11 – derselbe „validated content hash“ bezeichnet zwei verschiedene Artefakte.

### Artefakt-/Render-Konsistenz
- A1 – gemischte Datenformen können Inhalt verlieren.
- A2 – Sanitizer entfernt bewusst erzeugte Tabellenattribute.
- A3 / A8 – TOC verändert/verschiebt Struktur vor nachgelagerten Prüfungen.
- A10 – Sanitizer verändert rel-Attribute nach/gegen Affiliate-Regel.
- A14 – erzeugter Vergleichs-Platzhalter ohne Resolver.
- A15 / A16 – Placeholder-/Linkfehler können Warn-/Strict-Netz umgehen.

### Research/Test-Parität
- F4 – Cannibalization-Weg nicht real durch aktuellen Test abgedeckt.
- F5 / F6 / A37 – Testsuite/Abhängigkeiten liefern kein vollständiges Produktionssignal.
- L2 – Research-Gate laut Paul-Modell nicht zwingend aktiv.

## DIREKTER STARTMASTER-BEFUND AUS HEUTIGEM CODE

Fachvertrag:
„PASS-Reuse nur bei identischem, hashgebundenem Input/Vertrag.“

Aktueller Handoff:
- jede Stage hat `input_sha256`;
- bei Nicht-PPM-Stufen wird technisch nur 64-Hex-Format erzwungen;
- keine generische Bindung beweist dort, welches konkrete Artikelartefakt der Hash bezeichnet oder dass Vor-/Nachstufe dieselbe Artefaktkette verwenden;
- PPM ist enger und bindet `input_sha256` explizit an `final_article_sha256`.

WICHTIGE EINORDNUNG:
Dieses lose Nicht-PPM-Verhalten bestand schon auf den belegten 7/7-Ständen `d841ed…` und `de21f6…`.
Daher aktuell **latente Vertrags-/Paritätslücke, nicht als Ursache des B01-Livefehlers belegt.**

## PRIORITÄT B – REAL, ABER NICHT IN AKTUELLEN B01/#140-FIX MISCHEN

- A17–A22 – Recovery/Fill/Budget/Cost/Yield/Bookkeeping.
- A4 – Responsive Images.
- A28 – Reader-Performance/Pagination.
- N1–N3 – Routing-/Leercorpus-Notizen.

Diese Punkte getrennt bearbeiten, wenn der aktuelle Produktionsweg wieder bis 107008 trägt.

## PRIORITÄT C – WORDPRESS/PUBLIC NACH DEM AKTUELLEN ZIEL

Aktueller ZV-TEXT-001 endet bewusst bei 107008 **vor Publish**.

Deshalb jetzt NICHT in PR #140 mischen:
- A13 – WP-Sync verliert internal_links/infoboxes.
- A23–A27 – Canonical/Sitemap/Reader/Links.
- A29 – Publish-Sync ohne Validierung.
- A30 – Draft→Approve→Publish Kurzschluss.
- A31 – record_id/post_id-Verwechslung.
- A32 – Bild-URL-Umschreibung nach Gate/Hash.
- A33 – fehlender WP-Create-Weg.
- A34 – done trotz fehlgeschlagenem Sync.
- A35 – BLOCKED-Draft öffentlich/Sitemap.
- A36 – approved-State downstream abgelehnt.
- L4 – kein WP-Ziel → terminal FAIL.

Diese Befunde sind sicherheits-/produktionsrelevant, aber **nicht Teil der jetzigen 107008-Wiederherstellung**, solange kein früherer Vertrag sie direkt beeinflusst.

## HARTE ARBEITSREGEL

1. Kein 41-Punkte-Sammelfix.
2. Erst Wirkungskette des aktiven 107007→107008-Wegs.
3. Pro Kandidat: konkretes Eingangsartefakt → Prüfung → Ausgangsartefakt → nächster Verbraucher.
4. Nur reproduzierter Widerspruch wird aktueller Fehlerkandidat.
5. Historische Fehlerquelle gegenprüfen.
6. KISS-Fix einzeln.
7. Bestehender Regressionstest danach.
8. Echter 7/7-Lauf bleibt Produktionsbeweis.
9. WordPress/Public-Funde separat nach Wiederherstellung des 107008-Ziels.
