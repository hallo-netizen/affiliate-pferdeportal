# Hobbydepot – erster konkreter Test mit drei kompletten Artikeln (21.11.2026)

**Ergebnis: 14/14 gezielte Prüfungen BESTANDEN. WordPress-IMPORTFREIGABE weiterhin NICHT erteilt.**

## Was wirklich ausgeführt wurde

- Die **drei vorhandenen vollständigen Hobbydepot-FAQ-Artikeltexte** wurden aus dem älteren echten GitHub-Actions-Entwurf `KMulti-Hobby-3-FAQ-Offline-Preview-Not-Approved` rekonstruiert und an den drei dokumentierten Wortlautstellen aktualisiert. Danach wurden **alle drei kompletten HTML-Texte auf Byte-Inhalt per SHA256 gegen den späteren echten GitHub-LanguageTool-Prüfbericht** abgeglichen: **3/3 exakt gleich**. Es wurden keine Artikel erfunden oder umgeschrieben.
- Die drei tatsächlichen aktuellen Artikeltexte wurden dann dem **unveränderten Original-PHP-Importer** `PSERC_System4_Import::normalizePayload()` aus Hobbydepot-Plugin **0.4.24.18** zur Prüfung vorgelegt; Original-Plugin-ZIP-SHA256 `03f21ca678f003ab55a2a3a86ccd44c0cceb1e6a758b6bb129de19b`. Ergebnis **`PSERC_SYSTEM4_PAYLOAD_VALID`, drei Artikel, `publish_allowed=false`**, alle drei HTML-Prüfsummen im PHP-Ergebnis exakt gleich den real geprüften GitHub-Artikelfassungen.
- Zusätzlich sechs fehlerhafte Eingaben wirklich in **demselben originalen PHP-Importer** ausgeführt. Alle sechs **BLOCKED**: falscher Planplatz, doppelter/abweichender Planplatz, leerer Titel, ungültiger Slug, abweichende Artikel-ID, falscher Importvertrag.
- Der **neueste echte LanguageTool-6.8-Java-Test** aus GitHub-Actions-Lauf [44889447704](https://github.com/hallo-netizen/k0-multiportal/actions/runs/44889447704) wurde als tatsächlich hochgeladenes Ergebnis-Archiv heruntergeladen, geöffnet und pro Artikel anhand des exakten HTML-Prüfsummenwerts mit unserem PHP-Eingang verglichen: **3/3 PASS, 0 offene Befunde**. `Instinktivbogen` wird als originale DSB-Fachbezeichnung fachlich berechtigt zugelassen. Das zuvor verfügbare ältere LanguageTool-Archiv `44889232888` war nicht mehr der aktuelle Prüfstand.
- Die ebenfalls original heruntergeladene [Quellenprüfung 44889232903](https://github.com/hallo-netizen/k0-multiportal/actions/runs/44889232903) enthält **30/30 absatzweise geprüfte Textstellen, 10 tatsächlich geladene Originalquellen, 16 wörtlich gefundene Belegstellen**. **`research_complete=false`**: Quellentext-Treffer sind ausdrücklich keine vollständige fachliche Quellenfreigabe.

## Gezielt geprüfte Originaltexte

| Nr. | Originaler WordPress-Titel | Vollständiger HTML-SHA256 |
|---|---|---|
| 1 | Ist Bogenschießen ein teures Hobby? | `3cf2005d240326f4a5d42514d2729b6ee929443d130fde771126b6f452e20b8a` |
| 2 | Welche Regeln gelten beim 3D-Bogenschießen? | `060d558d27b1f8599295361fd5842503531b55c23f54831e32bb224c77f96fe0` |
| 3 | Wie finde ich einen 3D-Bogenschießen-Parcours? | `ea8bba5d1657265fac7cd33d52841f589d668ee5bb2d0444157d18c4b39d2560` |

**Zählung 14/14:** Drei Gleichheitsprüfungen zwischen aktuellem HTML und echtem LanguageTool-Artikelbeleg; ein echter positiver PHP-Importformatlauf; sechs echte PHP-Negativläufe; drei artikelweise Prüfungen des echten aktuellen LT68-Artefakts; ein Abgleich des vorhandenen echten Quellen-Audit-Artefakts. *Es wurden nicht 14 vollständige End-to-End-Produktionsläufe durchgeführt.*

Vollständiger lokal erstellter JSON-Testbericht mit Positiv-/Negativergebnissen: `HOBBYDEPOT_ERSTER_ARTIKEL_FORMATTEST_ERGEBNIS_20261121.json`, SHA256 `979f0b1c0b8e66f5ee35cea9a94551a624e1b1fd13ac70983c13b1bb510509a9`. Er wurde in der Chat-Sitzung als Download bereitgestellt. **Nicht** die im selben lokalen Testordner liegende rekonstruierte Probe-Importdatei hochladen: sie ist ausdrücklich `DO_NOT_IMPORT`, weil es noch keine echte K-Multi-Gesamtfreigabe gibt.

## Einziger verbleibender Block für eine finale Importfreigabe

- Vollständig unterschriebene/verbindlich freigegebene gemeinsame Fakten- und Autorenprüfung fehlt (Quellenaudit ist keine Freigabe).
- Eigenes vollständiges Hobby-Artikelregelbuch ist noch kein aktiver, verbindlich genehmigter 121-Regeln-Durchlauf. `hobby_depot=NO_VALUES_BLOCKED`, `production_enabled=false`.
- Für `Pflege` und `Anleitung` hat K-Multi derzeit weiterhin einen gemeinsamen technischen Verweis, während auf Hobbydepot-Seite eigenständige Regeln vorbereitet sind; beim hier getesteten FAQ-Auftrag war die Zuordnung korrekt.
- Es gab **keinen** echten WordPress-Live-Datenbanklauf und keine K-Multi-genehmigte WordPress-Importdatei. Ein Import allein wegen korrektem PHP-Format wäre unzulässig.

**Änderungsgrenze:** K0, das Original-K-Multi-Programm, K-Multi-Registry, K-Multi-Bindings, Original-Hobbydepot-WordPress-Plugin und WP-Aufträge **unverändert**. Hier nur ein echter lokaler Test und diese fachliche Dokumentation. **Kein neues Plugin, keine Installation, keine Veröffentlichung.**
