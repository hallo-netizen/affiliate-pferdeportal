# Verbindlicher Production Package Identity Guard V1

Vor JEDEM Workflow-Supervisor-Signing und vor JEDEM finalen Produktionspaket ist `production_package_identity_guard.py` auszuführen.

Der Guard ist fail-closed und besitzt keine Schreibautorität auf Redaktionsplan, WordPress, READY-Snapshot oder Artikelinhalt.

Verbindliche Invarianten:

- `canonical_article_id_generation_allowed = false`
- Quelle der ID: kanonischer vollständiger PPM-Redaktionsplan
- Lookup-Schlüssel: bestehender READY-`plan_slot`
- Trefferanzahl: exakt 1
- `category_slug` exakt gleich
- `article_type` exakt gleich
- Rückprüfung: `SHA256('pserc-plan-slot-v2|' + canonical_article_id) == plan_slot`
- erst nach PASS: Supervisor-Signatur

Ein Builder, der diese Guard-Ausgabe nicht als PASS belegt, darf kein signierbares/finales Produktionspaket ausgeben.
