from pathlib import Path
p=Path("/tmp/candidate134/affiliate-portal-router/pferdeportal-affiliate-router.php")
s=p.read_text()
s=s.replace("Version: 6.72.132","Version: 6.72.134",1)
s=s.replace("const VERSION = '6.72.132';","const VERSION = '6.72.134';",1)
needle="""        $state = $this->aff043_state();
        $status = sanitize_key((string)($state['status'] ?? 'not_started'));
"""
insert="""        $idealo_restore = get_option(self::OPTION_NETWORK_IDEALO, array());
        $idealo_restore = is_array($idealo_restore) ? $idealo_restore : array();
        $idealo_mode_restore = $this->idealo_sanitize_output_mode($idealo_restore['output_mode'] ?? 'ebay_only');
        $idealo_strategy_restore = method_exists($this, 'idealo_sanitize_link_strategy')
            ? $this->idealo_sanitize_link_strategy($idealo_restore['link_strategy'] ?? 'hybrid')
            : sanitize_key((string)($idealo_restore['link_strategy'] ?? 'hybrid'));
        if (!empty($idealo_restore['enabled'])
            && in_array($idealo_mode_restore, array('separate','combined','automatic'), true)
            && $idealo_strategy_restore === 'hybrid') {
            $idealo_restore['link_strategy'] = 'products';
            update_option(self::OPTION_NETWORK_IDEALO, $idealo_restore, false);
        }

        $state = $this->aff043_state();
        $status = sanitize_key((string)($state['status'] ?? 'not_started'));
"""
if needle not in s:
    raise SystemExit("restore anchor not found")
s=s.replace(needle,insert,1)
p.write_text(s)
r=Path("/tmp/candidate134/affiliate-portal-router/readme.txt")
rs=r.read_text().replace("V6.72.132 ","V6.72.134 ",1)
r.write_text(rs)
