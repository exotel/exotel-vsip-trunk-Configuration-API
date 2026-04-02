#!/usr/bin/env php
<?php
require '_client.php';
$trunk = getenv('TRUNK_SID');
$cid = getenv('CREDENTIAL_ID');
if (!$trunk || !$cid) {
    echo "Error: TRUNK_SID and CREDENTIAL_ID required\n";
    exit(1);
}
$body = [];
if (getenv('SIP_CRED_FRIENDLY_NAME')) {
    $body['friendly_name'] = getenv('SIP_CRED_FRIENDLY_NAME');
}
if (getenv('SIP_CRED_USERNAME')) {
    $body['user_name'] = getenv('SIP_CRED_USERNAME');
}
if (getenv('SIP_CRED_PASSWORD')) {
    $body['password'] = getenv('SIP_CRED_PASSWORD');
}
if (!$body) {
    $body['friendly_name'] = 'updated_label';
}
echo "Updating credential...\n";
exo_put("/trunks/$trunk/credentials/$cid", $body);
