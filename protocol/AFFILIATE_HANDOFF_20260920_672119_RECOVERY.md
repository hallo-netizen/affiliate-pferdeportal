# Affiliate – Übergabe Recovery 6.72.119 – 20.09.2026

Diese Datei ist **nur Wegweiser**. Keine zweite CURRENT-/Status-/NEXT-ACTION-Wahrheit.

## Exakter Einstieg

1. Repo `hallo-netizen/affiliate-pferdeportal`
2. Branch `affiliate-release-current`
3. `release/affiliate-zentrale/AGENTS.md`
4. einzige Current-Autorität: `control/release-governance/CURRENT_RELEASE.json`
5. erwartete Current-Generation: **76**
6. erwarteter Current-Blob-SHA: `a6bf31ceff873183758eb10c54320c3c087d0278`
7. Branch-HEAD frisch lesen; bei unveränderter Generation direkt die gebundene NEXT ACTION aus CURRENT ausführen.

## Korrektur gegenüber der Übergabe 10:56

Der frühere Zwang `READ_ONLY_LIVE_STATE_FORENSICS` mit direktem DB-/Options-Readback ist durch ausdrückliche Nutzerkorrektur **abgelöst**. Kein direkter Live-Datenbankzugang ist Voraussetzung der Wiederherstellung.

Die tatsächlichen 6.72.108–6.72.118-Pakete, Affiliate-Büro und Plugin-Updateprotokoll wurden hart gegengeprüft.

## Belegter Recovery-Fehler

Die zwei unterschiedlichen 6.72.118-Pakete widersprechen sich:
- 118-A löscht die 115-/117-Nachweismarker.
- 118-B verlangt genau beide Marker und kann danach `not_applicable` werden.
- 118-B macht nur `idealo_only -> automatic` rückgängig.
- 118-B führt einen bereits laufenden Batch nicht über normale Requests weiter.
- 118-A kann einen vollständigen Artikelplan-Rebuild hinterlassen.

Beide alten 6.72.118 bleiben gesperrt.

## Geprüfter Wiederherstellungskandidat

`AFFILIATE_ZENTRALE_V6.72.119_KISS_EMERGENCY_RESTORE_POSNEG.zip`

SHA-256:
`eb51dcbd19c62dae1a3958d209676926aa02793cb13a8fe64292ed53c3bcea74`

Evidence:
`release/affiliate-zentrale/evidence/affiliate_672119_kiss_recovery_local_20260920.txt`

Prinzip:
- Fachcode exakt 6.72.108;
- nur Hauptdatei + Readme abweichend;
- keine neue Fachlogik;
- keine Inventarlöschung;
- kein globaler Revisionssprung;
- kein neuer Voll-Rebuild;
- Bannerfelder werden nicht verändert;
- nur vorhandene gespeicherte Artikelpläne werden produktseitig repariert;
- fremde manuelle Provider-Modi und fremde Rebuilds bleiben unangetastet;
- ein exakt von 118-A hinterlassener Voll-Rebuild wird gestoppt;
- Recovery läuft in kleinen Paketen auch über normale Requests weiter.

Lokale Abnahme:
- 12/12 Original-118-Fehlernachweis PASS
- 55/55 statisch PASS
- 30/30 Runtime PASS
- Banner-Mutationsprobe fail-closed PASS
- PHP 21/21 PASS
- Fresh-Unpack 26/26 byteidentisch PASS
- Fresh Static 55/55 PASS
- Fresh Runtime 30/30 PASS

## Genau eine NEXT ACTION

**Exakt den oben genannten SHA einmal installieren.**

Danach sichtbar prüfen:
- normale Kategorie-Produkte wieder vorhanden;
- eBay nicht mehr aus der Produktmischung verschwunden;
- keine generischen `Produktvorschau`-Karten;
- kein unerwünschter `Hier könnte Ihre Anzeige stehen`-Block;
- Artikel-/Produktausgabe wieder vorhanden;
- Journal/Glossar/Pferderassen unverändert.

Kein LIVE-PASS vor diesem Readback. Keine Featurearbeit. Kein altes 6.72.118 installieren.
