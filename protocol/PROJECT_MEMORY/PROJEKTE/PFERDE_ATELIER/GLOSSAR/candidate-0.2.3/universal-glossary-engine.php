<?php
/**
 * Plugin Name: Universal Glossary Engine
 * Description: Configurable glossary backend/frontend for WordPress portals.
 * Version: 0.2.3
 * Requires at least: 6.4
 * Requires PHP: 8.1
 * Author: OpenAI
 * License: GPL-2.0-or-later
 */

if (!defined('ABSPATH')) { exit; }

define('UGE_VERSION', '0.2.3');
define('UGE_FILE', __FILE__);
define('UGE_DIR', plugin_dir_path(__FILE__));

require_once UGE_DIR . 'includes/class-uge-config.php';
require_once UGE_DIR . 'includes/class-uge-core.php';
require_once UGE_DIR . 'includes/class-uge-admin.php';
require_once UGE_DIR . 'includes/class-uge-frontend.php';
require_once UGE_DIR . 'includes/class-uge-seo.php';
require_once UGE_DIR . 'includes/class-uge-transfer.php';
require_once UGE_DIR . 'includes/class-uge-policy.php';

register_activation_hook(__FILE__, ['UGE_Core', 'activate']);
register_deactivation_hook(__FILE__, ['UGE_Core', 'deactivate']);

add_action('plugins_loaded', static function () {
    UGE_Core::init();
    UGE_Admin::init();
    UGE_Frontend::init();
    UGE_SEO::init();
    UGE_Transfer::init();
    UGE_Policy::init();
});
