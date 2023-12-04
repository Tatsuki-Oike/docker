<?php

$dsn = 'mysql:host=mysql';
$user = 'sample_user';
$password = 'sample_password';

try {
    $dbh = new PDO($dsn, $user, $password);
    echo "SUCCESS\n";
} catch (PDOException $e) {
    echo "FAIL: " . $e->getMessage() . "\n";
    exit();
}
?>