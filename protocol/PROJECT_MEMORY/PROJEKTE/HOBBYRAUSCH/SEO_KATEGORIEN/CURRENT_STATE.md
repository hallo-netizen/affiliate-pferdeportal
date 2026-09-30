# HOBBYRAUSCH – SEO_KATEGORIEN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-09-30
STATUS: TESTLABOR UNERWARTET DEPLOYED / V1.9.1 LOKAL HARD PASS / ROLLBACK + READ_ONLY RETEST NÄCHSTES

## Aktueller belastbarer Stand

Research/Tiefenprüfung des bisherigen Testlabors:
- 15/15 Content-Knoten;
- Spezialisierungsprüfung abgeschlossen;
- READ_ONLY_PREVIEW lokal PASS.

Live-Befund des alten Laufs:
- WordPress zeigt `Deployment abgeschlossen`;
- Schreiben + Readback wurde unerwartet ausgeführt.

Aktueller Fixstand ist jetzt **V1.9.1** derselben Pluginlinie.

V1.9.1 enthält:
- vollständigen V1.9.0 Stage-Hardlock;
- zusätzlich allgemeingültigen Editorial Intent Ownership Handoff;
- keine Hobby-Depot-Fachbegriffe hardcodiert;
- kein neues Plugin.

Lokale Prüfung:
- 248/248 PASS;
- Fresh-Unpack 248/248 PASS;
- PHP-Lint Source 18/18;
- PHP-Lint Installer 17/17;
- Runtime-Parität 22/22 byteidentisch.

Realer Kompatibilitätscheck:
Die bisherige READ_ONLY_PREVIEW-Datei enthält 27 `ARTICLE_ONLY`-Entscheidungen ohne eindeutigen Artikel-Owner. V1.9.1 blockiert deshalb nur deren späteren Redaktions-Handoff; die Kategorienprüfung selbst bleibt kompatibel.

## NEXT ACTION

V1.9.1 installieren → aktuellen Test-Deployment-Run vollständig zurückrollen → denselben READ_ONLY_PREVIEW erneut übernehmen.

Erwartung:
- `structure_ready`;
- kein automatischer Write;
- Stage-Hardlock real PASS;
- Editorial-Handoff sichtbar und fail-closed für noch ungebundene ARTICLE_ONLY-Owner.
