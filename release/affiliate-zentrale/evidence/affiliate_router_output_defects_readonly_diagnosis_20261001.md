# Affiliate-Zentrale – Read-only Diagnose der gemeldeten Ausgabefehler

Datum: 2026-10-01
Basis: aktueller 6.72.173-Sourcebaum, Head `18e3b21b96554023c8c65d6b628a97211398bee5`
Status: READ_ONLY_DIAGNOSIS / KEIN WEITERER SOURCE-WRITE / PERFORMANCE-HARDLOCK AKTIV

## Harte Regel

Die in 6.72.171 belegten Performance-Optimierungen dürfen weder zurückgebaut noch überschrieben werden.
6.72.172-Housekeeping bleibt ebenfalls erhalten.
Vor jedem späteren Fachfix wird erneut der frische Current-Sourcebaum gelesen und nur das kleinste Delta geschrieben.

## 1. eBay PRIVATE / HivePress – gezählt, aber 0 sichtbar

### Belegter Codepfad

Frontend:
- `ebay_filter_stale_posts()` prüft jedes eBay-PRIVATE-Listing zusätzlich gegen `ebay_private_public_post_allowed()`.
- `ebay_private_public_post_allowed()` blockiert ein eBay-Listing sofort, wenn `ebay_public_checkpoint_allows_private_listing()` false liefert.
- Ein sicherer Public-Checkpoint ist damit eine harte Sichtbarkeitsdecke.

Canonical Public Verify:
- `ebay_run_verify_private_public($settings, $allowed_listing_ids)` baut aus der Candidate-Liste eine `$allowed_map`.
- Für jeden veröffentlichten hp_listing-Post gilt aktuell **vor** Ownership-/Source-Prüfung:
  `if(is_array($allowed_map) && !isset($allowed_map[$id])){continue;}`
- Ist die Candidate-Liste leer, werden dadurch alle veröffentlichten Listings übersprungen.
- Ergebnis: `$public=0`, `$invalid=[]` und die Funktion liefert aktuell `status=pass`.
- Danach kann `ebay_run_commit_public_checkpoint()` einen sicheren Checkpoint mit leerem `private_listing_ids` speichern.
- Ab diesem Moment blendet der Frontend-Checkpoint sämtliche eBay-PRIVATE-Listings aus.
- Die WordPress/HivePress-Taxonomie kann diese weiterhin als veröffentlichte Listings zählen, bis die nachgelagerte Checkpoint-Bereinigung sie tatsächlich auf Draft setzt.

### Bewertung

Dieser Codepfad kann exakt den gemeldeten Zustand **„gezählt, aber keine eBay-Anzeigen sichtbar“** erzeugen.

Noch nicht belegt ist ausschließlich, ob der aktuelle Live-Checkpoint tatsächlich eine leere/ungeeignete `private_listing_ids`-Liste enthält. Die Codeursache selbst ist reproduzierbar und kein Rateschluss.

### Nachhaltiger Rootfix-Korridor

Kein Fail-open und kein Abschalten des Checkpoints.

Der Final-Public-Gate muss zusätzlich beweisen:
- ein veröffentliches, plugin-owned eBay-PRIVATE-Listing außerhalb des Candidate-Sets darf nicht einfach ungeprüft übersprungen werden;
- wenn ein solches Listing nach bestehender Source-/Policy-/Lifecycle-Prüfung weiterhin gültig ist, ist das ein **Candidate-Gap** und der neue Checkpoint darf nicht committed werden;
- echte stale/ended/blocked Listings dürfen weiterhin aus dem neuen Checkpoint herausfallen;
- leerer Candidate darf nur PASS sein, wenn tatsächlich kein weiterhin gültiges PRIVATE-Listing existiert.

Damit wird ein leerer oder unvollständiger Candidate nicht mehr als „sicher“ durchgewunken.

## 2. Banner-Automatik – Schabrackendesigner -> Schabracken

### Belegter Codepfad

`output_classify_for_portal()`:
1. Safety / Veto / manuelle Entscheidungen;
2. Creative-Evidence wird gebildet;
3. generischer Portal-Domain-Test;
4. **wenn kein generischer Domain-Term gefunden wird, Rückgabe `creative_domain_signal_missing`;**
5. erst danach werden reale Portalziele geladen und semantisch gerankt.

Die Zielrangfolge besitzt bereits starke exakte Signale:
- Ziel-Slug gegen Destination;
- Creative-Token gegen Target-Token;
- Teilwort-/Leaf-Abgleich.

Diese Logik wird für ein Creative, das vorher am generischen Domain-Gate stoppt, jedoch nie erreicht.

### Bewertung

Damit kann ein fachlich eindeutiges Creative wie **„Schabrackendesigner“** vor der Prüfung gegen das reale Portalziel **„Schabracken“** auf REVIEW enden.

### Nachhaltiger Rootfix-Korridor

- Safety, negative Fachsignale und Veto bleiben zuerst und unverändert.
- Danach darf ein **eindeutiger exakter Treffer auf ein reales zulässiges Portalziel** selbst als Creative-Fachevidenz gelten.
- Nur wenn kein solcher exakter realer Zieltreffer existiert, greift weiterhin das generische Domain-Gate.
- Keine Sonderregel nur für „Schabracken“; providerneutral und zielkatalogbasiert.

## Abnahmetests für spätere Source-Fixes

eBay PRIVATE positiv:
- gültiges PRIVATE-Listing im erlaubten HivePress-Teilbaum wird sichtbar;
- leerer Candidate bei weiterhin gültigem veröffentlichtem eBay-Listing = FAIL vor Checkpoint-Commit;
- gültig leerer Bestand = PASS.

eBay PRIVATE negativ:
- stale / ended / policy-blocked / manual-blocked / falscher Seller bleibt unsichtbar;
- außerhalb „Private Anzeigen“ bleibt eBay PRIVATE unsichtbar;
- native HivePress-Anzeigen bleiben unverändert.

Banner positiv:
- „Schabrackendesigner“ kann bei eindeutigem realem Ziel „Schabracken“ automatisch READY werden.

Banner negativ:
- fachfremdes Creative bleibt blockiert/review;
- widersprüchliche negative Signale werden nicht durch einen schwachen Zieltreffer überstimmt;
- Veto und Safety bleiben absolut.

Performance:
- keine Änderung der 6.72.171 request-lokalen Frontend-Caches;
- keine neue globale DB-/Term-/Datei-/Netzwerkabfrage;
- eBay-PRIVATE-Zusatzprüfung nur im Hintergrund/Public-Verify, nicht im normalen Portal-Hotpath;
- Banner-Zielbeweis muss vorhandene bereits geladene Target-/Evidence-Daten verwenden.
