<?php
include 'trackeddevice.php';
include '../checkDB.php';
$servername        = 'localhost';
$dbuser            = 'root';
$password          = 'Biertaart';
$dbname            = 'tracking';
$conn              = new mysqli($servername, $dbuser, $password, $dbname);
$trackeddevicelist = array();
if ($conn->connect_error) {
	die("Connection failed: " . $conn->connect_error);
}

$query  = "SELECT * FROM Users INNER JOIN Locations ON Users.ID=Locations.Users_ID WHERE Locations.Time > DATE_SUB(NOW(),INTERVAL 20 DAY)";
$result = $conn->query($query);
while ($person = mysqli_fetch_array($result)) {
	$trackeddevice = new trackeddevice($person['ID'], $person['Username'], $person['X'], $person['Y'], $person['Z'], $person['Time']);
	array_push($trackeddevicelist,$trackeddevice);
}

$encodedObj = json_encode($trackeddevicelist);
echo $encodedObj;
$conn->close();
