# PPM 6.7.9 – Kategorie-Delta-Kandidat 2026-09-23

Rolle: Arbeits-/Prüfnachweis. Keine zweite Kategorienquelle.

## Quelle

Einzige fachliche Kategorienquelle:
`CATEGORY_INTEGRATION_HOBBYRAUM/PFERDEPORTAL_KATEGORIEN/KATEGORIEN.tsv`

SHA256:
`b1e2bfdab2a07bd1049b972763e8d5a3fc17cf4fe95ad09276a43c77ffca94a3`

Exakte PPM-Ausgangsbasis:
`PORTAL_PRODUCTION_MACHINE_V6.7.9_SIGNED_ARTICLE_TYPE_EXTENSION_ROOTFIX_FINAL.zip`

SHA256:
`acbda93bd1c4292de7aaf88db2195631103991ff508b36c88cb694714818abd1`

## Gebautes Delta

- Produktionskategorien: 1124 -> **1149**
- neue Produktionskategorien: **25**
- Portalslots: 5620 -> **5745**
- neue Portalslots: **125**
- Journal-Slots unverändert: **45**
- Gesamtslots: 5665 -> **5790**
- Produktseiten-Count der internen Portalableitung: 329 -> **334**
- Menu-Items-Count der internen Portalableitung: 1520 -> **1550**

Die PPM-interne Kategorienkopie ist nur technische Ableitung. `KATEGORIEN.tsv` bleibt die einzige fachliche Kategorienwahrheit.

## Interne Kandidaten-Hashes

- complete portal category source SHA256: `250d6a32e9013f55db98e3e545582c45d72397cc302fb43b9b1d8a0b9e68f004`
- hierarchy SHA256: `9be411f90e981ac22f0d2599c09a6eca422ad85adc69d2f9bdefb26d2f5d2a0d`
- canonical plan SHA256: `d2ce7030a8f69aa20af1ec16c0bc004078b63b01350c0c465f31b59fafea8178`
- reconciliation SHA256: `def8444db30ffed9173901e37905f5bf7f7ed619eacd6cca15d7a601e4ee70c2`
- governance SHA256: `97b2546a949c9d266939c4a810902fc92a023e50470fdcd6f67ba8da80a3be6f`
- system inventory SHA256: `d1e9c5535e065c6721945239a7948d58cd5041cf2d17f3e0461a5a7b66caf75e`
- hard-rule registry SHA256: `fb181959cffa3d09810461406a01223b37051156491c54ab203bdd79592c0f1c`
- hard-rule matrix SHA256: `70e4867eaa36607943a847405e8fde1e8fdc99461fb36e75ba445f2bdf9008ed`
- build manifest SHA256: `7ec6966c7c1a9c921bcaa6061cbdeb91b229f508bc93ef59e20a617d7d7d6482`

## Fokussierte Prüfung der neuen Änderung

PASS:
- category source validator: 0 Fehler
- editorial registry validator: 0 Fehler
- system inventory validator: 0 Fehler
- hard-rule coverage validator: 0 Fehler
- 25/25 neue Kategorien besitzen exakt 5 Slots
- neuer realer Slot wird gefunden
- nicht vorhandener Slot wird fail-closed nicht gefunden

Delta-Regression:
- alte 1124 Kategorien: **value-identical**
- alte 5620 Portalslots: **value-identical**
- alte 45 Journal-Slots: **value-identical**

Es wurden keine alten Vollbeweise erneut durchgetestet.

## Kandidatenarchiv

`PORTAL_PRODUCTION_MACHINE_V6.7.9_CATEGORY_25_SLOT125_UNSIGNED_CANDIDATE.zip`

SHA256:
`3063c150f551d0743425b7364248113f6dfd6fc0fc1e63272da85db93d07dc35`

ZIP-Integrität: PASS.

## Einziger verbleibender Blocker

`BLOCKED_BUILD_SIGNATURE_INVALID`

Grund:
Der Build-Manifest wurde für den neuen, intern konsistenten Kandidaten neu erzeugt. Die vorhandene Ed25519-Signatur gehört weiterhin zum unveränderten alten Produktionsbuild und darf nicht erfunden oder ersetzt werden.

Nächster zulässiger Schritt:
**Exakt den Manifest-Stand `7ec6966c...` über einen autorisierten Ed25519-Signierweg signieren; dabei keine weitere Datei verändern. Danach ausschließlich Build-Integrity verifizieren.**

WordPress:
**keine Schreiboperation durchgeführt.**
