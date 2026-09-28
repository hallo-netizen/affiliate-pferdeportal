# HOBBYRAUSCH – PLUGINS – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-09-28
STATUS: HD-001 V1.8.6 ROOTFIX UPDATE BEREIT

## Rolle

Einzige aktuelle Zustandsautorität des Scopes `HOBBYRAUSCH_PLUGINS`.

## Aktueller belastbarer Stand

HD-001 V1.8.5 wurde live bis zum ersten echten DataForSEO-Konzeptstart getestet.

Live-Blocker:
`SEO-Erstentwurf erzeugen` verlangte irrtümlich eine separate Human-Sight-Review-Bestätigung.

Rootfix V1.8.6:
- Konzeptstart verlangt nur Adminrecht + eigenen Nonce + ausdrückliche DataForSEO-Paid-Bestätigung;
- spätere Human-Review-Gates unverändert;
- keine Funktions- oder Qualitätsreduktion.

Tests:
- 227/227 PASS;
- Fresh-Unpack-Installer 227/227 PASS;
- Installer PHP 16/16 PASS;
- Runtime-Parität 21/21 PASS.

## NEXT ACTION

V1.8.6 über V1.8.5 installieren und denselben Testlabor-Konzeptstart erneut ausführen.
