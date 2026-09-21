<?php
$termId=(int)get_option('pste_e2e_heutaschen_term_id',0);
if($termId<=0)throw new RuntimeException('TERM_ID_MISSING');
$settings=PSTE_Plugin::settings();
$job=PSTE_Research_Job::start($termId,'Heutaschen',$settings);
update_option('pste_e2e_single_job_uuid',(string)$job['job_uuid'],false);
$driver=PSTE_Research_Driver::kick(0,'E2E_MANUAL_SINGLE');
echo wp_json_encode(['job'=>$job,'driver'=>$driver],JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES)."\n";
