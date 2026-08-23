# Verbindlicher Production Package Full Downstream Release Gate V2

## Hardlock
`FINAL` ist eine technische Zustandsaussage und darf nicht durch Dateibenennung vorweggenommen werden.

Eine Produktionsdatei darf nur dann in den Nutzer-Download / die aktuelle MASTER übernommen werden, wenn `FINAL_RELEASE_GATE=PASS` vorliegt.

## Pflichtprüfungen vor FINAL
- keine selbst erzeugte `canonical_article_id`
- `plan_slot == sha256("pserc-plan-slot-v2|" + canonical_article_id)`
- kanonischer Plan liefert exakt einen Treffer
- Kategorie und Beitragsart stimmen mit diesem Treffer überein
- `source_hashes` enthält den von `PPM679_Storage` tatsächlich gespeicherten Fact-Pack-Hash
- reale PPM-6.7.9-Content-/Structure-/Source-/Link-/Category-/Write-/Readback-Gates mit exakt dem Kandidatenpaket PASS
- PSERC Envelope PASS
- Supervisor Authentizität PASS
- Supervisor Full Validation PASS
- PSERC-PPM Bridge PASS
- PPM-Endstatus exakt `NORMAL_DRAFT_END_TO_END_READBACK_PASS_AWAITING_USER_CONTENT_REVIEW_NO_PUBLISH`
- genau erwartete Draft-Anzahl
- `publish_allowed=false`

## Mechanische Sperre
Das Werkzeug `final_release_gate.py` erzeugt die auslieferbare `...FINAL_VERIFIED.json` **erst nach** vollständigem PASS. Bei einem fehlenden Gate wird keine Delivery-Datei erzeugt.

## Dynamische Live-Prüfung
Der lokale Full-Downstream-PASS ersetzt nicht die serverseitige Live-State-Prüfung. Er verhindert statische Paket-/Vertrags-/Validatorfehler vor dem Upload. Der Server darf weiterhin bei echtem Live-State-Delta fail-closed blockieren.
