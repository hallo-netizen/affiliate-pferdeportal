# PFERDERASSEN – DATENABLAGE

STAND: 2026-09-12

## 1-KLICK-ÜBERSICHT

**WAS IST DAS?**  
Die zentrale Ablage der einzelnen quellengebundenen Rassendatensätze.

**HIER BIST DU RICHTIG, WENN …**  
du einen konkreten Rassendatensatz lesen, anlegen oder nach bestätigter Recherche ergänzen willst.

**DU DARFST …**  
pro Rasse genau einen strukturierten Datensatz nach `../RASSEN_DATENMODELL.md` pflegen.

**DU DARFST NICHT …**  
Synonyme als neue Rassen duplizieren, freie unstrukturierte Parallelakten anlegen, Quellen weglassen oder Felder durch Vermutung füllen.

**ALS NÄCHSTES …**  
`../RASSEN_DATENMODELL.md` und `../RASSEN_REGISTER.md` lesen; danach den konkreten Datensatz bearbeiten.

## ABLAGEREGEL

- ein Datensatz pro Rasse;
- empfohlene Form: JSON;
- stabile interne ID;
- `schema_version` im Datensatz;
- Quellen/Faktzuordnung müssen erhalten bleiben;
- Pony/Kleinpferd/Pferd ist Klassifikation, kein eigener Datenraum.

## ERWEITERUNG

Neue allgemein sinnvolle Felder werden zuerst zentral in `../RASSEN_DATENMODELL.md` definiert. Alt-Datensätze werden kontrolliert nachgezogen und bis dahin als `nicht_recherchiert` behandelt.
