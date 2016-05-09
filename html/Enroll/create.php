<?php
	include '../checkDB.php';
	$servername = 'localhost';
	$dbuser = 'root';
	$password = 'Biertaart';
	$dbname = 'tracking';
	$dbport = 3306;

	$conn = new mysqli($servername, $dbuser, $password,$dbname);
	if ($conn->connect_error) {
		die("Connection failed: " . $conn->connect_error);
	}
	$Name = $_POST['inputName'];
	$Macadress = $_POST['inputMacadress'];

	if(!$_POST['submit'])	{
		echo "please fill in these forms so you can use indoor location tracking";
	} else {
		$query = "INSERT INTO Users (Username, MacHash) VALUES('" . $Name . "', '" . hash("sha512",$Macadress) . "')";
		if (!mysqli_query ($conn,$query)){
			echo("Error description: " . mysqli_error($conn));
		}
		else{
			echo "user has been added";
		}
	}
	mysqli_close($conn);
?>
