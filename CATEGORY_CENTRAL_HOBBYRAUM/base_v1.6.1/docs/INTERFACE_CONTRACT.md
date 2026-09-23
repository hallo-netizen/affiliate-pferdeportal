# Schnittstellenvertrag V1.6.1 – HARDLOCK

- Kategorie-/Research-Schema bleiben Version 1.4; Global-Coverage Schema 1.0.
- Alle aktiven Pakete tragen `master_contract_id=ALLGEMEINGUELTIGER_KATEGORIE_MASTER_016_WORKFLOW_HARDLOCK`.
- Project Contract verlangt `target_market` und `language_code`.
- Initial-, Global-Gap- und Final-Review benötigen: Status, `review_scope_sha256`, UTC-Zeit, Zusammenfassung, `approved_by_user_id`, `receipt_signature_sha256`.
- Review-Quittungen werden nur serverseitig über den kontrollierten Adminpfad signiert.
- Global-/Research-Paketmarkt und Sprache müssen exakt mit dem gebundenen Source-Draft übereinstimmen.
- Keine WordPress-/HivePress-Content-Writes.
