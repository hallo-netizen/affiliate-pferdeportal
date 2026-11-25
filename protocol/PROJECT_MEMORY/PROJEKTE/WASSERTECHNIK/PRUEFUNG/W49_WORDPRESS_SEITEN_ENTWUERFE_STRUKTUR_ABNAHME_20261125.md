# W49 – WordPress-Seitenliste bestätigt Entwürfe; Kategoriekonzept als Struktur abgeschlossen
**25.11.2026 · echter Nutzer-Screenshot aus „Seiten → Alle Seiten“, WordPress-Admin**

## Originalbeleg
Screenshot aus WP-Backend `/wp-admin/edit.php?post_type=page`, als Originaldatei im persönlichen Wassertechnik-Pluginbüro archiviert:
`/Wassertechnik/Plugin-Büro/W49_WP_SEITEN_197_EINTRAEGE_ENTWUERFE_2026-11-25.png`.

## Tatsächlich zu erkennen
- Liste zeigt rechts oben **197 Einträge**. Dies ist vereinbar mit **195** in W35 bestätigten Wassertechnik-Seiten plus **2 weiteren** gewöhnlichen WordPress-Seiten, aber der Screenshot belegt nicht für alle 197 eine einzelne Eigentümerzuordnung.
- Die **sichtbaren Wassertechnik-Seiten**, darunter Abwasser & Entwässerung, Abwassertank, Grauwasseranlage, Fettabscheider, Rohrreinigungsmaschine, sind ausdrücklich jeweils **„Entwurf“**.
- Die Filterzeile **„Veröffentlicht/Entwurf“** ist durch Scrollposition oberhalb des sichtbaren Bildausschnitts verborgen. Der Screenshot belegt deshalb **nicht**, dass jede der 197 Seiten ein Entwurf ist. Keine Behauptung von „0 veröffentlichten Seiten“ insgesamt.
- W47 (390 von 390 W35-Zielen vorhanden, null fehlende und null Konflikte) und W48 (sieben Hauptbereiche + separater Fachzugang sichtbar; **0** Produktlinks in der Navigation) sind weiterhin gültig.

## Technischer Abgleich mit bestehendem Originalcode
- W35 zählt Seiten unabhängig vom Publikationsstatus und legt neu fehlende Seiten absichtlich mit `post_status=draft` an. W44 hat den einen bestehenden Importer auf **195 Seiten und 195 Beitragskategorien** erweitert; 81 neue Produktarten bleiben bewusst unveröffentlichte Entwürfe.
- Die vorhandene W42/W44-Navigation verlinkt nur Seiten mit `post_status=publish`, korrekt passendem `_wt_owner_id` und erwartetem Pfad. Für alle sichtbaren Entwürfe ist es daher **beabsichtigt**, dass sie im Menü fehlen.
- Dass wirklich alle **79 alten Produktseiten** Entwürfe sind, ist durch den sichtbaren Ausschnitt nicht unmittelbar bewiesen. Sollte später eine nachweislich veröffentlichte passende Produktseite im Menü fehlen, ist eine konkrete Owner-/Pfadprüfung nötig. Keine pauschale Fehlerbehauptung und keine ungeprüfte Massenveröffentlichung.
- Externer Webzugriff auf Startseite und stellvertretende alte/neue Umzugs-URL `/bewaesserung/gartenschlauch/` und `/brunnen/bewaesserung/gartenschlauch/` blieb im jetzigen Prüflauf **nicht erreichbar**. Damit kein echter HTTP-301-Status bestätigt. Bei nicht veröffentlichtem Ziel kann die absichtlich geschützte Weiterleitung zudem ausbleiben.

## Projektentscheidung
- **Kategoriekonzept und WordPress-Struktur: ALS STRUKTUR ABGESCHLOSSEN.** W27-Fachentscheidung steht, DataForSEO 81/81 echt abgeschlossen zu 0,13344 USD, 218 alte SEO-Begriffe geschützt. In WP existieren 390/390 Zielobjekte (195 Seiten und 195 Inhaltskategorien), keine W35-Konflikte, die sieben kaufnahen Hauptbereiche + Fachtechnik sind sichtbar.
- **Noch nicht abgeschlossen:** öffentliche Publikationsreife, tatsächliche Produktlinks, inhaltliche Freigaben und verifizierte 17 HTTP-301-Weiterleitungen. Das gehört zum **nachfolgenden Inhalts-/Veröffentlichungsschritt**, nicht zur erneut auszuführenden Kategorienanlage.
- **Nächste fachliche Arbeit:** Nur echte fertig geschriebene Produktseiten nach den üblichen Inhalts-/SEO-Regeln veröffentlichen; dann prüfen, dass die Menülinks erscheinen. Weiterleitungen bei tatsächlich veröffentlichten Zielseiten kontrollieren. **Keine leeren Entwürfe massenweise veröffentlichen.** Kein erneuter W35-Import, keine neue DataForSEO-Zahlung, kein zusätzliches Diagnoseplugin.

## Aktueller Plugin- und Archivstand
WP-Installation: Nutzer bestätigt WT001 **0.1.14 W44**. Identisches ZIP im persönlichen Archiv nochmals überprüft:
`/Wassertechnik/Plugin-Büro/WASSERTECHNIK_KATEGORIE_WORKFLOW_0.1.14_W44_KOMPLETTUPDATE_INSTALLIEREN.zip` (103.184 Byte, W44 SHA-256 `6ab38d967dcc7ca018b0286007e1826960e086a2d879f71844035e814fa579a8`). Vorgänger 0.1.13 weiterhin im Archiv. **Kein neuer Pluginbau erforderlich**; screenshot wurde ergänzend archiviert.
