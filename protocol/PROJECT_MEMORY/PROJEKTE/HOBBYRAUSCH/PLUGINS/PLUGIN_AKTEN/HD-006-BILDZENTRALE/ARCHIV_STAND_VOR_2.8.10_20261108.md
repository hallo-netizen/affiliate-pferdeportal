# Historische HD006-Stände (nicht mehr CURRENT)

Diese Datei ist die unveränderte frühere CURRENT-Akte; nur zur Recherche, nie als Installations- oder Menüvertrag verwenden.

---

# AKTUALISIERUNG 08.11.2026 – 2.8.10 IST AKTUELLE INSTALLATIONSFASSUNG

**Pflichtdokument:** [BILDZENTRALE_VERTRAG_2.8.10_20261108.md](./BILDZENTRALE_VERTRAG_2.8.10_20261108.md). Die Menünamen aus dem älteren 2.8.8-Menüvertrag sind ÜBERHOLT: Das HD-006-Erstellungsplugin heißt **Bildzentrale**, das andere Zuordnungsplugin heißt **Bilder zuordnen**. Vollständige 2.8.10-ZIP, Prüflog und Testnachweise in der persönlichen Library unter `/Hobby Depot/Plugin-Büro/`. 65 Backend-, 27 Menü- und 21 Browsertests PASS; WordPress-Live offen. Die folgenden älteren Versionsangaben sind historisch, nicht Current.

---

# HD-006 – HOBBY DEPOT BILDZENTRALE – CURRENT

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-11-08
STATUS: **HD-006 2.8.8 MENÜTRENNUNG LOKAL PASS / WORDPRESS-LIVEPRÜFUNG OFFEN. Die unten dokumentierte 2.7.8 ist historisch (Inventar 01.11.), keine aktuelle Installationsfreigabe.**

Plugin-ID:
`HD-006-BILDZENTRALE`

## AKTUELLE PFLICHTREGEL: MENÜTRENNUNG 2.8.8 (08.11.2026)

**Vor jedem HD-006-Update zwingend lesen:** [MENUE_VERTRAG_20261108.md](./MENUE_VERTRAG_20261108.md) und die dort abgelegte reproduzierbare [Patch-Datei](./REPRODUKTION_2.8.8_MENU_FIX.py) sowie [Regressionstests](./MENU_REGRESSION_2.8.8.php).

**Fehlerursache:** Zwei verschiedene WordPress-Bildverwaltungen haben dieselbe Admin-Menüadresse verwendet. Eine reine Titelkorrektur ist verboten.

- **Bilder erstellen** (HD-006) → `/wp-admin/admin.php?page=hdbz-bilder-erstellen`.
- **Bilder zuordnen** (bestehende Zuordnung) → `/wp-admin/admin.php?page=hobby-depot-bildzentrale`.
- Beide Klickpfade müssen real verschieden sein; bestehende Zuordnung und API/Webhooks bleiben unverändert.

**Neu erstellter Installationskandidat:** `HOBBY_DEPOT_BILDZENTRALE_2.8.8_GETRENNTE_MENUES_UND_KLICKPFADE.zip` (SHA-256 `dd076c7772c820adcceabea85897a6bcfe79a47dd66430475b988d413541787a`). Lokal 27/27 Menüszenarien bestanden; Hobbyregister-Datei unverändert. ZIP aus Chatlieferung, kein eigener Download im GitHub-Pluginbüro bestätigt; ein WordPress-Livetest ist offen. **Nicht** zu alten 2.7.x-Installationskandidaten zurückkehren.

## Verifizierte Quelle

WPvivid-Pluginbackup:
`pferde-atelier.de_wpvivid-6e9ec6d805997_2026-09-24-11-08_backup_plugin.part001.zip`

Originaldatei:
`plugins/pferde-atelier-bildzentrale/pferde-atelier-bildzentrale.php`

