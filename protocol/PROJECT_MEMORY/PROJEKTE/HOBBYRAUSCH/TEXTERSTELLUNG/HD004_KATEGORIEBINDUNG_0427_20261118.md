# Hobbydepot Texterstellung 0.4.27 – 18.11.2026

**Status: NUR ARBEITSKOPIE, NICHT INSTALLIEREN. Keine Live-Freigabe.**

### Genau nachgewiesen und umgesetzt
- 0.4.26 geöffnet; alte Methode `TXE_Workshop::checkedCategory` prüfte lediglich vorhandenes WordPress-Term, nicht die zentrale HD004-Zuordnung.
- Neue, zentrale **lesende** `TXE_HD004_Category_Binding::resolveSlug` ersetzt exakt diese alte Prüfung. Prüft Registryvertrag, Revision, eindeutiges Term-Mapping und Parent-Verbindung über HD004 bis zu einer vorhandenen Hobbyseite; erlaubt logische Relation-Knoten ohne vorgetäuschte WordPress-ID. Keine zweite Kategorie-Wahrheit und **keine** Artikelart aus Labeln.
- Tests: 20/20 synthetische HD004-Fälle; 81/81 PHP-Lint; 90/90 ZIP-Prüfung. Nur 2 Dateien geändert, 1 PHP-Datei neu; 4 original PSERC Import-PHP-Dateien bytegleich.
- Alte historische `PFERDE_ATELIER_WORDPRESS_IMPORT_V1`-Kennung bleibt zweimal allein aus Kompatibilitätsgründen bestehen. Keine alten Pferde-Domäneninhalte eingeführt.
- Dateien-Büro: `/hobbydepot/TEXTERSTELLUNG/ARBEITSKOPIEN/HOBBYDEPOT_TEXTERSTELLUNG_0.4.27_QUELLE_NICHT_INSTALLIEREN.zip`.
- SHA256 ZIP `e4183bbc4da2e3516644b42923110380131b3c328295b8419c4467bc1ef9280a`.
- Prüfnachweis: `/hobbydepot/TEXTERSTELLUNG/PRUEFBERICHTE/HOBBYDEPOT_TEXTERSTELLUNG_0.4.27_STAND.md` und `.../HOBBYDEPOT_TEXTERSTELLUNG_0.4.27_PRUEFBERICHT.json`.

### Nachweislich offen
1. Die übrigen ORIGINAL-PSTE-Recherchepfade verwenden noch ihre eigene Familienstruktur; Einzelkategorieprüfung ersetzt nicht deren vollständige HD004-Anbindung. Ein aktueller tatsächlicher WordPress-HD004-Snapshot/Readback von hobbydepot.de liegt nicht als Quelle vor.
2. Der einzige zugängliche K0-Multiportalbestand `hallo-netizen/k0-multiportal` ist laut README **Quarantäne, keine Produktion**. Die archivierten vier K0-Typen sind keine gültige Produktionsfreigabe. Das im Archiv enthaltene einzelne Hobbybeispiel `discgolf-beratung` deckt Hobbydepot nicht ab. Die Plugin-Fähigkeitsquelle bleibt deshalb **PENDING**; kein erfundener Typenvertrag, kein K0-Umbau.

### Wer handelt?
- Entwicklung: eine gebündelte Fachanbindung HD004→PSTE-Recherche und die aktuelle K0-Typ-/Portalquelle nachweisen. Ursprünglicher K0/PSERC-Import bleibt unverändert.
- Betreiber: **jetzt nichts installieren**. Erst nach echtem erfolgreichen WordPress-/DataForSEO-/MINI-/K0-Durchlauf eine einzige Installationsversion erhalten.

Unverändert: 0.4.23–0.4.26, HD004, Pferdeatelier, K0 und WordPress-Daten.
