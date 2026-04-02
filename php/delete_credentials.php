#!/usr/bin/env php
<?php
require '_client.php';
$trunk = getenv('TRUNK_SID');
$cid = getenv('CREDENTIAL_ID');
if (!$trunk || !$cid) {
    echo "Error: TRUNK_SID and CREDENTIAL_ID required\n";
    exit(1);
}
echo "Deleting credential...\n";
exo_delete("/trunks/$trunk/credentials", ['id' => $cid]);
