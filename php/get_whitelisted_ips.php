#!/usr/bin/env php
<?php

require_once '_client.php';

// Get whitelisted IPs for a trunk
$trunk_sid = getenv('TRUNK_SID');
if (!$trunk_sid) {
    echo "Error: TRUNK_SID environment variable is required\n";
    exit(1);
}

echo "Getting whitelisted IPs for trunk $trunk_sid...\n";
$result = exo_get("/trunks/$trunk_sid/whitelisted-ips");
echo "Whitelisted IPs retrieved successfully!\n";
?> 