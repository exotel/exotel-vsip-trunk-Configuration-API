<?php

/**
 * Get the base URL for Exotel API calls
 */
function exotel_base() {
    $auth_key = getenv('EXO_AUTH_KEY');
    $auth_token = getenv('EXO_AUTH_TOKEN');
    $domain = getenv('EXO_SUBSCRIBIX_DOMAIN');
    $account_sid = getenv('EXO_ACCOUNT_SID');
    
    if (!$auth_key || !$auth_token || !$domain || !$account_sid) {
        echo "Error: Missing required environment variables (EXO_AUTH_KEY, EXO_AUTH_TOKEN, EXO_SUBSCRIBIX_DOMAIN, EXO_ACCOUNT_SID)\n";
        exit(1);
    }
    
    return sprintf('https://%s:%s@%s/v2/accounts/%s',
        $auth_key, $auth_token, $domain, $account_sid);
}

/**
 * Make a POST request to the Exotel API
 */
function exo_post($path, $payload) {
    $ch = curl_init(exotel_base() . $path);
    
    curl_setopt($ch, CURLOPT_CUSTOMREQUEST, 'POST');
    curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($payload));
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, ['Content-Type: application/json']);
    curl_setopt($ch, CURLOPT_FAILONERROR, false);
    
    $resp = curl_exec($ch);
    $http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    
    if ($resp === false) {
        echo "cURL Error: " . curl_error($ch) . "\n";
        curl_close($ch);
        exit(1);
    }
    
    curl_close($ch);
    
    if ($http_code >= 400) {
        echo "HTTP Error $http_code: $resp\n";
        exit(1);
    }
    
    echo $resp . "\n";
    return json_decode($resp, true);
}

function exo_request($method, $path, $query = null, $payload = null) {
    $url = exotel_base() . $path;
    if ($query && count($query) > 0) {
        $url .= '?' . http_build_query(array_filter($query, function ($v) {
            return $v !== null && $v !== '';
        }));
    }
    $ch = curl_init($url);
    curl_setopt($ch, CURLOPT_CUSTOMREQUEST, $method);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_FAILONERROR, false);
    $headers = [];
    if ($payload !== null) {
        $body = json_encode($payload);
        curl_setopt($ch, CURLOPT_POSTFIELDS, $body);
        $headers[] = 'Content-Type: application/json';
    }
    if ($headers) {
        curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
    }
    $resp = curl_exec($ch);
    $http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    if ($resp === false) {
        echo "cURL Error: " . curl_error($ch) . "\n";
        curl_close($ch);
        exit(1);
    }
    curl_close($ch);
    if ($http_code >= 400) {
        echo "HTTP Error $http_code: $resp\n";
        exit(1);
    }
    echo $resp . "\n";
    return json_decode($resp, true);
}

function exo_get($path, $query = null) {
    return exo_request('GET', $path, $query, null);
}

function exo_put($path, $payload) {
    return exo_request('PUT', $path, null, $payload);
}

function exo_delete($path, $query) {
    return exo_request('DELETE', $path, $query, null);
}
