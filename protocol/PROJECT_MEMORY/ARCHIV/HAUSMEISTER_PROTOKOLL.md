# ARCHIV – HAUSMEISTER-PROTOKOLL

STAND: 2026-09-05

## Zweck

Jede echte Aufräum-/Archivverschiebung wird hier nachvollziehbar dokumentiert.

Pflichtfelder je Vorgang:
- HM-ID
- Datum
- Quelle
- ursprünglicher Pfad/Referenz
- Hash/Identität
- Grund für HISTORISCH
- neuer Archivort/Referenz
- aktualisierte aktive Verweise
- Prüfung
- Ergebnis

## Regel

Keine stille Archivverschiebung.
Keine Löschung durch den Hausmeister.

Aktuell:
Noch keine produktiven Dateien durch den neuen Hausmeisterprozess verschoben.


## HM-001 – Master 0057 Teil A als reines Historienarchiv einsortiert

DATUM:
2026-09-05

QUELLE:
Nutzerupload `ARBEITSMASTER_0057_NEU_TEIL_A_UNVERAENDERLICHES_HISTORIENARCHIV(1).zip`

IDENTITÄT:
SHA-256 `25c8a9fa71ff6f1f57137c2afb1e2c03ed8a6e3477f2902fdf003590ea785423`

GRUND FÜR HISTORISCH:
Eigener README-Vertrag bezeichnet Teil A ausdrücklich als unveränderliches `98_HISTORY_READ_ONLY`-Historienarchiv.

NEUER ARCHIVORT:
`/Campus-Archiv/PROJEKTE/PFERDE_ATELIER/TEXT_STARTMASTER0107/HISTORISCH/MASTER_0057_TEIL_A/`

AKTIVE VERWEISE:
keine Fach-/CURRENT-Verweise geändert.

PRÜFUNG:
Manifest 4.955/4.955 + innerer tar.zst-SHA-256 PASS.

ERGEBNIS:
GELB / korrekt historisch / lokale Originalkopie nicht entbehrlich.

## HM-002 – LanguageTool 6.8 als TEXT/SEO-Offline-Abhängigkeit archiviert

DATUM:
2026-09-05

QUELLE:
Nutzerupload `ARBEITSMASTER_0043_NEU_TEIL_2_LANGUAGETOOL_ABHAENGIGKEIT(2).zip`

IDENTITÄT:
SHA-256 äußere ZIP `187f7c2efe7762049e9f00553dafe686e269bbf62220abe2f2715fe55df8605a`

INNERES ARTEFAKT:
`LanguageTool-6.8.zip`
SHA-256 `6a7f6b67b779ae9505f7579f0c41453ea8d1bd72ae750bdc2c55ba974281467d`

NEUER ARCHIVORT:
`/Campus-Archiv/PROJEKTE/PFERDE_ATELIER/TEXT_STARTMASTER0107/ABHAENGIGKEITEN/LANGUAGETOOL/6.8/`

EINORDNUNG:
TEXT/SEO-spezifische Offline-Abhängigkeit / nicht Plugin / aktuelle Nutzung UNGEKLÄRT.

AKTIVE VERWEISE:
kein CURRENT_STATE, Hobbyraum, Fehler- oder Zielvertrag geändert.

PRÜFUNG:
Manifest-Hash und Größe gegen inneres LanguageTool-ZIP PASS; 2.051 ZIP-Einträge inventarisiert.

ERGEBNIS:
GELB / archiviert / keine Allgemeingültigkeits- oder Aktivfreigabe.


## HM-003 – Repository-Besen-Audit 2026-09-22

DATUM:
2026-09-22

AUFTRAG:
Einmaliger Hausmeisterdurchlauf über den aktiven GitHub-`main` mit harter Sperre:
aktuelle Einträge und aktuelle Plugins niemals löschen oder verschieben.

PRÜFUNG:
- Hausmeister-Regel frisch gelesen;
- Autoritätsplan frisch gelesen;
- Pferde-Atelier-PLUGINS Current + Register frisch gelesen;
- kompletter `main`-Tree frisch vermessen;
- große ZIP-Blöcke nach Größe identifiziert;
- neun historische/diagnostische Root-ZIPs nach exaktem Namen auf aktive Referenzen im Default-Branch geprüft;
- Ursprungscommits dieser neun Dateien frisch gelesen.

ERGEBNIS:
- **0 Dateien gelöscht**;
- **0 aktuelle Pluginartefakte angefasst**;
- **0 aktive Current-/Ziel-/Fehler-/Routingautoritäten verschoben**;
- neun große Dateien als `ARCHIVKANDIDAT / NO DELETE` klassifiziert;
- Kandidatenvolumen ca. 70.25 MB;
- Detailbeleg: `ARCHIV/REPOSITORY_BESEN_AUDIT_20260922.md`.

WARUM KEINE LÖSCHUNG:
Hausmeister darf laut verbindlichem Prozess Dateien nicht löschen. Außerdem ist fehlender aktueller Dateinamensverweis allein kein ausreichender Löschbeweis.

ERGEBNISSTATUS:
PASS / sicherer Auditlauf / keine aktive Wahrheit verändert.


## HM-004 – Neun Repository-Kandidaten ins Sammelarchiv verschoben

DATUM:
2026-09-22

AUFTRAG:
Die in HM-003 identifizierten neun Kandidaten vorerst gesammelt archivieren; aktuelle Einträge und Plugins zwingend nicht anfassen.

AUSFÜHRUNG:
- byteidentische Verschiebung nach `archive/repository-loeschkandidaten/2026-09-22/`;
- keine endgültige Löschung;
- PR #360;
- Merge `78d02baf8f830e82b1f9e59ef7df458a5d367fee`.

PRÜFUNG:
- `hardlock` PASS;
- `hardlock-base` PASS;
- Post-Merge: alte Root-Pfade 0/9 vorhanden;
- Archivpfade 9/9 vorhanden;
- Git-Blob-SHAs 9/9 unverändert;
- aktuelle Plugin-/Current-Autoritäten nicht angefasst.

ERGEBNIS:
PASS / sicher archiviert / spätere Sammelprüfung vor endgültiger Entfernung weiterhin erforderlich.


## HM-005 – Pferdeatelier Textsysteme K1 bis K9 aus aktiver Campusfläche entfernt

DATUM:
2026-10-16

QUELLE:
aktiver Campus-Branch `hobbyroom/project-memory-campus-v1-20260905`.

GRUND FÜR HISTORISCH:
Nutzerentscheidung: K0 ist Produktionsbasis; K1 bis K9 bleiben nur zur späteren Recherche erhalten und dürfen keine aktive Current-/Start-/Fallback-Autorität mehr besitzen.

ARCHIVREFERENZEN:
- `archive/pferdeatelier-textoffice-k1-k9-20261016`
- `archive/pferdeatelier-textsysteme-k1-k8-20261016`
- `archive/pferdeatelier-k9-gold-20261016`
- lokales vollständiges GitHub-Backup vom 16.10.2026

AKTIVE VERWEISE:
TEXT-Routing, Autoritätsplan, Fehlerwegweiser, Handlungsverzeichnis und Zielregister auf K0 umgestellt. TEXTSYSTEM_4A als aktive Bürotür entfernt.

PRÜFUNG:
28 historische Pferde-TEXT-/4A-Dateien aus der aktiven Campusfläche entfernt; Archivkopien vorab gesichert; aktive Routingdateien auf fehlende Legacy-Currentverweise geprüft.

ERGEBNIS:
PASS / historischer Bestand erhalten / aktive Arbeitsfläche verkleinert / keine Plugin- oder WordPress-Fachänderung.
