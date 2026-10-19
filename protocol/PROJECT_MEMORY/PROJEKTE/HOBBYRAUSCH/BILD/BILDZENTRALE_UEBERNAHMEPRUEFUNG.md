# HOBBY DEPOT – BILDZENTRALE – ÜBERNAHMEPRÜFUNG

STAND: 2026-10-19
STATUS: GROBPRÜFUNG ABGESCHLOSSEN / SOURCE-AUDIT OFFEN

## Referenzquelle

Allgemeine Bildzentrale:
- Version **2.7.6**
- Pferde-Plugin-Slug: `pferde-atelier-bildzentrale`
- Hauptdatei: `pferde-atelier-bildzentrale.php`
- Referenzartefakt: `ALLGEMEINE_BILDZENTRALE_2.7.6_RASSEN_BATCH_AUTOMATIK_INSTALLIEREN.zip`
- Release-SHA-256 laut allgemeiner Current: `12edc4405560ac3b149cf76a0b6e65694337b1533c0ea5e3a777d3b6c98ccbf0`
- späterer Read-only-Source-Scan: eine PHP-Quelldatei, 383603 Bytes, SHA-256 `984a8d4da6594ffa93e6d4024b57cc6c22c7d1fbfec398177a19b0490c20d89b`

Die unterschiedlichen Hashes beziehen sich auf ZIP vs. Hauptdatei und sind kein Widerspruch.

## Allgemeingültig übernehmbar

Die Kernfunktion ist ausdrücklich projektübergreifend angelegt:
- Medien-/Featured-Image-Verarbeitung;
- Beiträge;
- WordPress-Taxonomien;
- CPT-Heros;
- optionale HivePress-Taxonomien;
- externe Bildprovider;
- Profile;
- Import/Export;
- Readback-Fallback;
- Schutz bestehender Bilder.

## Bekannte Pferde-Altlasten

Aus der 2.7.2–2.7.6-Entwicklung belegt:
- Rassen-Hero-Profil/Migration;
- `pa_breed`;
- 21:9-Rassen-Hero-Sonderweg;
- Prompt/Framing für vollständige Pferdemotive;
- serieller 10er-Rassenbatch.

Zusätzlich nach Nutzerfestlegung zu entfernen:
- **Bildertrommel**.

## Source-Audit sobald Bytes gebunden sind

Pflichtsuche mindestens nach:
- `pa_breed`
- `pferd` / `horse`
- Rassen-/Breed-Bezeichnern
- fest codierten Term-/Taxonomie-IDs
- Pferde-Domains/-URLs
- projektgebundenen Prompttexten
- Rassen-Batch-/Queue-Handlern
- Bildertrommel-/Rotation-/Random-Logik
- alten Projektoptionen/Transients
- projektspezifischen Adminlabels

## Ziel für Hobby Depot

Kein neuer Kernaufbau. Nur:
**allgemeinen 2.7.6-Kern behalten + Pferde-Sonderlogik entfernen + Hobby-Depot-Konfiguration binden.**

Keine Änderung am bestehenden Bildbestand ohne eigenen Apply-Auftrag.
