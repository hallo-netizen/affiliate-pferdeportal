# BÜRO GLOSSAR – CURRENT_STATE

STAND: 2026-09-13
STATUS: EINZELARTIKEL LIVE FAIL BESTÄTIGT / 0.2.10-rc11-native-single KUBIO-INTEGRATION + PAKET PASS / PFERDE-LIVE-READBACK OFFEN

## Belastbarer aktueller Stand

- Büro `GLOSSAR` steuert das öffentliche Pferde-Atelier-Glossar.
- Fachwahrheit bleibt in `../WISSENSDATENBANK/AKTENSCHRAENKE/GLOSSAR/`.
- Vorhandene WordPress-Seite `Glossar` bleibt Hauptseite.
- `main` und das Pferde-Designplugin bleiben unangetastet.
- Arbeitsbranch: `hobbyroom/glossar-livefail-red-green-20260913`.

## Realer Nutzerbefund nach 0.2.10-rc7

Der Einzelartikel-Fehler blieb live bestehen. Der vom Nutzer gelieferte echte HTML-Anfang zeigte eine zweite komplette Dokumenthülle innerhalb des bereits geöffneten Kubio-`<head>`:

- erstes `<!DOCTYPE html>` / `<html id="kubio">` / `<head>`;
- danach innerhalb dieses Kopfes erneut `<!DOCTYPE html>` / `<html id="kubio">` / `<head>`.

Damit ist der frühere rc7-Klickbarkeitsbeweis für diesen Livefehler widerlegt. Ursache der Testlücke: Der alte Real-Design-Test prüfte den eigenen klassischen UGE-Single-Renderer unter rekonstruiertem Design und Loop-Poison, aber nicht die FSE/Kubio-Dokumenthülle auf genau einmal `DOCTYPE/html/head`.

## Aktueller technischer Kandidat

Version: `0.2.10-rc11-native-single`

Änderung gegenüber dem gebundenen rc7-Stand:
- ausschließlich die UGE-Übernahme der **Single-Template-Hülle** entfernt;
- Glossarbegriffe werden als öffentlicher `uge_term` nativ durch WordPress/Kubio gerendert;
- Taxonomie-/Kategorie-Template bleibt unter UGE-Kontrolle;
- rc7-Routing, Publikationspolicy und übrige Glossarlogik bleiben erhalten.

Build-/Test-Head:
`b0b6fb786bcafe37819700df019ec31a92a2dc30`

Workflow:
`.github/workflows/glossar-0210-rc11-native-single-hardtest.yml`

Run:
`34766187415` → SUCCESS

Jobs:
- Kubio Native Single Hardtest `103747455702` → SUCCESS
- Package `103747644208` → SUCCESS

## Harte Integrationsprüfung

Ausgeführt in echtem WordPress-Docker mit:
- aktivem Kubio-Theme;
- aktivem Kubio-Plugin;
- rekonstruiertem Pferde-Designplugin `1.50.469`, SHA-256 `580fa6c7f5566f29df9254ce92f687a4831554e1d84bf03fbd936bb7577edfe5`;
- echten veröffentlichten/draft/missing `uge_term`-Testdaten.

Positiv:
- `/glossar/begriff/hufbein/` → HTTP 200;
- echter Hufbein-Inhalt sichtbar;
- Kubio-Hülle vorhanden;
- exakt **1× DOCTYPE, 1× html, 1× head**.

Negativ/Regression:
- Draft-Begriff → 404, Draft-Inhalt nicht sichtbar;
- unbekannter Begriff → 404;
- normaler WordPress-Beitrag → 200, Inhalt sichtbar, nur eine Dokumenthülle;
- Glossar-Taxonomie weiterhin 200;
- klassischer UGE-Single-Full-Document-Renderer wird nicht mehr ausgewählt.

Belegmarker:
- `UGE0210RC11_KUBIO_PUBLISHED_SINGLE_VISIBLE_PASS`
- `UGE0210RC11_KUBIO_SINGLE_DOCUMENT_SHELL_EXACTLY_ONCE_PASS`
- `UGE0210RC11_DRAFT_AND_MISSING_NEGATIVE_PASS`
- `UGE0210RC11_UNRELATED_POST_REGRESSION_PASS`
- `UGE0210RC11_TAXONOMY_UNCHANGED_PASS`

## Paket

Installierbares Paket:
`universal-glossary-engine-0.2.10-rc11-native-single.zip`

Innerer Plugin-ZIP SHA-256:
`45c8f4d2a01883b6bb548c8db2db8bf9b19f5ddc80cb346b647d992fca7f748f`

Actions-Artefakt:
- ID `10320871739`
- Outer artifact SHA-256 `8ced9d219a6a38d81ab9be50fe146dc8a5acfa6a8e58a0154f5e84410d450434`

Nach Download des Actions-Artefakts wurde der innere Plugin-ZIP erneut geprüft:
- SHA-256 identisch → PASS;
- ZIP-Lesetest → PASS;
- Version → PASS;
- Single-Template-Übernahme fehlt wie vorgesehen → PASS;
- Taxonomie-Template-Übernahme bleibt vorhanden → PASS.

## PASS-Grenze

**rc11 Kubio/WordPress Positiv-/Negativ-/Regressionstest: PASS.**

**Exakt daraus gebautes und hashgebundenes Paket: PASS.**

**Pferde-LIVE-PASS: NEIN / OFFEN.**

Nächster Schritt ist ausschließlich die reale Installation dieses exakten Pakets und der direkte Live-Klick auf einen Glossarbegriff. Erst ein realer Nutzer-Readback darf `GLOSSAR-ROUTE-004` live schließen.
