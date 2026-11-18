# Korrektur des Auftrags – Hobbydepot Texterstellung (18.11.2026)

## Verbindliche Betreiberweisung
**KEIN UMBAU, KEINE NEUE ARCHITEKTUR, KEINE EIGENENTWICKLUNG.** Einziger Auftrag: **bestehendes Texterstellungs-Plugin vom Pferdeatelier fachlich säubern** und als Hobbydepot-Kopie erhalten. Weder HD004 noch den Texterstellungsworkflow/Rechercheablauf oder K0 dabei neu entwerfen. Keine neue Diagnose, neue Zuordnung, neue Typregel oder zusätzliche Entscheidungsinstanz.

## Geprüfter Quellenvergleich
- Echte Quellen-ZIPs verglichen: Original `Texterstellung_KISS_0.4.23_TEST_MINI_Anleitung_K0_KISS.zip`, ursprüngliche Hobbydepot-Quellarbeitskopie `Texterstellung_HOBBYDEPOT_ARBEITSKOPIE_0.4.23.zip` und Zwischenfassungen 0.4.25/0.4.28.
- Die originale Hobbydepot-0.4.23-Arbeitskopie hat **78 ursprüngliche PHP-Quelldateien** und enthält weiterhin spezifische Pferdebegriffe in 4 Dateien (u.a. Magazinrouter, Artikeltypenregistrierung, Themennormalisierung) sowie genau zweimal die historische Import-Vertragskennung `PFERDE_ATELIER_WORDPRESS_IMPORT_V1`.
- Die Fassung 0.4.25 enthält zwar **keine** weiteren direkten Pferde-Schlüsselwörter aus der geprüft abgedeckten Wortliste, hat aber Änderungen außerhalb reiner Datenbereinigung. Deshalb ist sie **nicht** als unveränderte Architektur bescheinigt.
- 0.4.26–0.4.28 fügen mindestens `class-txe-hd004-category-audit.php` und `class-txe-hd004-category-binding.php` und zusätzliche Diagnose-/Freigabelogik hinzu. Das überschreitet den nun klargestellten Auftrag. **Diese Fassungen als Entwicklungsweg gestoppt, nicht weiterführen, nicht installieren.**
- Die zwei historischen Import-Kennungen und weitere vorhandene PSTE-/PSERC-Schnittstellennamen nicht blind umbenennen: Bestehende externe Kompatibilität darf nicht beschädigt werden.

## Zulässige Fortsetzung
1. Einzige Quellgrundlage: **bestehender ursprünglicher Texterstellung-0.4.23-Quellstand**, die Hobbydepot-0.4.23-Kopie als bereits angelegte Bereinigungs-Arbeitskopie. Keine HD004-Adapter aus Zwischenfassungen übernehmen.
2. Nur Pferdeatelier-spezifische Portaltexte, Beispieldaten, Seeds, Kategorien, fachliche Spezialfälle und Bezeichner **ohne Vertragsbindung** entfernen/neutralisieren. Keine neuen fachlichen Zuordnungsregeln als Ersatz erfinden.
3. Bestehende Methoden, Klassen, Hooks, Recherche-, MINI-, K0- und Importabläufe unverändert belassen; lediglich für Hobbydepot verpacken und vorhandenen PHP-Code auf Vollständigkeit, syntaktische Gültigkeit und versehentlich verbliebene Pferde-Fachreferenzen prüfen.
4. Reine Bereinigung dokumentieren: pro geänderter Datei Vorher/Nachher und Begründung. **Nur eine installierbare ZIP ausgeben, wenn sie tatsächlich geprüft und ohne zusätzliche Architekturänderung vollständig ist.** Vorher keine Installationsanweisung.

## Status und Verantwortung
- ***Scope reset / noch KEINE bereinigte freigegebene Installationsversion.***
- Nutzer muss **jetzt nichts** installieren oder exportieren. Keine DataForSEO-Abfrage, kein WordPress-/HD004-Sync, K0 unangetastet.
- Dieser Eintrag hat für den Auftrag Hobbydepot Texterstellung Vorrang vor den Ausweitungsideen in den 0.4.26–0.4.28-Berichten; Artefakte bleiben zur Historie erhalten.
