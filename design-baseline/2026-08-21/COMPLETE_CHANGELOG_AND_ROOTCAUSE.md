# Design-Baseline-Audit 2026-08-21

## Ergebnis

Der V93-Master ist archivseitig intakt und sein SHA-256-Manifest ist vollständig gültig. Die eingebetteten Installer sind die maßgebliche Runtime-Basis V89.

**Gefundene strukturelle Schwachstelle:** `CURRENT_PLUGIN_SOURCE` in beiden V93-Mastern wurde nach V83 nicht mit dem eingebetteten V89-Installer synchronisiert. Dadurch kann ein Build, der blind `CURRENT_PLUGIN_SOURCE` verwendet, echte spätere Änderungen verlieren.

Die heute erzeugten V94-Installer wurden dagegen nach Hash-/Dateivergleich aus dem **eingebetteten V89-Installer** fortgeführt: beim Pferde-Plugin sind 488/492 Produktionsdateien byteidentisch, geändert wurden nur Haupt-PHP, Einzelbeitrags-CSS und die Contract-Dateinamen/-texte. Beim Universal-Plugin sind 10/15 Dateien byteidentisch, geändert wurden nur Hauptdatei, Renderer, CSS, Readme und Contract.

## Live-Akzeptanz laut Nutzer

- Tabellen Einzelbeitrag: PASS
- Beitragsvorschau Journal-Root: PASS
- Beitragsvorschau Journal-Kategorien: FAIL

Der FAIL liegt in dem neu hinzugefügten V94-Journal-Kategorie-Kartenblock. Er darf nicht als stabiler Nullpunkt gelten.

## Verbindlicher nächster Build

1. Ausgangsbasis ist ausschließlich der hier gehashte V94-Kandidat bzw. für Rückbau der gehashte V93-V89-Installer.
2. Tabellen-PASS und Journal-Root-PASS müssen byte-/regelbezogen erhalten bleiben.
3. Nur der Journal-Kategorie-Kartenblock darf korrigiert werden.
4. Vor Freigabe muss der komplette Pluginbaum gegen diese Manifeste verglichen werden.
5. `CURRENT_PLUGIN_SOURCE` und eingebetteter Installer müssen danach **100 % identisch** sein (abgesehen von dokumentierten Master-only Dateien).

# STATE JSON
```json
{
  "timestamp": "2026-08-21T10:04:00+02:00",
  "stable_contract_baseline": {
    "pferde_design": "1.50.458 / runtime V89, master contract V93",
    "universal_design": "2.2.29 / runtime V89, master contract V93",
    "pferde_search": "2.1.5 / contract V93",
    "universal_search": "2.1.5 / contract V93"
  },
  "current_v94_candidate": {
    "pferde_design": "1.50.459 / Contract V94",
    "universal_design": "2.2.30 / Contract V94",
    "user_live_acceptance": {
      "single_post_tables": "PASS",
      "journal_root_post_preview": "PASS",
      "journal_category_post_preview": "FAIL (oversized/wrong card layout)"
    }
  },
  "critical_master_inconsistency": {
    "pferde_master_CURRENT_PLUGIN_SOURCE": "stale at V83 relative to embedded V89 installer; 488/492 same, 2 changed, 2 contract filename replacements",
    "universal_master_CURRENT_PLUGIN_SOURCE": "stale at V83 relative to embedded V89 installer; 11/15 same, 3 changed, 1 contract filename replacement",
    "embedded_installers": "authoritative for V93 runtime; both master manifests verify 100%"
  },
  "v94_delta_from_authoritative_v93": {
    "pferde_changed": [
      "pferde-template-kit.php",
      "assets/single-post-locked-v15083.css",
      "contract files V89->V94"
    ],
    "universal_changed": [
      "universal-portal-design-suite.php",
      "includes/class-upds-renderer.php",
      "assets/upds.css",
      "readme.txt",
      "contract V89->V94"
    ],
    "all_other_files": "byte-identical within each plugin tree"
  }
}
```