Beweis:
- Version 2.7.6;
- 383603 Bytes;
- SHA-256 `984a8d4da6594ffa93e6d4024b57cc6c22c7d1fbfec398177a19b0490c20d89b`;
- exakte Übereinstimmung mit dokumentiertem Pferdeatelier-Source-Scan.

## Historischer Kandidat vom 20.10.2026 (nicht zur Neuinstallation)

`HOBBY_DEPOT_BILDZENTRALE_2.7.8_VERBINDLICHER_BILDPROMPT_INSTALLIEREN.zip`

ZIP SHA-256:
`d9d8caad4c2f4057fee30f9d21607376fa110d82defed8c0f759e5c202b83342`

Hauptdatei:
- 320401 Bytes;
- SHA-256 `edda98383add25fc2d02bf35bfff433b2c5ded332cc21a0fc43a82577e6004ec`.

## Korrektur

Der frühere Kandidat 1.0.0 war **nicht** aus dem echten Pluginquellstand abgeleitet und ist verworfen. Seine Library-Kopien im Bildbüro und Plugin-Büro wurden entfernt.

## Delta

Entfernt:
- pa_breed;
- kompletter Rassen-Batch;
- Rassen-Hero-Sonderprompt;
- Pferde-Motivcluster und Pferde-Such-/Alttext-/Fallbackregeln;
- feste ID 9120;
- Pferdeatelier-Admin-/REST-Slugs.

Angepasst:
- Hobby-Depot-Name/Slug;
- HDBZ-Namespace;
- neutraler Hobby-Prompt;
- acht Hobbywelten;
- Hobby-Depot-WordPress-/HivePress-Bildbindung.

Beibehalten:
- allgemeiner Originalkern; nach Namespace-Normalisierung 134 Funktionen unverändert.

## Bildprompt 2.7.8

- verbindlicher Hobby-Depot-Grundprompt;
- ruhige, nicht überladene Motive;
- Tätigkeit bevorzugt;
- Hände/Arme/handelnde Personen zur Verdeutlichung;
- Menschen nicht dekorativ;
- automatische Beitragsableitung aus Titel + Kurztext + bis zu 120 Wörtern Inhalt;
- Grundregel auch für Kategorie-, Hero- und HivePress-Prompts.

## QA

- PHP PASS;
- ZIP PASS;
- WordPress-Paketstruktur PASS;
- 0 fehlende Callbacks;
- 0 fehlende self-calls;
- 0 Pferde-/Rassen-/Horse-/Breed-/pa_breed-Literale;
- allgemeine Kernwege gegen Original unverändert PASS;
- lokaler Prompt-Positivtest 2874/3000 Zeichen PASS;
- 2.7.7 → 2.7.8 Funktionsdelta nur Prompt-/Themenableitung + Versionswert.

## Bildertrommel

Im verifizierten Original ist kein eindeutiger Code-/UI-Block dieses Namens belegbar. Daher wurde kein allgemeiner Weg auf Verdacht gelöscht.

## WordPress-Inventarabgleich 01.11.2026

Die vom Betreiber gelieferte vollständige WordPress-Pluginliste zeigt **Version 2.7.8 als aktiv**. Der zuvor dokumentierte Entwicklungs-/Teststand 2.7.8 ist versionsgleich, aber nicht dadurch funktional live-geprüft. Ein unabhängiger Server-Quellcode-/ZIP-Readback und ein Live-Funktionstest wurden in diesem Abgleich nicht ausgeführt. Keine Plugininstallation oder Campus-CURRENT.zip-Synchronisierung. Beleg: `../../EVIDENCE_WP_PLUGINLISTE_20261101.md`; operative WordPress-Current: `../../../WORDPRESS_TECHNIK/CURRENT_STATE.md`.

## EXAKT EINE NEXT ACTION (08.11.2026)

**Bei installiertem 2.8.8 im WordPress-Backend die getrennten Menüs „Bilder erstellen“ und „Bilder zuordnen“ mit ihren zwei verschiedenen URLs kontrollieren. Danach das geprüfte 2.8.8-Plugin-ZIP dauerhaft im Pluginbüro hinterlegen.**
