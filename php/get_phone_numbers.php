#!/usr/bin/env php
<?php

require_once '_client.php';

// Get phone numbers for a trunk (same endpoint as destination-uris)
$trunk_sid = getenv('TRUNK_SID');
if (!$trunk_sid) {
    echo "Error: TRUNK_SID environment variable is required\n";
    exit(1);
}

echo "Getting phone numbers for trunk $trunk_sid...\n";
$result = exo_get("/trunks/$trunk_sid/destination-uris");
echo "Phone numbers retrieved successfully!\n";
?> 