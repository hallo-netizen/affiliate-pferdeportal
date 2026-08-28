# ARBEITSPROTOKOLL STARTMASTER0097 – Skalierbare Titelverteilung mit Published-/PSERC-Parität

## Ziel
Breite automatische Titelerstellung ermöglichen, ohne Titelqualität, Longtail-Autorität, Dubletten-/Kannibalisierungsschutz, Artikelinhalt oder Design zu lockern.

## Ursachen
1. PSTE 0.56.22 reservierte Skeletons faktisch global statt nur im relevanten Rolling Window 8; 500er-Stress: 31 PASS / 469 REVIEW.
2. Der PSTE-Allocator kannte den bereits veröffentlichten PSERC-Beratung-Phrasenbestand nicht.
3. Die spätere PSERC-Sortierung konnte die von PSTE geprüfte Nachbarschaft verändern.
4. PSERC 0.28.11 leitete `semantic_identity_title` vom sichtbaren/allocation Titel ab; Titelhilfswörter konnten dadurch die semantische Dublettenprojektion beeinflussen.

## Rootfix
- PSTE 0.56.23: Skeleton-Schutz exakt rolling 8, Published-Phrasenbestand read-only einbezogen, PSERC-Reihenfolge im Audit gespiegelt.
- PSERC 0.28.12: stabile Pre-Title-Semantikidentität; sichtbarer Titel ist keine semantische Identität mehr.
- Unzulässige Titeloberflächen werden weiterhin vom bestehenden Qualitätsgate verworfen. Das Thema bleibt erhalten; bei fehlender sicherer Alternative `REVIEW_REQUIRED` fail-closed.

## Vollständige lokale Positiv-/Negativprüfung
- Source: PASS.
- Installer frisch entpackt und byte-identisch: PSTE 225/225, PSERC 122/122 PASS.
- PHP-Lint Source/Re-Extract: PSTE 73/73, PSERC 40/40 PASS.
- Realistischer Pferde-40er: 40/40 PASS, 0 REVIEW.
- 500er Skalierung: 500/500 PASS, 0 REVIEW, keine Rolling-/PSERC-Reorder-Skeletonkollision.
- Published-Worst-Case: 18 belegte Phrasenfamilien, 40/40 PASS, 0 Kollisionen.
- Qualitäts-Negativfall Sicherheitswesten: 6 unzulässige Oberflächen werden verworfen, 23 gültige bleiben, 0 ungültige Auswahl.
- Manuelle Titel und Nicht-Beratung byte-identisch.
- Kein sicherer Alternativtitel => REVIEW_REQUIRED, Kandidat bleibt erhalten.
- Gleicher SEO-Longtail mit zwei völlig verschiedenen Titeln => beide BLOCKED_DUPLICATE identisch.
- Unterschiedlicher Longtail => PASS; Broad-Legacy unbekannt => fail-closed blockiert.
- Current-/Published-Phrasendubletten => REVIEW_REQUIRED.
- Exact-Five positiv PASS; Contentfeld, Designfeld und Beratung-Fragetitel negativ BLOCKED.
- Published-Reader SELECT-only, kein `post_content`, kein Write.
- Produktionspaket-Boundary-Guard PASS.

## Schutz
Keine Änderung an Artikelinhalt, Artikelstruktur-/Qualitätsregeln, Textmaschine, PPM 6.7.9, LanguageTool, Affiliate-Ausgabe, Design, Auto-Publish oder DataForSEO-/Target-Keyword-Autorität.

## Release-Artefakte
- MASTER SHA-256: `409ce2f9ca9123f1821a393db0570b4f7d3fa8047ffbee7c8a173e13f15d7944`
- PSTE 0.56.23 SHA-256: `0905c7e38527121e18fedac887270c643a97e40f9925c492dc45f7b730e98e34`
- PSERC 0.28.12 SHA-256: `c3ba24f336749a509e0eb462e44ce060c1d56dd38ad36a656a7f7d64007d71d0`

Status: **LOCAL FULL WORKFLOW + RE-EXTRACT PASS; INSTALLATION PENDING.**