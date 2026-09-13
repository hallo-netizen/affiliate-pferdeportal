# BÜRO GLOSSAR – CURRENT_STATE

STAND: 2026-09-13
STATUS: 0.2.7 TECHNISCHER KANDIDAT HARDTEST PASS / PFERDE-LIVE-READBACK OFFEN

## Belastbarer aktueller Stand

- Büro `GLOSSAR` steuert das öffentliche Pferde-Atelier-Glossar.
- Fachliche Glossardaten bleiben ausschließlich in `../WISSENSDATENBANK/AKTENSCHRAENKE/GLOSSAR/`.
- Vorhandene WordPress-Seite `Glossar` bleibt Hauptseite.
- Glossarbegriffe sind keine normalen Beiträge/Seiten.
- Das bestehende Pferde-Designplugin bleibt unangetastet.
- Technischer Kern: `MOD-008 – Universal Glossar Engine`.

## Aktueller gebundener Kandidat

Plugin:
`Universal Glossary Engine 0.2.7`

Rewrite-Schema:
`5`

Branch:
`hobbyroom/glossar-027-release-hardtest-20260913`

Getesteter Commit:
`7191f15358cc73a78231652e9479f3a9fb5a9c37`

Autoritativer Run:
`34749231699`

Fresh-Install Job:
`103702569466` → PASS

Echter WordPress-Updateweg 0.2.5 → 0.2.7:
`103702569602` → PASS

Gated Package Job:
`103702749853` → PASS

Innerer Plugin-ZIP SHA-256:
`e9c32fc64db3c64c3b85e0d2692ff200e8f6d60e5827d7ab514657adff2ae831`

Actions-Artefakt-ID:
`10315142446`

Technisches Protokoll:
`../../../ALLGEMEINGUELTIGE_BAUSTEINE/GLOSSAR/TESTPROTOKOLL_0.2.7_20260913.md`

## Versionsklarheit

0.2.6 bleibt Entwicklungs-/Testhistorie und ist **kein aktueller Übergabekandidat**.

Grund:
Im Entwicklungsverlauf wurde 0.2.6 mehrfach als Kandidatenkennung benutzt. Für eindeutige Paketbindung wurde deshalb der erste übergabefähige Stand neu als 0.2.7 gebaut und vollständig neu geprüft.

Dauerregel:
Unterschiedliche Paketbytes = unterschiedliche Pluginversion.

## Hart geprüft

Positiv und negativ belegt:
- Fresh-Install WordPress + MySQL + Astra;
- echter WordPress-In-place-Updateweg von 0.2.5;
- absichtlich zerstörte Einzelbegriff-Rewrite-Regel → 404;
- Schema 4 → 5 nach Update und OPcache-Revalidierung;
- echte Einzelbegriffsseiten mit Artikelmarkup/Inhalt;
- unbekannter Begriff 404;
- Draft 404;
- Legacy 301;
- AJAX gültig/ungültig;
- Kategorie-/Begriffskollision;
- normale WordPress-Beiträge unverändert;
- Daten-/Konfigurationspersistenz;
- Deaktivieren/Reaktivieren;
- Hero-Abstand;
- responsive Hero-Darstellung;
- Breadcrumb-Achse;
- komplette alte Regression-/Frontendmatrix erneut PASS;
- exaktes erzeugtes ZIP lokal nochmals Hash-/Struktur-/Version-/Schema-negativ geprüft.

## Vier reale Pferde-Frontendpunkte

Autoritative Fehlerquelle:
`FEHLERQUELLEN.md`

1. Hero-Abstand oben.
2. Hero-Bild responsive.
3. Einzelbegriff-Links dürfen keine weiße Seite liefern; Titel/Inhalt müssen sichtbar sein.
4. Kategorie-Breadcrumb Position/Darstellung.

Technisch im 0.2.7-Kandidaten abgesichert, **reale Pferde-Sicht-/Funktionsprüfung noch offen**.

## Noch NICHT bewiesen

- Installation dieses exakt hashgebundenen 0.2.7-ZIPs im Pferde Atelier;
- realer Readback der vier Punkte;
- exakte Ursache der bisher beobachteten weißen Live-Seite;
- aktueller Astra+Yoast-Kombinationstest, soweit für endgültigen Release erforderlich;
- realer Wissensdatenbankimport;
- größerer Bestands-/Performance-Test;
- separates zweites reales Portal.

Daher: technischer Kandidat PASS, **kein Pferde-LIVE-PASS**.

## Nächster Schritt

Ausschließlich `HOBBYRAUM.md` folgen: exakt hashgebundenes 0.2.7-ZIP über den geprüften WordPress-Updateweg installieren und danach die vier realen Punkte plus negative Regressionen zurücklesen.
