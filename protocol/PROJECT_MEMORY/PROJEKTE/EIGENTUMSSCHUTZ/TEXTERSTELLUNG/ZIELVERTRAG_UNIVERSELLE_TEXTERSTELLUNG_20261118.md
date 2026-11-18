# Zielvertrag – universelle Texterstellung (18.11.2026)

**Entscheidung:** Statt eigener Pferdeatelier-Ableger eine gepflegte, portalneutrale Plugin-Codebasis. Daraus zwei Paketvarianten erzeugen: (A) Hab & Bewahr mit gebundener Portal-Konfiguration und (B) neutrale Erstinstallation mit Einrichtungsassistent. Kein doppelter Quellcode, keine eigenen neuen Inhaltsentscheider.

## Verbindliche Regeln
1. Gemeinsamer Ablauf: vorhandene einmalige Keywordrecherche/DataForSEO -> genau eine Redaktion/Kategorie/Artikelart-Entscheidung -> Titel -> bestehender K0-Fünffelderexport -> nur WordPress-Entwürfe. Keine parallele Themenprüfung, keine neue Prüfstation nach K0.
2. Portaldaten gehören in eine eigenständige Konfiguration (Name, WordPress-Site, bestehender Leseweg zum aktuellen Kategorienbaum, optional Design-/Fachprofil). Keine Pferde-, Hab-, Hobby-, Roboter- oder Wasser-Kategorien im universellen Kern.
3. Vorhandene WordPress-Kategorien/Seiten und ihre Beziehungsdaten in *einem* lesenden Adapter verwenden. Kein neu erfundener Kategorienmaster. Strukturtypen nicht blind gleichsetzen: Hab = R1/R2/R3 Seiten -> flache category -> Beitrag; bei anderen Portalen tatsächlich aktive Struktur prüfen. Aktualisierungen müssen ohne Codeänderung sichtbar sein.
4. Artikelart separat aus dem einmaligen Redaktionsentscheid beziehen, nie aus Präfixen im Kategorienamen ableiten. Artikel-ID und signierter K0-Planplatz bleiben vom zuständigen Originalvertrag kontrolliert; keine Erzeugung eigener Ersatz-IDs.
5. Bisherige PSTE/PSERC-Interne Kennungen können in einem gekapselten Alt-Kompatibilitätsbaustein weiterexistieren, solange der Originalvertrag es erfordert. Dieser Baustein ist keine Pferde-Fachregel und darf nicht ohne Ersatz entfernt werden.
6. Pro Installation eigener WordPress-Datenspeicher, Recherche-Status, Aufträge, Credentials und Diagnose. Keine Übernahme von Pferdeartikelbeständen. Keine kostenpflichtige DataForSEO-Abfrage ohne ausdrückliche Bedienfreigabe.
7. Leere Erstinstallation ist sicher: freundliche Schritt-für-Schritt-Einrichtung mit automatischer Erkennung von Site und verfügbarem Kategorien-Leseweg, Fehlanzeige für fehlende K0-Zuständigkeit. Ohne eindeutige Portalbindung kein K0-Export/Rückimport. Keine stillen Platzhalter für fehlende Zuordnungen.
8. Vollständige Portalfreigabe braucht getestete K0-Portalregistrierung/Regelgleichheit und K0-Rückgabeformat. Aus dem historischen K0-Multiportal-Register dürfen für Hab/Robotik/Wasser keine Freigaben gefolgert werden.
9. Freigabe nur nach echten Portaltests: Pluginaktivierung, Kategorien-Readback, Recherche ohne unerlaubte Kosten, einmalige Themenzuordnung, K0-5-Feld-Auftrag, verifizierte Rückgabe, Entwurfsimport und Diagnosen; keine automatische Veröffentlichung.
10. Versionierung: dieselbe Kernversion für Hab-gebundenes und neutrales ZIP; beide aus einer Quelle gebaut und getrennt geprüft. Keine neuen Plugins für kleine Zwischenschritte.

## Gebündelter Arbeitslauf
- Bestehende 0.4.24- und QA-Quellen vergleichen; echte Pferde-Fachentscheidungen auslagern/deaktivieren; Altprotokolle nur als gekennzeichnete Kompatibilität erhalten.
- Ein lesender Kategorien-Adapter und ein echter einzelner Redaktionseingang, der `category` und `article_type` getrennt bestätigt.
- KISS-Einrichtung und isolierte Site-Konfiguration; Hab-Variante und generisches Blanko-Paket aus derselben Quelle erzeugen.
- Prüfung der bestehenden K0-Runtime/Portalregistrierung **ohne** sie im Rahmen dieser Vorbereitung zu verändern; unregistrierte Portale bleiben für K0 gesperrt.
- Hab-Tests, anschließend neutraler Robotik/Wasser-Probestart. Erst nach bestandenem Realimport Installationsfreigabe.

**Aktueller Status:** Zielvertrag dokumentiert; Implementierung und reale WordPress/K0-Abnahme stehen aus. Das bisherige Hab-0.4.24 und QA-ZIP ausdrücklich nicht zur Installation freigegeben.