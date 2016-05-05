<?php
        $servername = 'localhost';
        $dbuser = 'root';
        $password = 'Biertaart';
        $dbname = 'tracking';
        echo '<script>console.log("Connection.php word uitgevoerd")</script>';
        $conn = new mysqli($servername, $username, $password);
                if ($conn->connect_error) {
                    die("Connection failed: " . $conn->connect_error);
                } 
                $sql = "CREATE DATABASE IF NOT EXISTS $dbname";
                if ($conn->query($sql) === TRUE) {
                    echo "Database created successfully";
                    $sql = "CREATE TABLE people (
                    ID INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY, 
                    Name VARCHAR(30) NOT NULL,
                    Macadress VARCHAR(30) NOT NULL,
		    Locationx DOUBLE,
		    Locationy DOUBLE,
		    Locationz DOUBLE,
		    lastseentime DATETIME


                    )";
                     
                } else {
                    echo "Error creating database: " . $conn->error;
                }
 
 
        //mysql_select_db($db);
?>
