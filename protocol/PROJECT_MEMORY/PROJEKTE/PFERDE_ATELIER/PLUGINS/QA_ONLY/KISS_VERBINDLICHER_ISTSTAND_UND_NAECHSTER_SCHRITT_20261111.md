# Pferdeatelier – verbindlicher Iststand / KISS-Zielvertrag (11.11.2026)

## Ziel – unverändert
Bestehender Workflow Keyword-/SEO-Recherche → PSTE-Freigabe → PSERC-Redaktionsplan → gültige Einzelübergabe → K0-Artikelproduktion. Bereits bestätigte Ergebnisse dürfen nicht durch unnötige Gesamtdurchläufe verloren gehen. **Datenbank tabu** (keine direkte DB-Änderung, Restore, Reset oder Schemaeingriff); keine erneute 5.000-Themen-Prüfung; kein zusätzlicher Code-/Pluginaufbau; K0 unangetastet. Nutzer nicht mit Zwischenarchiven/ungeprüften Plugins belasten.

## Tatsächlicher gesicherter Stand
1. Am 10.11.2026 waren drei Regendecken-Themen als READY für den bestehenden **Fünf-Felder-Metadatenexport** freigegeben. Originalplan, signierter Drei-Artikel-Batch und drei originale PRE_TYPE-SEO-Nachweise wurden aus damaligen Dateien gesichert und offline mit den existierenden Prüfern bestätigt.
2. Der später eingesetzte PSTE-0.57.144.37-Wiederanlauf hat laut WordPress-Flugschreibern 5.013 von 5.013 Themen erneut bewertet und dabei Datensätze tatsächlich geändert (kein reiner Lesevorgang, keine Anbieterabfragen). PSERC hat danach einen Plan mit 0 READY aktiviert. **Dieser Schaden ist nicht durch das Archiv einer Exportdatei behoben.**
3. Die Archiv-ZIPs **PSTE 0.57.144.32** und **PSERC 0.28.61** wurden tatsächlich gefunden, byteunverändert aus dem Archiv geprüft und mitsamt dem signierten Originalexport separat gesichert. Das ist ein verifizierter historischer **Code- und Exportstand**, **keine** Installation und **keine** nachgewiesene Wiederherstellung des aktuellen WP-Plans.
4. Der Drei-Artikel-Batch ist auch als drei einzelne Dateien für die bestehende K0-Eingangsvalidierung (ein Item pro K0-Lauf) vorbereitet und auf Hash/Fünf-Felder-Vertrag überprüft; diese drei Dateien sind **nur vorbereitete Eingaben**, keine geschriebenen Artikel und noch kein vollständiger K0-Auftrag. Für K0 werden je Item zusätzlich die eigene gültige redaktionelle Recherche-/Suchintent-Bindung und der Schreibkontext benötigt.
5. Neuere lokale Patchpakete PSTE .38 / PSERC .66 hatten lokal simulierte Prüferfolge, sind **nicht** in echtem WordPress abgenommen und **nicht** als Lösung freigegeben. Sie dürfen nicht mit Wiederherstellung verwechselt werden.
6. **Es wurde bislang keine WordPress-Instanz geändert, keine Datenbank angetastet, kein K0-Lauf gestartet und keine neue WordPress-Abnahme ausgeführt.** GitHub-/Library-Archivieren ist lediglich Dokumentation.

## Nachgewiesener Fehlerverlauf
- Falscher Vergleich signierter vierteiliger Suchprofile mit fünfteiligem Roh-Tupel führte zu falschen Quellenkonflikten.
- Unnötige Neubewertung wurde zum 5.013er-Wiederanlauf und speicherte negative Entscheidungen.
- PSERC ließ einen leeren 0-READY-Plan aktiv werden. So ging der früherer nutzbare Freigabestand im aktuellen WP-Testkontext verloren.
- Reines Rückkopieren alter Plugin-Dateien stellt **keine** überschriebenen gespeicherten Freigaben wieder her.

## Genau ein nächster operativer Arbeitsweg, ohne Minifixes
- **KEINE** weiteren Plugin-Downgrades/-Upgrades, Gesamtautomatik oder neue Datei-Downloads vom Nutzer verlangen.
- Auf Basis des **nachweislich vorhandenen Original-Fünf-Felder-Batches** und des **bestehenden K0-Eingangsvertrags** die bereits fertige Drei-Artikel-Übergabe als Ausgangspunkt verwenden; ausschließlich die bereits bestehenden K0-Validierungs- und Vorbereitungsschritte einsetzen, keine künstliche Neubindung, keine Behauptung einer fertigen K0-SEO-Herkunft, keine ungeprüfte Produktionsfreigabe.
- Die komplette automatische WordPress-Kette kann **ohne tatsächliche WP-Testabnahme und ohne gültige aktuell gespeicherte Freigaben nicht als repariert gelten**. Diese Grenze ausdrücklich benennen, statt wieder ein repariertes Plugin zu behaupten.
- Wenn ein K0-Lauf aus GitHub technisch möglich ist, **zuerst** die vorgesehene Laufablage, Portalauflösung, zwingenden Zusatzdateien und Sperren lesen; nur tatsächlich vollständig belegte Eingaben bereitstellen. K0-Produktionslogik nicht modifizieren.

## Anwenderaktion
**Derzeit keine.** Drei Einzeldateien sind Zwischenartefakte – Nutzer muss damit nichts machen. Kein neuer Download, kein Plugininstallations- oder Auto-Startauftrag.

## Status
`ORIGINAL_THREE_READY_EXPORT_VERIFIED`; `CURRENT_WORDPRESS_READY_ZERO`; `K0_SINGLE_ITEM_INPUTS_PREPARED_NOT_SUBMITTED`; `NO_DB_OPERATION`; `NO_WP_FIX_CONFIRMED`; `NO_K0_PRODUCTION`; `KISS_NO_MORE_PATCH_SPRAWL`.
