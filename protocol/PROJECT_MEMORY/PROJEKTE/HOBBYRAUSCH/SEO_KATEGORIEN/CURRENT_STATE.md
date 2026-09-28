# HOBBYRAUSCH – SEO_KATEGORIEN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-09-28
STATUS: TESTLABOR UNERWARTET DEPLOYED / V1.9.0 HARDLOCK LOKAL PASS / ROLLBACK NÄCHSTES

## Aktueller belastbarer Stand

Research/Tiefenprüfung waren vollständig:
- 15/15 Content-Knoten;
- Spezialisierungsprüfung abgeschlossen;
- READ_ONLY_PREVIEW lokal PASS.

Live-Befund nach READ_ONLY_PREVIEW-Übernahme:
- WordPress zeigt `Deployment abgeschlossen`;
- Schreiben + Readback erfolgreich.

Das ist für den angeforderten Einzelschritt nicht akzeptabel und wird nicht als Plugin-PASS gewertet.

V1.9.0 Rootfix:
- exakte serverseitige Stage-Bindung aller Guided-Aktionen;
- stale spätere Aktionen blockieren;
- Downstream-Artefakte werden bei Upstream-Ersatz invalidiert;
- aktiver Deployment-Run muss vor neuem Upstream-Import zurückgerollt werden.

Lokale Prüfung:
- 241/241 PASS;
- Fresh-Unpack 241/241 PASS;
- exakter Regressionstest READ_ONLY_PREVIEW + stale Deploy-Plan → kein Deployment, stale Pakete gelöscht, Stage structure_ready;
- PHP/Runtime-Parität PASS.

## NEXT ACTION

V1.9.0 installieren, aktuellen Test-Deployment-Run vollständig zurückrollen und danach denselben READ_ONLY_PREVIEW erneut übernehmen. Erwartung: finale Read-only-Prüfung bei Stage `structure_ready`, kein automatischer Write.
