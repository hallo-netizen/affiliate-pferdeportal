# AFFILIATE – HOBBYRAUM

STAND: 2026-09-07
STATUS: AKTIV

## 1-KLICK-ÜBERSICHT

**WAS IST DAS?**  
Der einzige aktuelle Arbeitsraum des Büros AFFILIATE.

**AKTUELLER AUFTRAG:**  
**OTTO in die bestehende Affiliate-Zentrale integrieren. Digistore24 bis auf Weiteres zurückstellen.**

**DU DARFST …**  
den gebundenen OTTO-Auftrag und seine Quellen lesen, prüfen und ausschließlich im bestehenden Affiliate-/Awin-/Produktquellenweg bearbeiten.

**DU DARFST NICHT …**  
einen separaten OTTO-Gesamtworkflow, ein neues Parallel-Plugin oder eine neue Netzwerkarchitektur erfinden; Digistore24 nebenbei weiterbearbeiten; OTTO ohne realen Feed-/Zugangsbeleg öffentlich aktivieren.

**ALS NÄCHSTES …**  
bestehenden OTTO-Vorbau gegen den realen Awin-Zugang prüfen und die kleinstmögliche Integrationslücke bestimmen.

## ARBEITSKONTROLLPUNKT – NUR DIE AKTUELLE ARBEIT

- **BÜROSTAND:** `CURRENT_STATE.md`
- **AKTUELLER AUFTRAG / NEXT ACTION:** ausschließlich diese `HOBBYRAUM.md`
- **CURRENT_BLOCKER:** nicht hier duplizieren → `protocol/PROJECT_MEMORY/FEHLERREGISTER.md` → autoritative Quelle
- **AKTIVER ZIELVERTRAG:** nicht hier duplizieren → `protocol/PROJECT_MEMORY/ZIELVERTRAEGE/REGISTER.md`
- **NICHT ANFASSEN / WARUM:** nicht hier duplizieren → Ziel-/Originalquelle + `protocol/PROJECT_MEMORY/AENDERUNGSREGISTER.md`

**Wenn zwei Angaben widersprechen:** nicht raten. Die oben benannte autoritative Quelle gewinnt.

## NEXT ACTION – OTTO

1. Den vorhandenen OTTO-Eintrag in `class-ppar-product-source-plan.php` und den bestehenden Awin-Weg als Ausgangspunkt verwenden.
2. Prüfen, welche reale OTTO-/Awin-Quelle nach der Programmzusage verfügbar ist: insbesondere Produktfeed, Tracking-/Deeplinkdaten und Pflichtfelder.
3. Danach nur die **kleinstmögliche** Lücke schließen:
   - OTTO innerhalb des bestehenden Awin-/Produktquellenwegs aktivierbar machen;
   - keine Doppelarchitektur;
   - zentrale Zuordnung, Produktkarten, Trackingprüfung und Fail-Closed-Regeln wiederverwenden.
4. Vor `active` und vor öffentlicher Ausgabe Positiv-/Negativprüfung mit realen OTTO-Daten.
5. Digistore24 bleibt während dieses Auftrags unangetastet.

## Konzeptbindung

Die vorhandene Affiliate-Recherche bleibt gültig:
**möglichst wenige stabile Kernquellen statt viele Sonderadapter.**
Awin ist Kernnetzwerk; OTTO wird deshalb als Awin-Produktquelle eingebunden.

## Fachweg bei der technischen Arbeit

`control/release-governance/CURRENT_RELEASE.json`
und
`release/affiliate-zentrale/AGENTS.md`
bleiben technische Autoritäten.

Vor einem Codefix zusätzlich die dokumentierte Differenz GitHub 6.72.1 ↔ WordPress live 6.72.2 beachten.

## Globale Arbeitsort-Sperre

**Tresor, Archiv, Backup und Git-Mirror sind niemals Werkbank oder Runner-Quelle.**

Autorität:
`protocol/PROJECT_MEMORY/BAUCONTAINER/EINGANGSSTANDARD.md` → **Backup-/Tresor-/Archiv-Sperre**.
