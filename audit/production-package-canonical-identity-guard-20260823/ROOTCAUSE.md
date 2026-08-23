# Root Cause – Production Package / canonical_article_id – 2026-08-23

## Beobachteter Live-Fehler
Der Serverlauf mit dem in STARTMASTER0071 erzeugten Boxenmatten-Paket wurde korrekt fail-closed blockiert:

`PSERC_PRODUCTION_TRIGGER_WORKFLOW_SUPERVISOR_BLOCKED`

Untergrund:

`SUPERVISOR_RELEASE_OR_PLAN_ITEM_MISSING_FOR_SLOT`

Es erfolgte kein WordPress-Write und kein Publish.

## Technische Ursache
Der Pre-Supervisor-Builder in STARTMASTER0070 erzeugte `canonical_article_id` unzulässig selbst aus Beitragsart, Titel, Slug und plan_slot:

`canonical_article_id='article:'+sha('Beratung|'+title+'|'+slug+'|'+plan_slot)[:24]`

Dadurch entstand die falsche ID:

`article:c9a5a66b28671525c53358ce`

PSERC definiert den externen `plan_slot` jedoch ausschließlich als domain-separierten SHA-256 aus der bereits existierenden kanonischen Artikel-ID:

`SHA256('pserc-plan-slot-v2|' + canonical_article_id)`

Für die falsche ID ergibt sich:

`ccc4924597e2f831bb20167b69df1261b48651e9ec6ce1cce100d4a7c3eec43b`

Der verbindliche READY-Planplatz lautet aber:

`a574700d0b94f6e31fe6a87743497009210e04816a7d7c8236a6b40ac04b8a7f`

Im kanonischen PPM-Redaktionsplan ist für genau diesen Slot bereits die korrekte Identität vorhanden:

`article:2d2f4c0ece3dc16e52a378c5`

Rückrechnung:

`SHA256('pserc-plan-slot-v2|article:2d2f4c0ece3dc16e52a378c5')`

=`a574700d0b94f6e31fe6a87743497009210e04816a7d7c8236a6b40ac04b8a7f`

## Warum der Fehler möglich war
Die produktive PSERC-Prüflogik war korrekt und blockierte den Fehler. Die Lücke lag außerhalb des Plugins im ad-hoc Paketbuilder: Vor der Signierung existierte kein obligatorischer lokaler Guard, der `canonical_article_id` gegen den kanonischen Plan auflöste und die Rückrechnung auf `plan_slot` verlangte. Dadurch konnte ein formal signierbares, aber identitär widersprüchliches Paket erzeugt werden.

## Dauerhafte Behebung
Ab STARTMASTER0072 gilt mechanisch:

1. `canonical_article_id` darf im Produktionsbuilder niemals generiert, aus Titel/Slug/Keyword/Intent abgeleitet oder frei gesetzt werden.
2. Eingangsautorität ist der bestehende `plan_slot` aus dem READY-Handoff.
3. Der Guard durchsucht den kanonischen vollständigen Redaktionsplan und muss exakt eine `canonical_article_id` finden, deren PSERC-V2-Token dem Eingangs-`plan_slot` entspricht.
4. Kategorie und Beitragsart des kanonischen Slots müssen ebenfalls exakt zum Handoff passen.
5. Die gefundene ID wird rückwärts erneut auf denselben `plan_slot` gehasht.
6. 0 Treffer, >1 Treffer, Kategorie-/Typabweichung oder ID-/Slot-Abweichung führen vor Signierung zu `IDENTITY_GUARD_BLOCKED`.
7. Erst nach Guard-PASS darf der Workflow-Supervisor-Release signiert und ein Produktionspaket ausgegeben werden.

## Scope / Nicht geändert
- Redaktionsplan: unverändert
- READY-Bestand: unverändert
- Planplatz: unverändert
- Artikelinhalt: byteidentisch
- Fact-Pack: unverändert
- Quality-Binding: unverändert
- PSTE: unverändert
- PSERC 0.28.5: unverändert; keine neue Plugin-Reparatur nötig
- PPM 6.7.9: unverändert
- Auto-Publish: weiterhin verboten

Die Korrektur betrifft ausschließlich die externe Produktionspaket-Identitätsbindung und deren zwingenden lokalen Guard.
