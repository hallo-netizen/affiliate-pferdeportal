# HOBBYRAUSCH – SEO_KATEGORIEN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-17
STATUS: **LIVE-BASELINE UNVERÄNDERT / V4 STRUKTURELL PASS ABER UNIVERSAL-USER-NEEDS FAIL / V5 KORREKTUR NÖTIG / HD-001 1.14.9 VERWORFEN / 1.14.10 MANUAL-ONLY LOCAL PASS**

## Live-Baseline

Produktiv unverändert:
`HD-TARGET-3P-RULE27-CATEGORY-GAPFIX-HOBBYFINDER-20261009+0f4dbf59238a7d83`

- 2357 aktive physische Zielobjekte;
- 2357/2357 Readback;
- 8 Hauptwelten;
- 330/330 terminale CORE-Seiten;
- LIVE-PASS.

## V4 – strukturell gültig, fachlich noch NICHT freigegeben

Profil:
`/hobby rausch/KATEGORIE_ZENTRALE/HOBBY_DEPOT_TARGET_PROFILE_AUDIT_CANDIDATE_V4_20261017.json`

Struktur-Audit:
`/hobby rausch/KATEGORIE_ZENTRALE/HOBBY_DEPOT_FULL_STRUCTURE_AUDIT_V4_20261017.json`

Universal-User-Needs-Audit:
`/hobby rausch/KATEGORIE_ZENTRALE/HOBBY_DEPOT_UNIVERSAL_USER_NEEDS_AUDIT_V4_20261017.json`

V4-Struktur:
- 8/8 Hauptwelten unverändert;
- 381 terminale Hobbyseiten;
- 2236 unterste Inhaltskategorien;
- keine fehlenden Parents;
- keine doppelten Node-IDs/Slugs;
- vollständige direkte Hub-`nav_order`;
- HD-001 Validator 0 Errors / 0 Warnings;
- Registry-Renderer 0 Strukturmismatches.

## Verbindlicher Zielvertrag für die Hobby-Ebene

Jeder HOBBY_HUB wird aus zwei Perspektiven geprüft:
1. Anfänger/Neuling braucht Orientierung;
2. bestehender Nutzer/Fortgeschrittener braucht Vertiefung.

Harte Regeln:
- **Einstieg & Grundlagen = Pflicht als sichtbare Content-Kategorie**;
- **FAQ / Häufige Fragen = Pflicht als sichtbare Content-Kategorie**;
- **Ausrüstung & Kosten = Standardpflicht**, sobald mindestens 3 eigenständige Beiträge möglich sind;
- **Praxis & Vertiefung = Pflicht als Nutzerabdeckung**, eigener Leaf nur wenn nicht bereits durch Fachkategorien abgedeckt;
- jede Content-Kategorie mindestens 3 eigenständige sinnvolle Beitragsintentionen;
- keine künstlich leeren Symmetrie-Kategorien.

Ausrüstung-&-Kosten umfasst typischerweise:
- Was brauche ich?;
- Grundausstattung;
- Kauf-/Auswahlfragen;
- Einsteigerbudget;
- einmalige Kosten;
- laufende Kosten;
- günstig vs. hochwertig.

## V4 Universal-Needs Befund

V4 erfüllt diese Regel noch NICHT vollständig:
- FAQ: 381/381 PASS;
- expliziter Einstieg/Grundlagen-Pfad: 376/381 PASS;
- fehlender expliziter Einstieg bei:
  - Mikroabenteuer;
  - Longboard Dancing;
  - Tierspuren dokumentieren;
  - Wolkenbeobachtung;
  - Terrarienbau;
- explizite Kosten-Kategorie: 0/381;
- 145/381 besitzen zwar bereits Ausrüstungs-/Material-spezifische Fachkategorien, aber der universelle Anfängerblock `Ausrüstung & Kosten` wurde nicht systematisch durchgesetzt;
- 381/381 besitzen mindestens zwei fachspezifische Vertiefungsleafs.

**Damit ist V4 KEIN finaler Dry-Run-/Sync-Kandidat.**

## Bereits bestätigte fachliche Erweiterungen

Enthalten bleiben:
- Spotting & Verkehr;
- Citizen Science;
- Natur bestimmen;
- Plane Spotting aus Messen & Analysieren heraus;
- Suchen & Finden;
- Modellbau unter Fertigen;
- Miniaturen & Szenen;
- Naturfunde;
- Schneckenhaltung;
- Bonsai & Miniatur → Penjing, Saikei;
- Leder → Lederprägen, Schuhmacherei;
- Essbare Pflanzen → Kräuteranbau, Obst im Kübel;
- Imkerei & Bestäuber → Wildbienenhotels, Hummelkästen;
- Gehegegestaltung → Paludarium, Terrarienbau.

## V5-Regel

V5 muss pro Hobby:
1. Einstieg/Grundlagen sichtbar sicherstellen;
2. FAQ sichtbar sicherstellen;
3. Ausrüstung-&-Kosten-Kapazität konkret prüfen;
4. bei >=3 eigenständigen Intents einen sichtbaren eigenen Kosten-/Ausrüstungsleaf sicherstellen;
5. bei <3 Intents diese Bedürfnisse klar in Einstieg/Grundlagen integrieren;
6. Fach-/Praxis-/Profi-Pfade erhalten und nicht durch generische Kategorien verdrängen;
7. danach vollständigen TargetTree-/Renderer-/Delta-Dry-Run erneut bestehen.

## Timeout-Korrektur

HD-001 1.14.9 ist verworfen.

Sicherer Kandidat:
`/hobby rausch/KATEGORIE_ZENTRALE/HD001_V1.14.10_MANUAL_ONLY_TIMEOUT_FIX_LOCALPASS.zip`

SHA-256:
`f9500d051249b239ca3215754eff54d37244fb80ef612ce54cfd5f722db7f243`

## ERSTER OFFENER BLOCKER

**V5 Universal-Needs-Korrektur muss abgeschlossen werden, bevor irgendein neuer WordPress-Dry-Run oder Sync erfolgt.**

## EXAKT EINE NEXT ACTION

**V4 jetzt NICHT dry-runnen/synchronisieren. Zuerst V5 gegen die verbindlichen Anfänger-/Fortgeschrittenen-Regeln vollständig erzeugen und lokal prüfen.**
