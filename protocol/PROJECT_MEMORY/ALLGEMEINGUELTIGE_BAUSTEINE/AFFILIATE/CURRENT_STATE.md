# ALLGEMEINER AFFILIATE-BESTAND – CURRENT STATE

STAND: 2026-09-11
STATUS: INVENTARISIERT / MODULKLASSE UNGEKLÄRT

Aktuelle Bestandsakte:
`MASTERDATEIEN_INVENTAR.md`

Archiv:
`/Campus-Archiv/ALLGEMEINGUELTIGE_BAUSTEINE/AFFILIATE/2026-09-05/`

Regel:
Dieser Ort ist ein Bestands-/Inventarraum, keine Aussage „allgemeingültiges Affiliate-Modul freigegeben“.

Projektbezogener aktueller Affiliate-Stand:
`../../PROJEKTE/PFERDE_ATELIER/AFFILIATE/`

## ERKANNTE ALLGEMEINE ARCHITEKTURREGEL – NOCH NICHT ALS MODUL FREIGEGEBEN

Aus dem ADCELL-Befund vom 11.09.2026 gilt für zukünftige Provider-Integrationen als Sicherheitsinvariante:

**Eine provider-spezifische Fachaktion darf niemals still in den Adapter eines anderen Providers fallen.**

Konsequenz:
- Provider-Routing explizit;
- unbekannter/nicht implementierter Provider fail-closed;
- Zugangsdaten, Partnerdaten und API-Aktionen bleiben provider-isoliert;
- gemeinsame Creative-/Output-/Veto-Logik darf erst hinter der korrekten Providerquelle wieder gemeinsam genutzt werden.

Diese Regel ist als Architekturfolge erkannt. Sie erklärt keine allgemeingültige Affiliate-Modulfreigabe und ändert keine bestehende Live-Freigabe.
