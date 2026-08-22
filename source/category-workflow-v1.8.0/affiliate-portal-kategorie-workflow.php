<?php
/**
 * Plugin Name: Affiliate-Portal Kategorie-Workflow
 * Description: Allgemeingültiger SEO-/Affiliate-Kategorie-Workflow für Content, HivePress/Marketplace und Journal; 14-Stufen-Kern read-only, Post-FINAL-Deployment transaktional getrennt.
 * Version: 1.8.0
 * Author: OpenAI
 * License: GPL-2.0-or-later
 * Requires at least: 6.4
 * Requires PHP: 8.1
 */

if (!defined('ABSPATH')) { exit; }

define('APKW_VERSION', '1.8.0');
define('APKW_MASTER_CONTRACT_ID', 'ALLGEMEINGUELTIGER_KATEGORIE_MASTER_016_WORKFLOW_HARDLOCK');
define('APKW_DIR', plugin_dir_path(__FILE__));
define('APKW_CONTENT_WRITE_CAPABILITY', false);
define('APKW_RESEARCH_SCHEMA_VERSION', '1.4');
define('APKW_CATEGORY_SCHEMA_VERSION', '1.4');

require_once APKW_DIR . 'includes/class-apkw-settings.php';
require_once APKW_DIR . 'includes/class-apkw-dataforseo.php';
require_once APKW_DIR . 'includes/class-apkw-inventory.php';
require_once APKW_DIR . 'includes/class-apkw-validator.php';
require_once APKW_DIR . 'includes/class-apkw-research.php';
require_once APKW_DIR . 'includes/class-apkw-coverage-ledger.php';
require_once APKW_DIR . 'includes/class-apkw-r9-lifecycle.php';
require_once APKW_DIR . 'includes/class-apkw-lifecycle-store.php';
require_once APKW_DIR . 'includes/class-apkw-delta-planner.php';
require_once APKW_DIR . 'includes/class-apkw-deployment-writer.php';
require_once APKW_DIR . 'includes/class-apkw-research-evidence.php';
require_once APKW_DIR . 'includes/class-apkw-comparator.php';
require_once APKW_DIR . 'includes/class-apkw-admin.php';

APKW_Admin::init();
