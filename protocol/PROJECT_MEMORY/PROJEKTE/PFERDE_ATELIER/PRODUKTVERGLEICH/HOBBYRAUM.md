# PRODUKTVERGLEICH – HOBBYRAUM

STAND: 2026-09-07
STATUS: AKTIV / V1-PLUGINENTWICKLUNG

## 1-KLICK-ÜBERSICHT

**AKTUELLER AUFTRAG**  
V1 als unabhängigen, allgemeingültigen Produktwissen-/Produktvergleichsweg bis WordPress-DRAFT entwickeln.

**HARTE GRENZEN**
- STARTMASTER/TEXT nicht umbauen;
- keine Produktfakten erfinden;
- SEO/Affiliate schreiben keine Produktwahrheit;
- kein main, kein Live-Publish.

## BELEGTER STAND

Technik-Branch:
`hobbyroom/productwissen-v1-prototype`

Draft-PR:
#142 gegen Campus-Branch.

PASS:
- `UPK_WORDPRESS_DB_GESAMT_PASS`;
- `UPC_WORDPRESS_DB_GESAMT_PASS`;
- `UPC_REAL_DOSSIER_PV_REG_001_PASS`;
- letzter belegter WordPress+MySQL Run: `34109264265` SUCCESS.

Damit sind Produktwissen, Vergleichspaarung, Merkmalsmatrix und deterministisches Writer-Dossier real gegen WordPress+MySQL geprüft.

## NEXT ACTION

**WordPress-DRAFT-Ausgabe als nächste dünne Schicht auf den vollständig gebundenen Single-Door-Output setzen.**

Harte Regeln:
1. WordPress-Draft-Writer akzeptiert niemals freien Titel oder freien HTML-Body;
2. Eingang ausschließlich: Vergleichs-ID + project_key + gebundene ruleset_id;
3. Draft-Writer ruft intern ausschließlich `upc_production()` auf;
4. nur `DRAFT_READY_FOR_REVIEW` + gültiger Receipt darf einen WordPress-Draft erzeugen;
5. Post-Status ausschließlich `draft`;
6. kein Publish-/Future-/Private-Fallback;
7. gespeicherter Post-Body muss byte-identisch zum validierten Renderer-HTML sein;
8. gespeicherter Output-Hash muss erneut geprüft werden;
9. fehlender/abweichender Receipt oder Hash = BLOCKED.

Belegter Writer-Stand:
- Zero-Freedom Static Guard PASS;
- 100/100 byte-identisch;
- Golden Output PV-REG-001 PASS;
- Ruleset-Manipulation BLOCKED;
- Faktenänderung gegen altes Ruleset BLOCKED;
- Run `34111825722` SUCCESS.

Noch kein Affiliate-Renderer und kein Vergleichsarchiv/Frontend. Diese folgen erst nach WordPress-DRAFT-PASS.

## Globale Arbeitsort-Sperre

Tresor, Archiv, Backup und Git-Mirror sind niemals Werkbank oder Runner-Quelle.
