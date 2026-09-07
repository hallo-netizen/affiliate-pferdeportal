# PRODUKTVERGLEICH – CURRENT STATE

STAND: 2026-09-07
STATUS: AKTIV / 0.2.4 TECHNISCH PASS / NUTZER-LIVE-VERIFY OFFEN

## AUTORITÄT

Diese Datei ist die einzige aktuelle Büro-Standzusammenfassung.

- aktuelle Arbeit: `HOBBYRAUM.md`
- Fehlerdetails: über `FEHLERREGISTER.md` → `FEHLERQUELLEN.md`
- Ziel: über `ZIELVERTRAEGE/REGISTER.md` → `ZIELVERTRAG_V1.md`
- Warum: `AENDERUNGSREGISTER.md`
- Ausführungsprotokoll: `PROTOKOLL_20260907.md`

## AKTUELLER STAND

V1 läuft eigenständig und ohne STARTMASTER/TEXT-Laufzeitabhängigkeit:

`Produktwissen -> Vergleich -> gebundenes Dossier -> Zero-Freedom-Renderer -> Validator -> WordPress-DRAFT -> Link-/Grafikfinalisierung -> finaler Draft-Hash`

Affiliate = Commerce-Leseschicht.  
SEO = optionale read-only Signale.

Produktwissen bleibt:
`0.1.0-prototype`.

Aktueller Produktvergleichs-Kandidat:
`0.2.4-prototype`.

## 0.2.4 – TECHNISCHER BELEG

Plugin-Code:
- Menü-Hook-Fix: `3295653c19aed3a4af47aad73dc2226e0d7a9b78`;
- Bootstrap/Version: `47666ef1a0f1dbe36c5c8744382b52e178d734e9`.

Realtest:
Run `34154550626` → PASS.

Tatsächlich ausgeführt:
- saubere 0.2.4-ZIP gebaut;
- WordPress installiert und Plugins aktiviert;
- echter WordPress-HTTP-Server;
- echter Admin-Login;
- echte gerenderte `/wp-admin/`-Sidebar;
- Top-Level-Menü `Produktvergleich` sichtbar;
- echte Menüseite geladen;
- `PV-REG-001`-Draftweg weiterhin PASS;
- kein Publish.

Bereinigter Branch vor Abschluss-Nachholprüfung:
`d9460e19f30f9bbaff5e9d5c63e134f8d9a38333`;
Hardlock Run `34154765043` → PASS.

## NUTZER-LIVE-STATUS

Belegt:
Beim vorherigen 0.2.3-Schritt war auf der echten Pferde-Atelier-Seite **kein** Hauptmenüpunkt `Produktvergleich` sichtbar.

Noch **nicht** belegt:
- 0.2.4 auf der echten Nutzerseite installiert;
- Hauptmenü dort sichtbar;
- `PV-REG-001` dort als Draft erzeugt;
- Draft fachlich/visuell geprüft.

Daher:
**kein LIVE-PASS.**

## HARD RULES

- Writer/Renderer hat null freie Autorität.
- gleiche gebundene Eingaben + gleiche Versionen = identischer Output.
- fehlende/abweichende Bindung = BLOCKED.
- Produktvergleich = 2–4 konkrete konkurrierende Produkte aus mindestens zwei Herstellern.
- Variantenvergleich = Varianten desselben Basismodells.
- keine erfundenen Fakten, Ranglisten, Sterne oder pauschalen Testsieger.
- Quellenkonflikte/Lücken bleiben sichtbar.
- Affiliate darf keine fachliche Auswahl umschreiben.
- kein ähnliches Ersatzprodukt bei fehlendem Exact Match.
- interne Links nur gebunden.
- neutrale deterministische Grafik.
- kein Auto-Publish.

## NEXT ACTION

Ausschließlich `HOBBYRAUM.md`.
