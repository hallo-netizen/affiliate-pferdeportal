# Affiliate Router 6.72.180 – version-only repack local proof

Date: 2026-10-02
Basis: exact 6.72.179 locally proven functional code
Version: 6.72.180
Plugin files: 27
PHP files: 21
Source manifest SHA-256: 96aa0861a05d7444776418b6f567bbff30272fb30426d0b8c81a1ae02282e1b9
Installer SHA-256: 5fb0dbfe6c92e6e8df40c3dd206a519d228a04c890affd7a3fb37f6d1749a2f5

## Delta from 6.72.179
Only:
- pferdeportal-affiliate-router.php: plugin header Version and VERSION constant 6.72.179 -> 6.72.180
- readme.txt: one 6.72.180 version-only release note

No functional PHP logic changed.

## Direct local proof on exact 6.72.180 ZIP
The ZIP was extracted fresh and the real plugin class was loaded with only the final bootstrap invocation disabled for direct method probing. Production methods were executed directly.

Scenario unique: 37/37 PASS.
Scenario duplicate hierarchical slug: 37/37 PASS.
Combined: 74/74 PASS.

Covered positive/negative cases include:
- Schabracken real hierarchy = category.
- Sattel real hierarchy = hub2.
- page:<ID> and page:<slug> resolve to the same real target.
- foreign slug rejected.
- duplicate hierarchical slug fails closed.
- real nested WordPress target URL confirms Schabracken.
- mismatched real URL does not confirm Schabracken.
- Schabracken category selects product_after_category_tiles.
- hub2 selects hub_after_cards.
- second target Pferdedecken resolves independently.
- automatic wrong target URL does not select Schabracken.
- unknown portal URL fails closed to non-ready.
- fixed duplicate slug fails closed.
- exact ID remains valid even with duplicate slug.
- plugin code is byte-exact after restoring the disabled bootstrap line.

PHP lint: 21/21 PASS on shipped PHP files.
Packaged plugin contains exactly 27 files.

## Performance preservation
6.72.180 is version-only relative to 6.72.179. No runtime, cache, provider, eBay, Idealo, GTIN, housekeeping, ranking, rendering or frontend logic changed.

## Status
LOCAL POSITIVE/NEGATIVE PROOF PASS.
release_allowed remains false until the separately required WordPress/MariaDB full gate is completed.
