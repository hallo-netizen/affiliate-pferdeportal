# DESIGN – HOBBYRAUM

STAND: 2026-09-07
STATUS: AKTIV

## 1-KLICK-ÜBERSICHT

**WAS IST DAS?**  
Der einzige aktuelle Arbeitsraum des Büros DESIGN.

**HIER BIST DU RICHTIG, WENN …**  
du die aktuell gebundene Pferde-Atelier-Designänderung prüfst oder fortsetzt.

**DU DARFST …**  
den gebundenen Auftrag und seine Quellen lesen und ausschließlich im ausdrücklich gebundenen Arbeitsweg ändern.

**DU DARFST NICHT …**  
`main` verändern, V104 still ändern, einen zweiten Parallelweg eröffnen oder aus dem Kandidaten bereits einen LIVE-Stand ableiten.

**ALS NÄCHSTES …**  
Kandidat V1.50.473 installieren und visuell auf „Gebisse“ plus mindestens einer weiteren Seite derselben Kategorieebene prüfen.


## AKTUELL GEBUNDENER AUFTRAG

Ziel:
Die zentrale Kategorieebene wird in dieser Reihenfolge ausgegeben:

1. H1;
2. Unterkategorie-/Beitragsart-Verweise;
3. unveränderter Kategorienartikel;
4. Beitragsvorschau / meistgelesene Beiträge;
5. kommerzielle Blöcke.

Arbeitsbranch:
`fix/category-content-order-v150473-20260907`

Beleg:
`design-baseline/2026-09-07/v150473-category-content-order/`

Kandidat:
`PFERDE_ATELIER_DESIGN_V1.50.473_CONTRACT_V104_KATEGORIE_REIHENFOLGE_INSTALLIEREN.zip`

Status:
lokale Positiv-/Negativprüfung PASS; **noch kein LIVE-PASS**.

## ARBEITSKONTROLLPUNKT – NUR DIE AKTUELLE ARBEIT

- **BÜROSTAND:** `CURRENT_STATE.md`
- **AKTUELLER AUFTRAG / NEXT ACTION:** ausschließlich diese `HOBBYRAUM.md`
- **CURRENT_BLOCKER:** nicht hier duplizieren → `protocol/PROJECT_MEMORY/FEHLERREGISTER.md` → autoritative Quelle
- **AKTIVER ZIELVERTRAG:** nicht hier duplizieren → `protocol/PROJECT_MEMORY/ZIELVERTRAEGE/REGISTER.md`
- **NICHT ANFASSEN / WARUM:** nicht hier duplizieren → Ziel-/Originalquelle + `protocol/PROJECT_MEMORY/AENDERUNGSREGISTER.md`

**Wenn zwei Angaben widersprechen:** nicht raten. Die oben benannte autoritative Quelle gewinnt.

## Harte Grenze

Bis zur Nutzerprüfung bleibt `CURRENT_STATE.md` unverändert auf dem bestätigten LIVE-Stand V1.50.472 / V104.

Kein Merge auf `main`; keine Änderung an Texten, Kartenlogik, Beitragsauswahl, Affiliate-Auswahl oder V104.

## Historie

Nicht hier dupliziert. Siehe `CURRENT_STATE.md`, `protocol/PROJECT_MEMORY/AENDERUNGSREGISTER.md` und `protocol/PROJECT_MEMORY/ARCHIV/REGISTER.md`.

## Globale Arbeitsort-Sperre

**Tresor, Archiv, Backup und Git-Mirror sind niemals Werkbank oder Runner-Quelle.**

Autorität:
`protocol/PROJECT_MEMORY/BAUCONTAINER/EINGANGSSTANDARD.md` → **Backup-/Tresor-/Archiv-Sperre**.
