from pathlib import Path
import re

wp=Path('protocol/PROJECT_MEMORY/WORDPRESS_REGISTER.md')
s=wp.read_text()
block='''### WP-009 – Universal Glossar Engine

MOD-ID:
MOD-008

Plugin:
`Universal Glossary Engine`

Aktuellster technisch gebundener Kandidat:
**0.2.9**

Rewrite-Schema:
**7**

Innerer Plugin-ZIP SHA-256:
`864befa0d159577e418906e4de3052ad0127b7dbcdad80775ba7e8f734ed1173`

Autoritativer finaler Hardtest:
- Run `34757795593`
- Build `103725094481` PASS
- Fresh/Regression/Null-Rewrite `103725094537` PASS
- Update 0.2.8 → 0.2.9 + erneuter Null-Rewrite `103725094620` PASS
- echter Design-1.50.469-Runtime + Browser + Null-Rewrite `103725094378` PASS
- gated Package `103725295224` PASS
- Actions-Artefakt-ID `10317444708`

Status:
**TECHNISCHER KANDIDAT HARDTEST PASS / KEIN PFERDE-LIVE-PASS.**

Wichtige Korrektur:
0.2.8 wurde durch realen Pferde-Readback als LIVE FAIL widerlegt: Hero nicht real responsive, Kategorien nicht mit vollständigem Glossar-Startseitenrahmen, Einzelbegriff-Links laufen ins Leere. 0.2.6/0.2.7/0.2.8 nicht verwenden.

0.2.9 prüft echtes responsives Bild, Kategorie-Vollrahmen, tatsächlich angeklickten Begriff-Link sowie Kategorie-/Begriff-Routing selbst bei vollständig gelöschten gespeicherten Glossar-Rewrite-Regeln und bereits aktuellem Schema 7. Draft-Preview bleibt Regression-PASS.

Hauptquelle:
`ALLGEMEINGUELTIGE_BAUSTEINE/GLOSSAR/`

Technisches Protokoll:
`ALLGEMEINGUELTIGE_BAUSTEINE/GLOSSAR/TESTPROTOKOLL_0.2.9_20260913.md`

Erste Projektanwendung:
`PROJEKTE/PFERDE_ATELIER/GLOSSAR/`

Modulklasse:
`UNGEKLÄRT / ZIEL ALLGEMEINGÜLTIG`.

Offen:
Pferde-Atelier-Live-Readback des exakt hashgebundenen 0.2.9-Kandidaten; Wissensdatenbankimport; Performance-Test; zweites reales Portal; Yoast-Kombination soweit release-relevant.
'''
m=re.search(r'### WP-009 – Universal Glossar Engine.*\Z',s,re.S)
assert m, 'WP-009 not found'
wp.write_text(s[:m.start()]+block)

mod=Path('protocol/PROJECT_MEMORY/ALLGEMEINGUELTIGE_BAUSTEINE/MODULREGISTER.md')
s=mod.read_text()
block='''## MOD-008 – UNIVERSAL GLOSSAR ENGINE

MODULKLASSE: UNGEKLÄRT / ZIEL ALLGEMEINGÜLTIG

STATUS:
0.2.9 technischer Kandidat HARDTEST PASS; Pferde-Live-Readback 0.2.9 offen. 0.2.8 ist realer LIVE FAIL und nicht zu verwenden.

HAUPTORT:
`ALLGEMEINGUELTIGE_BAUSTEINE/GLOSSAR/`

AKTUELL BELEGTER STAND:
- Plugin 0.2.9
- Rewrite-Schema 7
- finaler Run `34757795593`
- getesteter Produkt-Head `f2fa6f0c248acfa6978b5faec5daf42a40d0ba3b`
- ZIP SHA-256 `864befa0d159577e418906e4de3052ad0127b7dbcdad80775ba7e8f734ed1173`
- Actions-Artefakt-ID `10317444708`

ZWECK:
Projektunabhängiger Glossar-Core mit Begriffstyp, hierarchischen Oberbereichen, Suche, A–Z, eigenen Begriff-URLs, SEO-Feldern und JSON-Transfer.

ABHÄNGIGKEITEN:
WordPress; projektspezifisches Design bleibt außerhalb des neutralen Cores.

NUTZENDE PROJEKTE:
- PFERDE_ATELIER → `PROJEKTE/PFERDE_ATELIER/GLOSSAR/`

AUTORITATIVE QUELLE / BELEG:
- `ALLGEMEINGUELTIGE_BAUSTEINE/GLOSSAR/CURRENT_STATE.md`
- `ALLGEMEINGUELTIGE_BAUSTEINE/GLOSSAR/TESTPROTOKOLL_0.2.9_20260913.md`
- finaler Hardtest Run `34757795593`

PRÜFGRAD:
Fresh/Regression PASS; echtes responsives Bild im Browser PASS; Kategorie-Vollrahmen PASS; real gerenderter Begriff-Link angeklickt PASS; Routing bei vollständig gelöschten gespeicherten Glossar-Rewrite-Regeln PASS; Update 0.2.8 → 0.2.9 PASS; echter Pferde-Designcode 1.50.469 Runtime PASS; gated package und lokaler exakter Artefaktcheck PASS.

OFFENE PUNKTE:
- Pferde-LIVE-Readback 0.2.9;
- zweites reales Portal;
- Wissensdatenbankimport;
- Performance-Test;
- Yoast-Kombination soweit release-relevant.
'''
pat=r'## MOD-008 – UNIVERSAL GLOSSAR ENGINE.*?(?=\n## MOD-|\Z)'
m=re.search(pat,s,re.S)
assert m, 'MOD-008 not found'
s=s[:m.start()]+block+s[m.end():]
s=s.replace('STAND: 2026-09-12','STAND: 2026-09-13',1)
mod.write_text(s)
