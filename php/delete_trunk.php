#!/usr/bin/env php
<?php

require_once '_client.php';

// Delete a trunk
$trunk_sid = getenv('TRUNK_SID');
if (!$trunk_sid) {
    echo "Error: TRUNK_SID environment variable is required\n";
    exit(1);
}

echo "Deleting trunk $trunk_sid...\n";
$result = exo_delete("/trunks?trunk_sid=$trunk_sid");
echo "Trunk deleted successfully!\n";
?> 