# NOTFALL-TRESOR – WIEDERAUFBAU

STAND: 2026-09-07
STATUS: KISS

Nur einen Stand mit \`BACKUP_PASS\` verwenden.

## WIEDERAUFBAU

1. **GitHub**
   - Git-Mirror zurückspielen;
   - Branches/Tags prüfen;
   - notwendige GitHub-Einstellungen anhand des Metadatenexports wiederherstellen.

2. **WordPress**
   - vorhandene WordPress-Vollsicherung wiederherstellen;
   - Datenbank + Dateien prüfen.

3. **Projektarchiv**
   - nur Dateien ergänzen, die nicht bereits durch GitHub/WordPress wiederhergestellt wurden.

4. **Prüfen**
   - Manifest/Hashes;
   - Campus-Einstieg;
   - WordPress erreichbar;
   - benötigte Projektdateien vorhanden.

Ergebnis:

\`RESTORE_PASS\`

oder

\`RESTORE_FAIL:<GRUND>\`

## HARTE REGEL

Backup/Archiv niemals als Arbeitsquelle benutzen.
Nach Wiederherstellung wieder normal über den Campus arbeiten.
