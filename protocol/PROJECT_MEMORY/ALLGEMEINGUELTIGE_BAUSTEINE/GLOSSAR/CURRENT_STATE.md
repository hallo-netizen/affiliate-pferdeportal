# UNIVERSAL GLOSSAR ENGINE – CURRENT_STATE

STAND: 2026-09-13
STATUS: 0.2.9 TECHNISCHER KANDIDAT HARDTEST PASS / PFERDE-LIVE-READBACK OFFEN

## Belastbarer Stand

- Modul: `MOD-008 – Universal Glossar Engine`.
- Neutraler WordPress-Core; Pferde Atelier ist erste Projektanwendung.
- Inhaltstyp `uge_term`, hierarchische Gruppen `uge_group`, Hauptseite, Suche/A–Z, SEO-Felder, JSON-Transfer.
- Kein Bildzwang, kein Auto-Publish.

## Reale Korrekturfolge

0.2.7: LIVE FAIL / nicht verwenden.

0.2.8: **LIVE FAIL / nicht verwenden.** Nutzer-Readback:
- Hero real nicht responsive;
- Kategorien nicht wie der Glossar-Startseitenrahmen gestaltet;
- Einzelbegriff-Links laufen ins Leere.

Zusätzlich wurde erkannt, dass die 0.2.8-Kategorie-Acceptance fachlich falsch war: sie verlangte das Fehlen von Hero/Tools und prüfte damit das Gegenteil der Nutzeranforderung.

## Aktueller technischer Kandidat

Version: `0.2.9`
Rewrite-Schema: `7`
Branch: `hobbyroom/glossar-livefail-red-green-20260913`
Getesteter Head: `f2fa6f0c248acfa6978b5faec5daf42a40d0ba3b`
Finaler Run: `34757795593`

Jobs – alle PASS:
- Build `103725094481`
- Fresh + komplette Regression + Null-Rewrite `103725094537`
- echtes Update 0.2.8 → 0.2.9 + erneuter Null-Rewrite `103725094620`
- echter Pferde-Designcode 1.50.469 + Browser + Null-Rewrite `103725094378`
- gated Package `103725295224`

## Neue harte Beweise

### Echtes Responsive-Bild
Der Browser misst das reale Bild selbst auf 1200 / 900 / 720 / 500 px. Es skaliert mit `width:100%` / `height:auto` und behält das Natural-Verhältnis 1400×560. Keine feste Bildhöhe und kein erzwungener 5:2-Hero-Container dienen mehr als Schein-Responsivität.

### Kategorien
Kategorie besitzt eigenen Inhalt und gleichzeitig den vollständigen Glossar-Startseitenrahmen:
Hero + Suche/A–Z + Icon-Navigation + Kategorie-Kopf/Karten. Kicker: `WISSEN`.

### Routing unabhängig von gespeicherten Rewrite-Regeln
0.2.9 ergänzt einen direkten Request-Binder für Glossar-Begriff und Glossar-Gruppe.

Die Tests entfernen **alle gespeicherten Glossar-Rewrite-Regeln bei bereits aktuellem Schema 7**. Kategorie- und Begriff-URLs müssen trotzdem funktionieren. Damit ist ein bloßer Schema-Bump nicht mehr die einzige Absicherung.

Der Browser klickt einen tatsächlich gerenderten Begriff-Link und verlangt danach echte Einzelartikelstruktur + Inhalt.

### Regression
Der erste RC des Direktroutings fing eine native Draft-Preview ab und wurde ROT. RC2/final nimmt WordPress-Previewparameter vom Binder aus; alte Preview-Regression ist wieder PASS. Dieser Befund ist Teil der finalen Kette.

## Exakter Kandidat

ZIP:
`universal-glossary-engine-0.2.9.zip`

SHA-256:
`864befa0d159577e418906e4de3052ad0127b7dbcdad80775ba7e8f734ed1173`

Actions-Artefakt-ID:
`10317444708`

Outer artifact digest:
`sha256:98513772d72fc65dc4d01520086b4c7e56e165cceeea1e31147a9d6cf830c6ff`

Das heruntergeladene ZIP wurde lokal nochmals auf Integrität, Version 0.2.9, Schema 7, Direct Binder, Kategorie-Vollrahmen und RC-Freiheit geprüft.

## Echter Designnachweis

Ausgeführt wird der exakte Pferde-Design-Hauptcode 1.50.469, SHA-256:
`580fa6c7f5566f29df9254ce92f687a4831554e1d84bf03fbd936bb7577edfe5`.

Kein Design-Stub gilt als Realnachweis.

## Modulklasse / offene Punkte

Modulklasse formal weiter:
`UNGEKLÄRT / ZIEL ALLGEMEINGÜLTIG`.

Offen:
- realer Pferde-Live-Readback exakt 0.2.9;
- zweites reales Portal für formale Allgemeingültigkeit;
- Wissensdatenbankimport;
- größerer Performance-Test;
- Yoast-Kombination soweit release-relevant.

## Dauerregeln

**Unterschiedliche Paketbytes = unterschiedliche Pluginversion.**

**Technischer Kandidaten-PASS ist kein Pferde-LIVE-PASS.**
