# HD-006 – verbindlicher Menüvertrag | 08.11.2026

**Problemursache, nicht noch einmal nur Titel umbenennen!**

Im WordPress-Backend gab es zwei Einträge „Bildzentrale“, beide mit dem gleichen Klickpfad. Im Screenshot vom 08.11.2026 führt `admin.php?page=hobby-depot-bildzentrale` zur Bildzuordnung („119 Bildmaster“). Der echte Quellcode von Bilderstellungs-Plugin HD-006 **2.8.7** registrierte aber denselben Admin-Menü-Slug für eine andere Oberfläche. Auch sechs interne Weiterleitungen verwendeten ihn. Das ist die nachgewiesene Kollision.

## Dauerhafte Trennung: zwei Namen, zwei URLs, zwei Funktionen

| Menüname | URL im Backend | Funktion |
|---|---|---|
| **Bilder erstellen** | `/wp-admin/admin.php?page=hdbz-bilder-erstellen` | HD-006: Bildgenerierung für Beiträge, Kategorien, HivePress und Hobbyregister |
| **Bilder zuordnen** | `/wp-admin/admin.php?page=hobby-depot-bildzentrale` | vorhandenes anderes Plugin: Hobby-/Kategorie-Bilder zuordnen |

Die Bildzuordnung behält unbedingt ihre URL und ihren Callback. HD-006 darf `hobby-depot-bildzentrale` **nie wieder als Admin-Menü-Slug** verwenden. Eine reine Menütextänderung ohne geänderte Klickpfade ist als Fix **verboten**.

Die Softwarekorrektur 2.8.8 ändert bei der Bildzuordnung nur den sichtbaren Menütext von „Bildzentrale“ in „Bilder zuordnen“, und nur falls dieser Titel tatsächlich so lautet. Fremder Menü-Slug, Callback, Berechtigung und Menüposition bleiben unverändert. Bereits eindeutig benannte andere Menüpunkte bleiben unberührt.

## Abgrenzung / Bestandsschutz

- REST/Webhook unter `hobby-depot-bildzentrale/v1` **muss unverändert bleiben**; das ist kein Admin-Menü.
- WordPress-Bilder, Hobbyregister, Kategoriezuordnungen, Medien, Design-Plugin, Frontend, API-Logik unverändert.
- Nur Hauptdatei von HD-006 geändert, Hobbyregister-Unterdatei byteidentisch.
- 2.8.8 ist ein lokal geprüfter **Installationskandidat**, kein behaupteter WordPress-Live-PASS.

## Beweise

Original 2.8.7 ZIP SHA256: `9ea589793bce56cf6407d3845086572678099a0bbfe3215098c9b116fae1df5d`.

Korrigierte 2.8.8 ZIP SHA256: `dd076c7772c820adcceabea85897a6bcfe79a47dd66430475b988d413541787a`.

**27 von 27** Simulationen der real geladenen PHP-Klasse bestanden: Menü in beiden Registrierungsreihenfolgen, zwei verschiedene Slugs, zwei verschiedene Beschriftungen, korrekte Callbacks und Click-URLs, keine Zuordnung vorhanden, drittes unbekanntes Menü, wiederholter Aufruf, schon umbenanntes Fremdmenü, interne Links, unveränderte REST-Routen. Beide PHP-Dateien mit Syntaxprüfung bestanden. Installierbares ZIP und vollständiges Prüfprotokoll in der zugehörigen Chatlieferung vom 08.11.2026.

## PFLICHTPRÜFUNG vor jeder neuen HD-006-Version

1. Getrennte Admin-Slugs **und** getrennte Beschriftungen nachweisen, nicht nur behaupten.
2. Beide Menüeinträge und tatsächliche Klickziele mit beiden Registrierungsreihenfolgen simulieren.
3. Alle internen Ersteller-Weiterleitungen führen zu `hdbz-bilder-erstellen`.
4. Fremde Zuordnung unter `hobby-depot-bildzentrale` vollständig erreichbar halten.
5. REST/Webhook, bestehende Bilder, Daten und Hobbyregister unverändert.
6. Bei Fehler: **keine Plugin-Freigabe**.

**Wiederholungsfehler ausgeschlossen durch Vertrag + Regressionstest.**