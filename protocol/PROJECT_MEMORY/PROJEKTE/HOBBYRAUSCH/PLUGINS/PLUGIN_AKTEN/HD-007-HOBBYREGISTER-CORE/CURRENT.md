# HD-007 – HOBBYREGISTER CORE – CURRENT

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-23
STATUS: **1.1.3 MAGAZIN-BREADCRUMB + PFERDERASSEN-SIDEBAR-TRANSFER LOCAL HARD PASS / CYBERDUCK-INSTALLATION OFFEN**

Plugin-ID:
HD-007-HOBBYREGISTER-CORE

Artefakt:
`HOBBY_DEPOT_HOBBYREGISTER_CORE_HD007_V1.1.3_FULL_MAGAZIN_SIDEBAR.zip`

SHA-256:
`c628730a81579dc70d3141b73ce591292613bb44431ac9c43969f1473d748c31`

Größe:
1,349,148 Bytes.

Hauptordner:
`hd-hobbyregister-core/`

## Magazin-Hierarchie

Registerstart:
**Startseite › Magazin › Hobbyregister**

Detailprofil:
**Startseite › Magazin › Hobbyregister › Hobby**

Damit bleibt das Register separat im Footer erreichbar, wird in der Nutzerführung aber unter dem Magazin als Überbau eingeordnet.

## Detailseitenleiste

Nach dem bewährten Pferderassen-Prinzip übertragen:

1. Auf einen Blick.
2. Zur gleichen Hobbygruppe:
   - 3 Bildvorschauen;
   - Titel;
   - kurzer Vorschautext;
   - klickbarer Verweis;
   - Button zur Hobbygruppe.
3. Ähnliche Hobbys:
   - 4 Bildvorschauen;
   - Titel;
   - kurzer Vorschautext;
   - klickbarer Verweis.
4. Button zum Hobbymagazin.

Der zusätzliche frühere Block „Ähnliche Hobbys“ unter dem Haupttext ist entfernt. Es gibt ihn nur einmal in der linken Spalte.

## Weiterhin erhalten

- 862er read-only Register;
- acht Schema-F-Fließtextabschnitte je Detailprofil;
- Iconnavigation auf der Registerübersicht;
- ungefilterte Startseite ohne „862 Treffer“;
- Bannerplatz auf Registerübersicht und Detailseite;
- keine neue Datenbank / keine DB-Writes.

## QA

- PHP-Lint PASS;
- Fresh-Unpack PASS;
- Magazin-Breadcrumb PASS;
- gleiche Hobbygruppe + Bildkarten PASS;
- Gruppenbutton PASS;
- ähnliche Hobbys + Bildkarten PASS;
- „Ähnliche Hobbys“ nur einmal im Detailtemplate PASS;
- 862er Register/Textsystem erhalten.

Evidence:
`EVIDENCE_1.1.3.md`

## EXAKT EINE NEXT ACTION

**Gemeinsames Bundle `HOBBY_DEPOT_AKTUELL_20261023_MAGAZIN_FOOTER_REGISTER_FINAL.zip` entpacken und `hd-hobbyregister-core` per Cyberduck über den vorhandenen Ordner unter `wp-content/plugins/` zusammenführen. Danach Registerstart und ein Detailprofil live prüfen.**
