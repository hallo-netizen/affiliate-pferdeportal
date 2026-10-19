# HD-003 – HOBBY DEPOT DESIGN / TEMPLATE KIT – CURRENT

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-19
STATUS: **1.50.692 SCHUHMACHEREI-TEXTPILOT DOKUMENTIERT GEBAUT / STATISCHE QA PASS / HARD POSITIV-NEGATIV-E2E OFFEN / NICHT ALS CURRENT.zip FREIGEGEBEN**

## AKTUELLER TECHNISCHER STAND

Plugin-ID:
`HD-003-DESIGN-TEMPLATE-KIT`

Basis:
- Vollpaket 1.50.691 mit aktiver V150691-Kette;
- 1.50.690-Detailseitenrollout darin enthalten;
- neue ruhige Startseitenbilder aus 1.50.691 enthalten;
- Hauptkategorie-Heros unverändert.

Pilot:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.692_SCHUHMACHEREI_TEXT_PILOT.zip`

Dokumentierte SHA-256:
`c9a45879b268c60d2d825be0225bfe0d1e03f37f219dd6282498c53b75e2d86a`

Pilot-Scope:
- ausschließlich Schuhmacherei textlich/visuell als Musterfall;
- 51-Wort-Lead: Was ist das Hobby, was macht man, was ist typisch;
- 164 Wörter Gesamttext;
- `Mehr zur Schuhmacherei`;
- 9 konkrete Kacheluntertitel;
- heller Petrolblock für sichtbaren Lead;
- andere Detail-Hobbys noch nicht ausgerollt;
- Startseite und Hauptkategorie-Heros unverändert.

Dokumentierte QA:
- PHP 120/120 PASS;
- ZIP PASS;
- aktive V150692-Releasekette PASS.

## ERSTER OFFENER BLOCKER

Für 1.50.692 fehlt in der aktuellen Evidence die projektweit vorgeschriebene vollständige lokale **Positiv- UND Negativ-E2E-Simulation** des tatsächlich gerouteten Renderpfads. Deshalb ist das Paket noch kein freigegebener Upload-/Deploymentkandidat.

## ISOLIERTES ARTEFAKT

`PLUGINS/ISOLIERTE_PLUGINS/HD-003-DESIGN-TEMPLATE-KIT/CURRENT.zip` wird **nicht** erzeugt/ersetzt, solange der Hard-PASS fehlt.

## EXAKT EINE NEXT ACTION

**Den realen 1.50.692-Schuhmacherei-Pfad lokal positiv und negativ E2E simulieren; bei PASS erst danach das Vollpaket ausgeben und die isolierte Plugin-Ausgabe synchronisieren.**

Fach-Current:
`../../../DESIGN/CURRENT_STATE.md`