# ARTIFACT SHA256
```text
b47bdc8bf6b060ef009da72529a00d1e4083a718deb43183fcd7a5d4574a8d78  MASTER_PFERDE_ATELIER_V1_50_458_CONTRACT_V93_20260818.zip
50a8cc6e22b4fd30167d52efe7aaefe76eca96635517395c40a6713642fcfa0d  MASTER_ALLGEMEINGUELTIG_DESIGN_V2_2_29_CONTRACT_V93_20260818.zip
5879bb257026ec72fa83fc817994a4764009a7c1fde75a13fcec129eae45d0c3  PFERDE_ATELIER_HIVEPRESS_ANZEIGENSUCHE_v2.1.5_AJAX_ANZEIGENKATEGORIEN_INSTALLIEREN.zip
2764696cc9de7090f482546f209246beff71d6e9ec477082dbe40c06a0167914  UNIVERSAL_HIVEPRESS_ANZEIGENSUCHE_v2.1.5_AJAX_ANZEIGENKATEGORIEN_INSTALLIEREN.zip
132cc5207f57727def1e6bb8f0197b59d54e726bc626f2716b4da6f3620ae4ec  PFERDE_ATELIER_DESIGN_V1.50.459_CONTRACT_V94_TABELLEN_JOURNAL_KARTEN_INSTALLIEREN.zip
aff750403724734d356db47811fc3897a45d555942b6478f0a83fdfba7e10bb4  UNIVERSAL_PORTAL_DESIGN_SUITE_V2.2.30_CONTRACT_V94_TABELLEN_JOURNAL_KARTEN_INSTALLIEREN.zip
```

# AENDERUNG_V1_50_452_V83.txt
```text
PFERDE ATELIER V1.50.452 / VERTRAG V83
======================================
BASIS: letzter stabiler freigegebener Stand V1.50.446 / V77. Die nicht freigegebenen Breadcrumb-Abstandsversuche V78–V82 sind nicht enthalten.

TECHNISCHE ÄNDERUNGEN – AUSSCHLIESSLICH EINZELBEITRAGS-TABELLEN
1. Abstand nach Tabellenblock auf 28 px festgelegt.
2. Pferde-spezifisch: innere Tabellenlinien und Kopftrennlinie auf Dunkeloliv #35422A gesetzt.
3. Die globale helle Linienvariable --pa-single-line bleibt unverändert; dadurch ändern sich keine anderen Rahmen/Linien des Einzelbeitrags.

UNVERÄNDERT
Breadcrumbs, Startseite, Kategorien, Journal, Anzeigenmarkt, Suche, Affiliate, Bilder, Karten, Texte, Tabellenlayout, Spaltenbreiten, Zellpadding, Responsive-Logik und alle übrigen Einzelbeitragsabstände.
```

# AENDERUNG_V1_50_455_V86.txt
```text
V1.50.455 / V86 – JOURNAL-STARTSEITE TOP-ALIGNMENT
Basis: stabiler V1.50.452 / V83-Stand.
Änderung: ausschließlich `.pa433-journal-bottom-block` erhält `justify-content:flex-start!important`.
Zweck: beide Zwischenüberschriften des Journal-Startseiten-Bottomblocks bleiben auch nach nachgelagerten Layoutpässen an derselben oberen Kante.
V84/V85-Sonderversuche sind nicht enthalten.
Unverändert: Texte, Abstände, Farben, Journal-Kategoriearchive, Anzeigenmarkt, Suche, Tabellen-V83, Breadcrumbs und sonstige Portalbereiche.
Live-Sichtprüfung: nach Installation erforderlich.
```

# AENDERUNG_V1_50_456_V87.txt
```text
V1.50.456 / V87 – JOURNAL-STARTSEITE: STRUKTURELLER FIX GEGEN NACHLADENDES VERRUTSCHEN
Datum: 2026-08-12

Ursache nach Quellcodeprüfung:
- Die beiden Journal-Startseiten-Bottomzellen wurden als <article> gerendert.
- Die rechte Zelle ist dadurch ein "article + article"-Nachfolger und kann von nachgeladenen Theme-/Runtime-Regeln anders behandelt werden als die linke.
- V85 margin:0 und V86 justify-content griffen am Symptom an, beseitigten aber die strukturelle Angriffsfläche nicht.

Änderung:
- NUR auf Journal-Root werden die beiden .pa433-journal-bottom-block-Zellen als <div> statt <article> gerendert.
- Journal-Kategoriearchive bleiben unverändert bei <article>.
- Die wirkungslose V86-justify-content-Sonderregel wurde entfernt.

Nicht geändert:
- Texte, Abstände, Farben, Tabellenfix V83, Suche, Anzeigenmarkt, Journal-Kategoriearchive, übrige Seiten.

Status:
- PHP-Lint PASS
- Struktur-/Scope-Prüfung PASS
- ZIP-Test PASS
- Live-Sichtprüfung offen
```

