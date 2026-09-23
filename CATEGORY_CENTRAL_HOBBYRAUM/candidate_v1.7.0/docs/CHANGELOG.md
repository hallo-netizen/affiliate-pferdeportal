# Changelog

## 1.7.0 – Zentrales Büro „Kategorien“ (Kandidat)
- Bestehenden V1.6.1-Research-/Hardlock unverändert erhalten.
- Neue zentrale Kategorien-Sollquelle mit Generation, deterministischem SHA-256 und vollständigem Delta-Protokoll.
- Vorschau vor jeder Übernahme; Löschungen nur mit ausdrücklicher Bestätigung.
- Stale-Preview-Schutz gegen Übernahme auf veraltetem Stand.
- Exakter letzter Stand als inaktiver Fallback; Rollback erzeugt eine neue protokollierte Generation.
- Neue Backend-Seite „Kategorien“ für Prüfen, Übernehmen, Export und Rollback.
- Keine WordPress-/HivePress-Content-Writes; `APKW_CONTENT_WRITE_CAPABILITY=false` bleibt unverändert.
- Fallbackbasis: V1.6.1 ZIP SHA256 `c0572951a5672e04fbad87f27ff6bb4990072db55500c6ad865c4d8193719c55`.
- Hardtest Run `35830042424`: SUCCESS. Lint, V1.6.1-Regression, Kandidaten-Regression, Add/Delete/Stale/Rollback-Simulation, No-Write-Scan und Fallback-Hash PASS.

## 1.6.1
- HARDLOCK Rootfix: manuelle Review-Status/Hash-Injektion durch serverseitig HMAC-signierte Review-Quittungen blockiert.
- Signierung zusätzlich an exakten sichtbaren Review-Scope-SHA-256 gebunden.
- Zielmarkt/Sprache vollständig in Projekt-, Research-, Review- und Paketbindung aufgenommen.
- Rehash-Tampering von Global-/Research-Paketen mit falschem Markt/Sprache blockiert.
- Master-Contract-ID in Category-, Global- und Research-Paketen fest gebunden.
- 112 Positiv-/Negativtests im Source-Stand.

## 1.6.0
- Drei sichtbare hashgebundene Freigabestufen; Global-Ähnlichkeit darf keine fachliche Entscheidung ersetzen; DEFERRED blockiert.

## 1.5.0
- Contentkategorie-Rootfix: tragfähige Beitragsrichtungen können echte Content-Kategorien sein.
