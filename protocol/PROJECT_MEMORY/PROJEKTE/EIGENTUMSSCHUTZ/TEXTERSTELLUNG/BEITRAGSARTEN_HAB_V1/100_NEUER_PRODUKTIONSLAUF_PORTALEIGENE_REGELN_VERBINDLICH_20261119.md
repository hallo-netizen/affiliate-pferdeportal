# Neuer Produktionslauf – verbindlich getrennte Portal-/Beitragsregeln
**19.11.2026 – Nutzerkorrektur und Zielvertrag. Keine technische Umsetzung oder Regeländerung in diesem Protokoll.**

## Verbindliche Nutzerkorrektur
Der neue Produktionslauf wird entwickelt. **Nicht den alten Produktionslauf umbauen, von dessen Regeln abhängig machen oder an dessen globale Prüfungen binden.** Die **eigenen, vollständigen Beitragsregeln jedes Portals** sind für den jeweiligen Artikel verbindlich. Die früher kopierten Pferdeatelier-Regeln sind nur genehmigtes Ausgangsmaterial, keine spätere technische Autorität über andere Portale.

## Ein einziger Produktionsweg
1. Die bestehende Import-/Auftragsdatei lässt das Portal eindeutig erkennen (bei Unklarheit keine Ersatzzuteilung).
2. Die vorher einmalig festgelegte Beitragsart wird übernommen, nicht erneut entschieden.
3. Der neue Produktionslauf lädt **genau ein** versioniertes, eigenständiges Regelbuch für die Kombination `Portal + Beitragsart`. Fehlendes Regelbuch -> sauber sperren; niemals Regelbuch eines anderen Portals verwenden.
4. Nur die Regeln dieses gewählten Pakets sind für diesen Text fachlich verbindlich; gemeinsame Schreib- und Prüfwerkzeuge dürfen sie technisch ausführen, aber keine fachlichen Alt- oder Fremdregeln hinzufügen oder überstimmen.
5. Recherche, Schreiben, einmalige komplette Qualitätsprüfung und Ausgabe des für das ausgewählte Portal passenden Importformats; keine zweite Typ- oder Inhaltsentscheidung.
6. Für jede Änderung zuerst ausdrückliche Freigabe einholen. Allgemeine Verbesserungen nach Freigabe bewusst in jedes betroffene eigenständige Regelbuch übernehmen; portalbezogene Änderungen nur im betreffenden Portal.

## Hab & Bewahr: bestätigter Zusatz für staatliche Links
- Ein externer Verweis **darf** nur gesetzt werden, wenn er dem Leser zu genau diesem Thema einen echten Zusatznutzen bietet; **keine Pflicht, keine Mindestzahl, kein Ausgleich durch Fülllinks**.
- Bevorzugter Ort am Textende: „Weiterführende amtliche Informationen“/Fußnote; **nur wenn dort wirklich ein sinnvoller Verweis steht**.
- Ausschließlich vorher geprüfte **staatliche** Websites. Startseite oder Hauptkategorie genügt; keine Versicherungsseiten, Unternehmen, Verbände, Shops oder private Seiten.
- **Jeder externe Verweis zwingend `rel="nofollow"`.**
- Amtlicher Weiterführungslink ersetzt keinen tatsächlichen Faktenbeleg, wo eine konkrete Aussage belegt werden muss.
- Interne Verweise und externe Informationsverweise werden im neuen Produktionslauf getrennt nach dem **jeweiligen Hab-Regelbuch** behandelt; keine fremde globale Linkentscheidung übernimmt die Kontrolle.
- Bestehende Verweise/Pflichtzahlen in den bereits kopierten Hab-Regelbüchern bleiben bis zu ausdrücklich genehmigten Änderungen bestehen. Technische Unterstützung für optionale Behördenlinks ist noch nicht nachgewiesen, nicht als aktiviert melden.

## Heutiger Ist-Zustand / technische Schranke
Die fünf Hab-Regelbücher sind auf GitHub fachlich eigenständig abgelegt, aber noch **nicht** an einen end-to-end getesteten neuen Produktionslauf gebunden. Die derzeit archivierte Offline-Entwicklungsbindung des Multiportal-Projekts meldet `hab_und_bewahr: NO_VALUES_BLOCKED`, `production_enabled: false`; der volle Text-Writer-Test fehlt. Diese Fakten sind kein Grund, wieder den alten Produktionslauf zum Änderungsziel zu machen.

## Nächster technischer Schritt
**Ausschließlich im neuen Produktionslauf:** exakte Portal-/Typ-Auflösung -> eines von fünf Hab-Regelbüchern -> vollständige Anwendung der eigenen fachlichen Regeln -> zulässiger optionaler staatlicher Fußnotenlink mit `nofollow` -> negative Tests für falsches Portal, unbekannten Typ, fremde Behördenseite, ohne `nofollow` und künstlich erzwungenen Link. Auch einen normalen Artikel **ohne** externen Link als PASS beweisen. Vorher keine produktive Freigabe.

**Schutz:** Kein Programmcode oder vorhandenes Textregelpaket mit diesem Protokoll verändert. Dies ist eine Dokumentation des vom Nutzer verbindlich vorgegebenen Produktionsmodells.
