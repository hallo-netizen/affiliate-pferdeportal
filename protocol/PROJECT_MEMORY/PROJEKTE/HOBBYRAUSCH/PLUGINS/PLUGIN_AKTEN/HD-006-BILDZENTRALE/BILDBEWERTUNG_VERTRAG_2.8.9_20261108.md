# HD-006 – Verbindlicher Hobbyregister-Bewertungsvertrag 2.8.9 (08.11.2026)

## Zwingende Redaktionslogik
Jedes Bild ist jederzeit bearbeitbar, einschließlich jedes bereits veröffentlichten Masterbilds.

**Exakt drei menschliche Zustände:**
- **Noch nicht geprüft** (Standard, solange dieses konkrete Bild nicht bewusst bewertet wurde).
- **Bild passt** (vom Anwender positiv bewertet).
- **Bild passt nicht** (vom Anwender negativ bewertet).

„Bild vorhanden / Kein Bild“ ist ausschließlich eine Aussage über die Existenz einer Bildzuordnung, nicht über deren Qualität.
Technische Vermerke wie `FINAL_MASTER_VERIFIED`, `DONE`, „Masterbild fertig“ dürfen niemals Bewertungen ersetzen oder das Bearbeiten verhindern.

## Sicherheits- und Klickvertrag
Jedes Hobby – auch alle bisherigen Master – bietet **Prüfen / bearbeiten** und **Neues Bild erstellen**.
Bei vorhandenem Foto wird eine Neubearbeitung explizit bestätigt. Altes Foto bleibt bis zur separat bestätigten Übernahme des Entwurfs unverändert; eine Übernahme kann zurückgenommen werden.
Bewertungen sind an die genaue Bildidentität gebunden und dürfen bei Bildwechsel nicht weitergelten.
Für fehlendes Foto ist „Bild passt“ gesperrt; Bilderzeugung dagegen möglich.
Keine automatische Massenbilderzeugung, höchstens zehn vorgemerkte Hobbys.

## Verbindlicher Admin-Menüvertrag
Das ORIGINAL-Plugin für bestehende Bildzuordnungen heißt weiterhin **Bildzentrale** und bleibt unter `admin.php?page=hobby-depot-bildzentrale`.
Die HD-006-Bilderzeugung heißt **Bilder erstellen** und bleibt unter `admin.php?page=hdbz-bilder-erstellen`.
Zwei getrennte Slugs, zwei Click-URLs, zwei unterschiedliche Funktionen. NIE das fremde Bildzentrale-Menü umbenennen. REST und Webhook unverändert.

## Vollständiger lokal geprüfter Kandidat
`HOBBY_DEPOT_BILDZENTRALE_2.8.9_BILDBEWERTUNG_ALLE_BEARBEITBAR.zip`
SHA-256 `e2e8128cd02c3772ddcf3ade85238cdb85753356f445c07483a5319e2e149253`
82.750 Bytes; vollständiges Plugin, zwei PHP-Dateien. ZIP PASS, PHP-Lint PASS.
Reale 862 Hobby-Zeilen simuliert: 48/48 Backendchecks, 27/27 Menüchecks und 16/16 Chromium-Klicktests PASS.
**WordPress-Live-PASS und vollständige GitHub-ZIP-Ablage noch offen.** ZIP derzeit als Chat-Artefakt verfügbar.

## Anti-Regression vor jedem neuen Update
Alle drei Bewertungen für jedes bestehende Bild testen; Erneuerung aller Master testen; Erhalt des Vorgängers bis Übernahme testen; Rücknahme testen; Bildidentitätswechsel testen; beide Admin-Menüs plus zwei Klickziele prüfen; Voll-ZIP, PHP-Syntax, Browser und Negativtests prüfen. Bei Ausfall keine Freigabe.

Separate Baustelle: Kachelfoto-Format „Drachen & Leinen“ im HD-003-Design-Plugin. Wird mit dieser Bildzentrale-Version **nicht** verändert.
