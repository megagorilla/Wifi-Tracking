<?php
	$servername        = 'localhost';
	$dbuser            = 'root';
	$password          = 'Biertaart';
	$dbname            = 'tracking';
	$conn              = new mysqli($servername, $dbuser, $password, $dbname);
	$trackeddevicelist = array();
	if ($conn->connect_error) {
		die("Connection failed: " . $conn->connect_error);
	}

	$query = file_get_contents("../SQL/createUsers.sql");
	$result = $conn->query($query);

	$query = file_get_contents("../SQL/createSniffers.sql");
	$result = $conn->query($query);

	$query = file_get_contents("../SQL/createLocations.sql");
	$result = $conn->query($query);

	$query = file_get_contents("../SQL/createRanges.sql");
	$result = $conn->query($query);

	$conn->close();
?> 
