# W8 – Importfähigkeit der vorhandenen WT001-Version

**Stand 14.11.2026. Echten ZIP-Inhalt auf GitHub geprüft; keine WordPress-Änderung.**

## Nachgewiesen
- Die installierte/archivierte WT001 Version 0.1.4 enthält sechs ZIP-Einträge: Hauptdatei, Inventur-Klasse, DataForSEO-Klasse, bezahlte Recherche-Klasse, SEO-Asset, README.
- Die vier PHP-Dateien wurden entpackt, ihre Funktionen und übliche WordPress-Inhalts-Schreibbefehle untersucht. **Keine Funktion für Anlage von Seiten oder Beitragskategorien vorhanden.** Der Programmtext bezeichnet diese Version ausdrücklich als reine Inventur-/SEO-Lösung.
- Der W4-Fachbaum, W5-SEO-Ergebnisse, W6-Importvorschau und W7-Megamenü-Entwurf bleiben unverändert. W6 ordnet **113 WP-Seiten und 105 Beitragskategorien** zu, insgesamt 218 Owner.
- Vorhandener WordPress-Snapshot vom 14.11.2026 12:28:47 UTC: 2 Standardseiten, 1 Beitrag, 1 Standardkategorie. Er ist nicht der aktuelle Livezustand.
- Das W7-Megamenü wurde nur schreibfrei geplant, **nicht** live auf Desktop/Mobil geprüft.

## Eine fehlende Hauptfunktion
Die bestehende Pluginidentität `wassertechnik-kategorie-workflow` um **einen** ADD-only-Importer erweitern, keine zweite Pluginlinie:
1. **Einmalige Gesamtentscheidung:** W6 als einzige Importziel-Liste (113 WP-Seiten und 105 WP-Kategorien); W4 Fachquelle, W5 nur SEO-Priorität, W7 nur Menü-Ansicht. Unterste Seitenebene konkretes Produkt/System; Kategorien flexibel und produktbezogen; ungefähr 3–5 plausible Artikelideen nur **weiche** Orientierung.
2. **Ein Gesamt-Preflight unmittelbar vor dem Import:** tatsächlichen WP-Bestand, Ziel-Site, Berechtigung, Backup, vorhandene Pfade/Slugs sowie stabile Owner zuordnen; fehlende Objekte bestimmen. Keine unabhängigen nachgelagerten Inhaltsentscheidungen.
3. **Ein schreibender Import erst nach ausdrücklicher Freigabe:** nur fehlende Seiten und Kategorien; Eltern vor Kindern; stabile Owner-Kennung, Unterbrechung ohne Duplikate fortsetzen. Vorhandene Standardobjekte nicht blind löschen, bestehende Objekte nicht überschreiben.
4. **Einmaliges WordPress-Readback** des neuen Gesamtbestands. Keine Artikel aus 356 groben Ideen, keine doppelte SEO-Recherche, keine neue API-Kosten.
5. Produktbezogene Beitragskategorien im Produktkontext anzeigen und das vorhandene Design für ein ausgewogenes Desktop/Mobil-Megamenü verwenden – erst nach gesonderter Frontendfreigabe.

**Grenze:** Diese W8-Datei ist der überprüfte Ist-Zustand und die einmalige Umsetzungsvorgabe, **kein fertig gebautes Importmodul** und keine Importfreigabe. Noch kein neues ZIP und kein WordPress-Schreiben.
