<?php

	echo "<h1> Create A User</h1> ";
	echo "<form action='create.php' method='post'>";
	echo "Name<input type='text' name='inputName' value='' /> <br />";
	echo "Macadress<input type='text' name='inputMacadress' value='' />";
	echo "<br />";
	echo "<input type='submit' name='submit' />";
	echo "</form>";

	$servername = 'localhost';
	$dbuser = 'root';
	$password = 'Biertaart';
	$dbname = 'tracking';
	$conn = new mysqli($servername, $dbuser, $password,$dbname);
	if ($conn->connect_error) {
    		die("Connection failed: " . $conn->connect_error);
	}

	$query = "SELECT * FROM Users";
	$result = $conn->query($query);

	while($person = mysqli_fetch_array($result)) {
		echo "<h3h>" . $person['Username'] . "</h3h>";
		echo "<p>" . $person['MacHash'] . "</p>";

	}
?>
