<?php
declare(strict_types=1);

function ok(bool $condition, string $name): void {
    if (!$condition) {
        fwrite(STDERR, "FAIL: {$name}\n");
        exit(1);
    }
    echo "PASS: {$name}\n";
}

function relevance_band(int $specificity): int {
    if ($specificity >= 450) return 5;
    if ($specificity >= 400) return 4;
    if ($specificity >= 350) return 3;
    if ($specificity >= 200) return 2;
    return 1;
}

function provider_key(array $campaign): string {
    $network = strtolower((string)($campaign['network'] ?? ''));
    if ($network === 'awin') {
        return ((int)($campaign['advertiser_id'] ?? 0) === 14336) ? 'otto' : 'awin_other';
    }
    if ($network === 'adcell') return 'adcell';
    if ($network === 'digistore24') return 'digistore24';
    if (in_array($network, ['manual','direct'], true)) return 'direct';
    return 'other';
}

function deterministic_bucket(string $week, array $context, string $slot, int $total): int {
    if ($total <= 0) return 0;
    $terms = array_map('intval', (array)($context['term_ids'] ?? []));
    sort($terms, SORT_NUMERIC);
    $slugs = array_map('strval', (array)($context['slugs'] ?? []));
    sort($slugs, SORT_STRING);
    $seed = implode('|', [
        $week,
        (string)((int)($context['post_id'] ?? 0)),
        implode(',', $terms),
        implode(',', $slugs),
        strtolower($slot),
    ]);
    return (int)(hexdec(substr(hash('sha256', $seed), 0, 8)) % $total);
}

function weighted_reorder(array $candidates, array $context, string $slot, array $weights, string $week): array {
    if (count($candidates) < 2) return $candidates;
    usort($candidates, static function(array $a, array $b): int {
        foreach (['specificity','matches','priority'] as $key) {
            $av = (int)($a[$key] ?? 0); $bv = (int)($b[$key] ?? 0);
            if ($av !== $bv) return $av > $bv ? -1 : 1;
        }
        return strcmp((string)($a['campaign']['id'] ?? ''), (string)($b['campaign']['id'] ?? ''));
    });
    $best = relevance_band((int)($candidates[0]['specificity'] ?? 0));
    $groups = [];
    foreach ($candidates as $i=>$candidate) {
        if (relevance_band((int)($candidate['specificity'] ?? 0)) !== $best) continue;
        $campaign = (array)($candidate['campaign'] ?? []);
        if (($campaign['creative_type'] ?? '') !== 'banner') continue;
        $key = provider_key($campaign);
        $weight = max(0, (int)($weights[$key] ?? 0));
        if ($weight <= 0) continue;
        $groups[$key][] = $i;
    }
    $ordered = ['otto','awin_other','adcell','direct','digistore24','other'];
    $eligible=[]; $total=0;
    foreach ($ordered as $key) {
        if (empty($groups[$key])) continue;
        $w=max(0,(int)($weights[$key] ?? 0));
        if ($w<=0) continue;
        $eligible[$key]=$w; $total+=$w;
    }
    if (count($eligible)<2 || $total<=0) return $candidates;
    $bucket=deterministic_bucket($week,$context,$slot,$total);
    $cursor=0; $selected='';
    foreach ($eligible as $key=>$weight) {
        $cursor += $weight;
        if ($bucket < $cursor) { $selected=$key; break; }
    }
    if ($selected==='' || empty($groups[$selected])) return $candidates;
    $selectedIndexes=array_fill_keys($groups[$selected], true);
    $out=[];
    foreach ($groups[$selected] as $i) $out[]=$candidates[$i];
    foreach ($candidates as $i=>$candidate) if (!isset($selectedIndexes[$i])) $out[]=$candidate;
    return array_values($out);
}

function repair_selection(array $assignment, ?array $automatic): ?array {
    $mode = strtolower((string)($assignment['banner_mode'] ?? 'automatic'));
    if ($mode === 'none') return null;
    if ($mode === 'fixed') return (array)($assignment['fixed'] ?? []);
    return $automatic;
}

$weights=['otto'=>40,'awin_other'=>25,'adcell'=>20,'direct'=>15,'digistore24'=>0,'other'=>0];
$context=['post_id'=>101,'term_ids'=>[8,3],'slugs'=>['decken','pferd']];
$otto=['id'=>'otto','creative_type'=>'banner','network'=>'awin','advertiser_id'=>14336];
$awin=['id'=>'awin','creative_type'=>'banner','network'=>'awin','advertiser_id'=>999];
$adcell=['id'=>'adcell','creative_type'=>'banner','network'=>'adcell'];
$ds24=['id'=>'ds24','creative_type'=>'banner','network'=>'digistore24'];

$highAwin=['campaign'=>$awin,'specificity'=>500,'matches'=>1,'priority'=>10];
$lowOtto=['campaign'=>$otto,'specificity'=>350,'matches'=>5,'priority'=>999];
$r=weighted_reorder([$lowOtto,$highAwin],$context,'post_inline_banner',$weights,'2026-37');
ok(($r[0]['campaign']['id'] ?? '')==='awin','relevance outranks OTTO share');

