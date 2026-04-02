#!/usr/bin/env php
<?php
require '_client.php';
$q = [];
if (getenv('PAGE_SIZE')) {
    $q['page_size'] = getenv('PAGE_SIZE');
}
if (getenv('PAGE_OFFSET')) {
    $q['offset'] = getenv('PAGE_OFFSET');
}
if (getenv('TRUNK_SID')) {
    $q['trunk_sid'] = getenv('TRUNK_SID');
}
echo "Listing trunks...\n";
exo_get('/trunks', $q ?: null);
