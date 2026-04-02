#!/usr/bin/env php
<?php
require '_client.php';
$trunk = getenv('TRUNK_SID');
$pass = getenv('SIP_CRED_PASSWORD');
if (!$trunk || !$pass) {
    echo "Error: TRUNK_SID and SIP_CRED_PASSWORD required\n";
    exit(1);
}
$body = [
    'user_name' => getenv('SIP_CRED_USERNAME') ?: 'voice_ai_user',
    'password' => $pass,
    'friendly_name' => getenv('SIP_CRED_FRIENDLY_NAME') ?: 'streamkit',
];
echo "Creating SIP credentials...\n";
exo_post("/trunks/$trunk/credentials", $body);
