#!/usr/bin/env php
<?php

require_once '_client.php';

// Get destination URIs for a trunk
$trunk_sid = getenv('TRUNK_SID');
if (!$trunk_sid) {
    echo "Error: TRUNK_SID environment variable is required\n";
    exit(1);
}

echo "Getting destination URIs for trunk $trunk_sid...\n";
$result = exo_get("/trunks/$trunk_sid/destination-uris");
echo "Destination URIs retrieved successfully!\n";
?> 