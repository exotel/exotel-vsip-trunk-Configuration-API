#!/usr/bin/env php
<?php
require '_client.php';
$ex = getenv('EXOPHONE') ?: getenv('DID_NUMBER');
if (!$ex) {
    echo "Error: set EXOPHONE or DID_NUMBER\n";
    exit(1);
}
$q = ['exophone' => $ex];
if (getenv('TRUNK_SID')) {
    $q['trunk_sid'] = getenv('TRUNK_SID');
}
echo "Trunk map lookup...\n";
exo_get('/trunk-maps', $q);
