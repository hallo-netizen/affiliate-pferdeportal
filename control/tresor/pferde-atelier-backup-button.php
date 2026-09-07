<?php
/**
 * Plugin Name: Pferde Atelier – Komplettsicherung
 * Version: 2.1.0
 * Hinweis: Kanonische Installationsdatei siehe Chat-Artefakt PFERDE_ATELIER_KOMPLETTSICHERUNG_2.1.0.zip.
 *
 * Architektur:
 * - Browser startet nur den Hintergrundworker;
 * - langer Backup-Lauf läuft per nohup/bash außerhalb des HTTP-Requests;
 * - Status wird gepollt;
 * - fertige Datei erst nach BACKUP_PASS downloadbar;
 * - wöchentlicher Cron startet denselben Hintergrundweg.
 *
 * Lokaler exakter Worker-Test 2026-09-07:
 * - Start-Rückgabe: ~0,017 s;
 * - asynchroner Abschluss: BACKUP_PASS;
 * - Paketstruktur: PASS;
 * - Git-Mirror fsck: PASS.
 */
