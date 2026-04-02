#!/usr/bin/env php
<?php
require '_client.php';
$trunk = getenv('TRUNK_SID');
if (!$trunk) {
    echo "Error: TRUNK_SID required\n";
    exit(1);
}
$q = [];
if (getenv('PAGE_SIZE')) {
    $q['page_size'] = getenv('PAGE_SIZE');
}
if (getenv('PAGE_OFFSET')) {
    $q['offset'] = getenv('PAGE_OFFSET');
}
if (getenv('CREDENTIAL_ID')) {
    $q['id'] = getenv('CREDENTIAL_ID');
}
echo "Listing credentials...\n";
exo_get("/trunks/$trunk/credentials", $q ?: null);
