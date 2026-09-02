# AFFILIATE-ZENTRALE — MANUELLER DATEIIMPORT / VERWORFENER ZWISCHENWEG

Stand: 2026-09-02
Branch: `affiliate-release-current`
Status: `SUPERSEDED / DO NOT IMPLEMENT / CSV ORACLE ONLY`

## Verbindliche Korrektur

Dieses Dokument autorisiert **keinen** manuellen DS24-Runtime-Betriebsweg mehr.

Der frühere Inhalt hatte die reale Digistore24-Kontrollliste/CSV fälschlich von ihrer verbindlichen Rolle als **Testoracle** zu einer Runtime-Autorität umgedeutet. Das widerspricht dem gebundenen Zielvertrag und wurde als `AFF-ERR-015` im verbindlichen Fehlerregister erfasst.

Ab jetzt gilt wieder uneingeschränkt:

- die DS24-Kontrollliste/CSV dient ausschließlich zum Read-only-Vergleich und zur Prüfung der automatisch gewonnenen Partnerschaftsmenge;
- kein CSV-/Dateiupload darf DS24-Partnerschaften, Marketplace-Cache, Creative- oder Output-Autorität für den Runtimebetrieb erzeugen;
- ein Dateiimport darf nicht als Ersatz für die fehlende automatische Partnerschafts-Discovery dienen;
- `listMarketplaceEntries`, `getAffiliateCommission(all)` und `validateAffiliate` bleiben als automatische Discovery ungeeignet, solange kein neuer realer Gegenbeweis vorliegt;
- Ziel bleibt eine unterstützte read-only Affiliate-seitige automatische Discovery aller real genehmigten Partnerschaften ohne Vorfütterung der 18 Kontroll-IDs.

## Historischer Testwert

Die früheren technischen Dateiimport-Tests bleiben ausschließlich historische Gegenfall-Evidence. Sie dürfen weder einen Runtime-Betriebsweg noch einen Release-/Live-PASS begründen.

## Source-Folge

`class-ppar-universal-import.php` und `class-ppar-manual-import-guard.php` dürfen nicht Bestandteil des kanonischen Runtime-Source sein, soweit sie den verworfenen DS24-Datei-Autoritätsweg bereitstellen. Die KISS-Navigation und die zentrale `Partner & Einnahmen`-Analytics bleiben davon unabhängig.

## Weitere Sperre

Zusätzlich gilt `AFF-ERR-016`: Kein neuer Installer und kein Live-Replace, solange die exakte live installierte 6.71-Quellbasis nicht bytegenau verfügbar und als direkte Source-Autorität gebunden ist. Keine Rekonstruktion aus älteren Repository-Ständen oder Protokollen.