$equal=[
 ['campaign'=>$otto,'specificity'=>450,'matches'=>1,'priority'=>10],
 ['campaign'=>$awin,'specificity'=>450,'matches'=>1,'priority'=>10],
 ['campaign'=>$adcell,'specificity'=>450,'matches'=>1,'priority'=>10],
];
$r1=weighted_reorder($equal,$context,'post_inline_banner',$weights,'2026-37');
$r2=weighted_reorder($equal,$context,'post_inline_banner',$weights,'2026-37');
ok(($r1[0]['campaign']['id'] ?? '')===($r2[0]['campaign']['id'] ?? ''),'same week/context/slot is deterministic');

$onlyOttoAdcell=[
 ['campaign'=>$otto,'specificity'=>450,'matches'=>1,'priority'=>10],
 ['campaign'=>$adcell,'specificity'=>450,'matches'=>1,'priority'=>10],
];
$r=weighted_reorder($onlyOttoAdcell,$context,'post_inline_banner',$weights,'2026-37');
ok(in_array(($r[0]['campaign']['id'] ?? ''),['otto','adcell'],true),'missing sources renormalize to eligible providers');

$withDs24=[
 ['campaign'=>$ds24,'specificity'=>450,'matches'=>9,'priority'=>999],
 ['campaign'=>$otto,'specificity'=>450,'matches'=>1,'priority'=>1],
 ['campaign'=>$awin,'specificity'=>450,'matches'=>1,'priority'=>1],
];
$r=weighted_reorder($withDs24,$context,'post_inline_banner',$weights,'2026-37');
ok(($r[0]['campaign']['id'] ?? '')!=='ds24','zero-share Digistore24 cannot win quota selection');

$automatic=['campaign'=>$otto];
$fixed=['campaign'=>$adcell];
ok((repair_selection(['banner_mode'=>'fixed','fixed'=>$fixed],$automatic)['campaign']['id'] ?? '')==='adcell','manual fixed repair overrides automation');
ok(repair_selection(['banner_mode'=>'none'],$automatic)===null,'manual none repair suppresses banner');
ok((repair_selection(['banner_mode'=>'automatic'],$automatic)['campaign']['id'] ?? '')==='otto','return to automatic restores engine');

ok(provider_key($otto)==='otto','Awin advertiser 14336 maps to OTTO');
$spoof=$otto; $spoof['advertiser_id']=999; $spoof['name']='OTTO';
ok(provider_key($spoof)==='awin_other','name cannot spoof OTTO identity');

$zeroOnly=[
 ['campaign'=>$ds24,'specificity'=>500,'matches'=>9,'priority'=>999],
];
$positiveOnly=[
 ['campaign'=>$otto,'specificity'=>350,'matches'=>1,'priority'=>1],
];
function auto_weight_filter(array $candidates, array $weights): array {
    return array_values(array_filter($candidates, static function(array $candidate) use ($weights): bool {
        $campaign=(array)($candidate['campaign'] ?? []);
        return (($campaign['creative_type'] ?? '') === 'banner')
            && ((int)($weights[provider_key($campaign)] ?? 0) > 0);
    }));
}
ok(auto_weight_filter($zeroOnly,$weights)===[],'zero-share source is excluded from automatic banner delivery');
ok(count(auto_weight_filter($positiveOnly,$weights))===1,'positive-share banner remains automatically eligible');

function normalize_real_awin_creatives(array $rows, int $advertiserId): array {
    $out=[]; $blocked=0;
    foreach ($rows as $row) {
        if (!is_array($row)) { $blocked++; continue; }
        if ((int)($row['advertiser_id'] ?? $row['merchant_id'] ?? 0) !== $advertiserId) { $blocked++; continue; }
        $id=trim((string)($row['creative_id'] ?? $row['id'] ?? $row['banner_id'] ?? ''));
        $title=trim((string)($row['title'] ?? $row['name'] ?? ''));
        $image=trim((string)($row['image_url'] ?? $row['image_source'] ?? $row['banner_url'] ?? ''));
        $tracking=trim((string)($row['tracking_url'] ?? $row['affiliate_url'] ?? $row['click_url'] ?? ''));
        if ($id==='' || $title==='' || $image==='' || $tracking==='') { $blocked++; continue; }
        $out[]=['creative_id'=>$id,'creative_type'=>'banner','advertiser_id'=>$advertiserId];
    }
    return ['rows'=>$out,'blocked'=>$blocked];
}
$real=normalize_real_awin_creatives([
 ['advertiser_id'=>14336,'creative_id'=>'b1','title'=>'OTTO Pferd','image_url'=>'https://img.invalid/b1.jpg','tracking_url'=>'https://trk.invalid/b1'],
],14336);
ok(count($real['rows'])===1 && $real['blocked']===0,'real OTTO/Awin banner row passes strict source contract');
$wrong=normalize_real_awin_creatives([
 ['advertiser_id'=>999,'creative_id'=>'b1','title'=>'Spoof','image_url'=>'https://img.invalid/b1.jpg','tracking_url'=>'https://trk.invalid/b1'],
],14336);
ok(count($wrong['rows'])===0 && $wrong['blocked']===1,'foreign advertiser banner is blocked');
$incomplete=normalize_real_awin_creatives([
 ['advertiser_id'=>14336,'creative_id'=>'b1','title'=>'No tracking','image_url'=>'https://img.invalid/b1.jpg'],
],14336);
ok(count($incomplete['rows'])===0 && $incomplete['blocked']===1,'incomplete real banner row is blocked');

echo "ALL WEIGHTED BANNER BEHAVIOR TESTS PASS\n";