# AENDERUNG_V1_50_457_V88.txt
```text
V1.50.457 / Contract V88
- Journalregister von 8 auf 9 explizite Kategorien erweitert: neu „Pferdewissen & Grundlagen“.
- Neue Kategorie wird exakt über Slug `pferdewissen-grundlagen` oder ersatzweise exakten Namen aufgelöst; keine unscharfe Aufnahme fremder Kategorien.
- Journal-Hub-Kategorieraster Desktop von 4 auf 3 Spalten umgestellt: bei 9 Kategorien 3×3. Tablet 2 Spalten, Mobil 1 Spalte unverändert.
- Eigener Bottomtext für „Pferdewissen & Grundlagen“ ergänzt: 338 Wörter, 3 Absätze, 2 Zwischenüberschriften, Links zu Wissen/Gesundheit/Training.
- V87-Fix für Journal-Root (neutrale DIV-Textzellen) unverändert erhalten.
- Sonstige Journaltexte, Anzeigenmarkt, Suche, Breadcrumbs, Tabellenfix V83 und Content-Hauptbereiche unverändert.
```

# AENDERUNG_V1_50_458_V89.txt
```text
V1.50.458 / CONTRACT V89 – JOURNAL-KATEGORIE-BREADCRUMB
Stand: 2026-08-12

AUSGANGSPUNKT
- Stabiler V88-Stand bleibt Basis.
- Neue Journal-Kategorie „Pferdewissen & Grundlagen“ war im Journal-Hub und Bottomtext bereits integriert.

KORREKTUR
1. Journal-Kategoriearchive erhalten den Breadcrumbpfad über die reale /journal/-Seite auch dann, wenn eine neu angelegte Kategorie noch nicht im Navigationsmenü steht.
2. Erkennung ausschließlich über das bestätigte Journal-Kategorieregister; keine Fremdkategorie wird aufgenommen.
3. Die bestehende Journal-Bild-/Breadcrumb-Achse gilt jetzt für alle tatsächlich aufgelösten Journal-Kategorien, nicht nur für acht fest eingetragene Term-IDs.
4. Abstand bleibt exakt wie bei den bereits freigegebenen Journal-Kategorien: 20 px Desktop/Tablet, 14 px mobil.

NICHT GEÄNDERT
- Journal-Hub 3×3, Bottomtexte, Bilder, Texte, Karten, Suche, Anzeigenmarkt, Einzelbeiträge, Tabellenfix V83 und V87-Neutralblock.
```

# MASTER-INTERNER FEHLER / ROOT CAUSE

PFERDE V93: `CURRENT_PLUGIN_SOURCE` ist nicht der V89-Stand des eingebetteten Installers. Vergleich: 492 Dateien je Baum; 488 byteidentisch; zwei Dateien geändert (`pferde-template-kit.php`, `assets/journal-bottom-editorial-v150433.json`); zwei Contract-Dateien nur unter V83 statt V89 vorhanden.

UNIVERSAL V93: `CURRENT_PLUGIN_SOURCE` ist ebenfalls nicht der V89-Stand des eingebetteten Installers. Vergleich: 15 Dateien je Baum; 11 byteidentisch; drei Produktionsdateien geändert (`universal-portal-design-suite.php`, `includes/class-upds-renderer.php`, `assets/upds.css`); Contract-Datei V83 statt V89.

Beide V93-Master selbst sind gegen ihr jeweiliges `MANIFEST_SHA256.txt` vollständig intakt: Pferde 687/687, Universal 215/215. Das Problem ist also kein Dateiverlust im Archiv, sondern eine falsche interne Kennzeichnung/Quelle: der Ordner `CURRENT_PLUGIN_SOURCE` ist älter als der eingebettete aktuelle Installer.

# VERBINDLICHE BUILD-REGEL AB JETZT

- Niemals wieder nur nach Ordnername `CURRENT_PLUGIN_SOURCE` bauen.
- Vor jedem Build: Version im Pluginheader, SHA-Manifest und eingebetteten Installer gegeneinander prüfen.
- Bei Abweichung: `BLOCKED`; keine ZIP erzeugen.
- Ausgangsbasis wird mit vollständigem SHA-256-Dateibaum in GitHub eingefroren.
- Nach Build muss jede nicht beabsichtigte Datei byteidentisch zum Baseline-Manifest sein.
- Master-Quelle und Master-Installer müssen denselben Produktionsbaum enthalten.
