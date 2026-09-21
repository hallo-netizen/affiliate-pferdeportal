<?php
$out=['driver'=>PSTE_Research_Driver::status(),'job'=>PSTE_Research_Job::peek(),'queue'=>PSTE_Breadth_Research_Queue::peek(),'provider_counts'=>get_option('pste_e2e_provider_counts',[])];
echo wp_json_encode($out,JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES)."\n";
