# Universal Product Comparison 0.7.0 – Hard Local Release Receipt

Stand: 2026-09-08
Status: REJECTED NACH WORDPRESS-LIVEFAIL PV-LIVE-001

Release artifact:
`universal-product-comparison-0.7.0-prototype.zip`

SHA-256:
`b6563940f96d0e9134109779f8046b5e8b9e1109bc9965d9d01deb5c75ed610d`

Geprüfter Abschnitt:
`SEO ↔ Produktwissen → Vergleichbarkeit → Nachfrage/Kannibalisierung → Dossier → Audit`

PASS:
- PHP lint 31/31
- bidirektionale SEO/Product-Knowledge Discovery positiv/negativ
- direkter A-gegen-B-Fall
- SEO→unbekanntes Produkt = RESEARCH_REQUIRED
- generische Vergleichsanfrage erzeugt keine Produktidentität
- Same-Brand ausgeschlossen
- 0g/50g Vergleichbarkeitsblock
- Dossier-/Profil-Drift fail-closed
- Provider PARTIAL bleibt PARTIAL
- kein Live-Provider ohne Autorisierung
- Planning-Page ohne versteckte Sync-/Materialisierungsaktion
- Writer/Draft-Adminaktion nicht registriert
- 81 reale PSTE-Themen: False-Pair-Guard PASS
- autoritativer PSTE-0.56.25-Installer SHA geprüft
- Product-Knowledge-0.5-Vertrag geprüft
- fertige ZIP frisch entpackt und komplette Suite erneut PASS
- Source ↔ Fresh-ZIP byte-identisch
- ZIP-Wurzel exakt `universal-product-comparison/`

Grenze:
Kein WordPress-Live-PASS behauptet. Kein Writer/Draft/Publish in dieser Prüfstufe.


## REJECT 2026-09-09

Realer WordPress-Lauf:
8 Kandidaten → 16 Provider-Aufrufe / $0.1920 → 0 SEO-PASS / 8 blockiert / 0 Dossiers.

0.7.0 meldete trotzdem grünes PASS.
Dieser Receipt ist dadurch **historisch verworfen** und keine Freigabequelle mehr.
