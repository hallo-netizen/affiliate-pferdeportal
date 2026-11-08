# HD-006 – HOBBY DEPOT BILDZENTRALE – CURRENT

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

**Datum:** 08.11.2026
**Aktuelle vollständige, lokal geprüfte Version:** **2.8.10**.
**Live-WordPress-Abnahme:** offen.
**Pferdeatelier / K0 / andere Portale:** unverändert.

## Verbindliche Bezeichnungen und Wege

| Menüname | Gehört zu | Admin-Adresse |
|---|---|---|
| **Bildzentrale** | HD-006 Bilderzeugung (dieses Plugin) | `/wp-admin/admin.php?page=hdbz-bilder-erstellen` |
| **Bilder zuordnen** | Eigenständige vorhandene Bildzuordnung | `/wp-admin/admin.php?page=hobby-depot-bildzentrale` |

Zwei verschiedene Click-URLs und Callbacks. Das zweite Plugin darf nur im sichtbaren Menü umbenannt werden, niemals umgeleitet oder verändert. REST/Webhook-Pfade bleiben unverändert.

## Verbindliche Hobbyregister-Bedienung

Ein Hobby öffnen → Bewertung aus **Noch nicht geprüft / Bild passt / Bild passt nicht** → optionaler Motivwunsch → einmal **Bild erstellen** klicken: derselbe Klick startet **sofort** den Anbieterauftrag (nach ausdrücklicher Kostenbestätigung). **Keine Warteschlange und kein zweiter Startknopf**.
Jedes Foto und jeder vorhandene Master darf erneut bearbeitet werden.
Der noch nicht veröffentlichte Entwurf wird als lokales WordPress-Mediathekbild angezeigt. Erst ausdrücklich **Bild übernehmen** ersetzt die bisherige Frontend-Zuordnung. Verwerfen und Fehler dürfen den alten Master nicht zerstören. Fehler beim Download eines bereits bezahlten Entwurfs müssen ohne neuen kostenpflichtigen Start wiederholbar sein.

## Vollständige Software und Prüfnachweise

- **ZIP:** `HOBBY_DEPOT_BILDZENTRALE_2.8.10_EINFACHE_BEDIENUNG.zip`
- **ZIP-Größe:** 83.745 Bytes.
- **SHA256:** `09c5fbfd113c1e0fa0d6552c473b5ef5d1b0f1150adddce10090291ce097227f`
- **Dauerhafte Voll-ZIP und alle Nachweise:** persönliche Library unter `/Hobby Depot/Plugin-Büro/`. Alle drei Dateien dort erfolgreich hochgeladen: ZIP, Prüfprotokoll, Testnachweise. Die ZIP ist **noch nicht** als Datei im GitHub-Repository gespeichert.
- **Tests:** 65/65 Backend, 27/27 Menü, 21/21 Browser, PHP 2/2, ZIP-integrität PASS. Originale werden nicht automatisch ersetzt.
- **Wichtig:** WordPress-/Provider-Simulation und echte Browserklicks an einer lokalen Oberfläche; kein bezahlter Live-Provideraufruf, kein WordPress-Live-PASS.

## Pflichtquellen und Regression

- [Aktueller Bedien-, Menü- und Bildschutz-Vertrag 2.8.10](./BILDZENTRALE_VERTRAG_2.8.10_20261108.md)
- [Historische Akte vor 2.8.10 – nur Archiv](./ARCHIV_STAND_VOR_2.8.10_20261108.md)
- [Historischer 2.8.8-Menüvertrag – ausdrücklich überholt](./MENUE_VERTRAG_20261108.md)
- [Historischer 2.8.9-Bildbewertungsvertrag – durch 2.8.10 abgelöst](./BILDBEWERTUNG_VERTRAG_2.8.9_20261108.md)

Vor jeder Freigabe: aktuelle ZIP und SHA verifizieren, beide Menüs und ihre **unterschiedlichen** Klickwege, direkte Bild-Erstellung, drei Bewertungen, erneutes Bearbeiten bestehender Master, Entwurfsvorschau und ausdrückliche Übernahme anhand des Testsatzes prüfen. Keine bloßen Versions- oder Titelfixes.

## Nächste Aktion

**Ein echter WordPress-End-to-End-Test nach Installation von 2.8.10:** Beim Hobbyregister ein Hobby öffnen, Bild erstellen, das neue Bild als Entwurf sehen, ausdrücklich übernehmen und im Frontend kontrollieren. Die bisherige Bilddatei muss bis zur Übernahme erhalten bleiben. Wenn der Live-Test scheitert: echten Fehlerpfad protokollieren und die Ursache im vorhandenen Plugin beseitigen. Keine weitere ZIP ohne erneute Regression.

**Nicht bearbeiten:** Kacheldesign „Drachen & Leinen“ – die Designänderung ist vom Nutzer ausdrücklich gestoppt.
