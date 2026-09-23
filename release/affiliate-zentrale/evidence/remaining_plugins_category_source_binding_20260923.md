# Restplugin-Kategorieklassifikation – Quellenbindung – 2026-09-23

Status: BLOCKED_EXACT_SOURCE_BINDING

Scope: ausschließlich statische Pferdeportal-Kategorie-/Portalstruktur-Kopien. Keine Inhalts-, Design-, Performance-, Provider-, Ranking-, Banner- oder sonstige Pluginlogik.

Bereits geschlossen:
- Affiliate-Zentrale 6.72.152: CLOSED PASS
- PPM 6.7.9: CLOSED PASS
- PSERC 0.28.23: dynamischer Kategoriepfad PASS; kein 25er-Codepatch
- PSTE 0.57.6: CLOSED PASS, eine Map 1124 -> 1149

Noch exakt zu binden, bevor eine Kategorieabhängigkeit hart klassifiziert werden darf:
1. Affiliate Portal Template Kit 1.50.559
2. Allgemeine Bildzentrale 2.7.6
3. Portal Link Policy Runtime Verifier 1.0.0
4. Portal Production Center 1.1.1
5. Portal Production Link Policy Gate 1.0.1
6. Portal Category Structure Repair Guard 1.0.1

Geprüfte Quellenwege:
- PLUGINS-Büro: aktuelle installierte Versionen vorhanden, aber keine technischen Vollquellpfade für diese sechs aktuellen Versionen.
- DESIGN-Büro: ältere Template-Kit-Vollquellen/Belege; kein exakt gebundener 1.50.559-Vollbaum.
- BILD-Büro: Bürostand 2.6.9 / historischer Codebeleg 2.4.9; kein exakt gebundener 2.7.6-Vollbaum.
- TEXT-/GEMEINSAM-Büros: keine exakten Vollquellpfade für die vier kleinen aktuellen Plugins.
- main / article-production / aktuelle Produktionsbranches: keine passend benannten Quellordner oder Pakete für die sechs aktuellen Versionen.
- GitHub PR-/Commit-/öffentliche Indexsuche: kein exakter Vollquellbeleg dieser sechs Versionen.
- aktueller Chat: keine dieser sechs Quellpakete hochgeladen.

Fail-closed:
- Keine Kategorieänderung an diesen sechs Plugins.
- Keine Einstufung "keine statische Kopie" ohne exakte Quellprüfung.
- Keine Rekonstruktion aus älteren Versionen.
- Kein WordPress-Write.

Erster offener Bindungspunkt: Affiliate Portal Template Kit 1.50.559.
