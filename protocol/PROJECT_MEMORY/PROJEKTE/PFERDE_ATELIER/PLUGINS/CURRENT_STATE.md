# PFERDE-ATELIER – PLUGINS – CURRENT_STATE

STAND: 2026-09-13
STATUS: BLOCKED / BÜRO ANGELEGT, VOLLSTÄNDIGE ISOLIERTE ARTEFAKTABLAGE NOCH NICHT FÜR ALLE PLUGINS BEWIESEN

## Belastbarer Stand

Das zentrale PLUGINS-Büro ist angelegt.

Bekannte Pluginbestände wurden frisch gegen Campus-/Fachquellen inventarisiert. Für mehrere Plugins ist der aktuelle belegte Versions-/Hashstand vorhanden; bei einzelnen liegt der aktuelle belastbare Pluginstand jedoch nur als externe/hashgebundene ZIP bzw. als Fach-/Releasequelle vor und nicht bereits als isolierte Datei im Campus-Branch.

Darum gilt ausdrücklich:
**Noch kein `ALLE_PFERDE_PLUGINS_ISOLIERT_PASS`.**

## Aktuell belastbar identifizierte Pluginfamilien

Siehe ausschließlich `REGISTER.md` für den Inventar-/Syncstatus.

Fach-/Release-/LIVE-Status niemals aus diesem CURRENT_STATE ableiten, sondern aus der dort je Plugin verlinkten autoritativen Quelle.

## Zielzustand

Für jedes tatsächlich im Pferde-Atelier geführte Plugin:

`ISOLIERTE_PLUGINS/<PLUGIN-ID>/CURRENT.zip`
+
`ISOLIERTE_PLUGINS/<PLUGIN-ID>/MANIFEST.md`

Nur nach belegter Quelle, Versionsprüfung, SHA-256 und erforderlichen Fach-/Regressionstests.

## Erster Blocker

Nicht alle aktuellen Plugin-ZIPs sind aus dem Campus-Branch oder einer aktuell direkt abrufbaren technischen GitHub-Quelle als identisches Installationsartefakt verfügbar.

Beispiele mit belegtem aktuellen Stand, aber noch fehlender isolierter Campus-Datei:
- Pferde Atelier Design 1.50.472: finaler Installername + SHA-256 belegt, Installer selbst im aktuellen Branch nicht als Datei vorhanden;
- Bildzentrale 2.6.9 / Universal Research & Fill 1.9.9: exakte Installer + Hashes belegt, aktuelle Binärdateien nicht im Campus-Branch vorhanden;
- Universal Product Comparison 0.8.0-prototype: aktuelle hashgebundene ZIP ist Fachautorität, aktueller Technikbranch enthält ausdrücklich nicht den vollständigen 0.8.0-Quellstand.

Diese Lücken dürfen nicht durch Rekonstruktion aus alten Mastern oder Chat-Historie kaschiert werden.

## NEXT ACTION

1. Pro Registereintrag die aktuelle autoritative Quelle frisch binden.
2. Wo der aktuelle Source/Release vollständig GitHub-erreichbar ist: isoliertes `CURRENT.zip` reproduzierbar erzeugen und prüfen.
3. Wo nur ein externes hashgebundenes Installationsartefakt autoritativ ist: genau dieses Artefakt einmal in die zentrale Plugin-Ablage übernehmen und Hash vergleichen.
4. Erst wenn alle aktiven Einträge `ARTEFAKT_SYNC=PASS` haben: Gesamtstatus auf PASS setzen.

## Nicht anfassen

- keine Pluginversion nur wegen eines älteren Masters hoch-/herabstufen;
- keine Fach-/LIVE-Wahrheit hierher verlagern;
- keinen allgemeinen Modul-Kern als Pferde-spezifisch umklassifizieren;
- keine Secrets.
