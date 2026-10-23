# HD-003 – HOBBY DEPOT DESIGN / TEMPLATE KIT – CURRENT

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-23
STATUS: **MAGAZIN-ZIELSEITEN LIVE BEANSTANDET / 1.50.722 HARDROUTE LOKAL HARD PASS / CYBERDUCK-INSTALLATION OFFEN**

Plugin-ID:
`HD-003-DESIGN-TEMPLATE-KIT`

Fach-Current:
`../../../DESIGN/CURRENT_STATE.md`

## Live-Hinweis

Der Nutzer meldet weiterhin unveränderte Magazin-Zielseiten: kein Hero, kein Zielseiten-Template, keine grüne Intro-/Aufklappdarstellung.

1.50.721 ist damit nicht freigegeben.
1.50.722 ersetzt 1.50.721.

## Lokaler Kandidat 1.50.722

Artefakt:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.722_UPDATE_MAGAZIN_ZIELSEITEN_HARDROUTE.zip`

SHA-256:
`15e0bfa3fc861cf1dee11c8a8059d10dad4c743d4f52efeff28f091a233b184e`

Größe:
2,104,172 Bytes.

Hauptordner:
`affiliate-portal-template-kit/`

### Reproduzierter Fehler

Bisherige Zielseitenbindung hing von `is_singular('page')` / Queried Object ab.

Failure-Mode-Test mit echter URL `/magazin/<slug>/` und absichtlich fehlender WordPress-Seitenklassifikation:
- 1.50.721: **0/12 Templateübernahme**.
- 1.50.722: **12/12 Templateübernahme**.

### Fix

Die exakt 12 bekannten Magazin-Zielslugs werden zusätzlich URL-basiert erkannt:
- `/magazin/<slug>/`
- Fallback `/journal/<slug>/`

Die Bindung greift vor der bisherigen WordPress-Seitenklassifikation in:
- Template-Routing;
- Owned-Content-Renderer;
- Content-Fallback.

Negativtest fremder Pfad mit gleichem Slug: PASS.

### Zielseitenrender

11 normale Zielseiten vollständig gerendert:
- Hero PASS;
- Hero-Bild PASS;
- Brush/Schreibschrift PASS;
- grüne Lead-Box PASS;
- nativer Aufklapper PASS;
- Styles PASS.

11/11 PASS.

Hobbyfinder ist separat Teil der 12/12-Routenprüfung und behält den bestehenden Funnel unter der Magazin-Hülle.

### Paket

16 Dateien:
- 2 PHP;
- 1 Content-Template;
- 12 Magazinbilder;
- 1 Brush.

Fresh-Unpack/PHP-Lint/Assets: PASS.

Evidence:
`EVIDENCE_1.50.722.md`

## EXAKT EINE NEXT ACTION

**1.50.722 per Cyberduck in den bestehenden Ordner `wp-content/plugins/affiliate-portal-template-kit/` einspielen und danach eine Magazin-Zielseite live prüfen.**
