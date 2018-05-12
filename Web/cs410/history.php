<?php
session_start();
if(isset($_SESSION['login'])&&$_SESSION['login']==1){
    $data = json_encode( getHistory($_SESSION['email']));
    echo($data );
}else{
    echo("plesae login");
}
function connect(){
    $servername = "localhost";
    $username = "root";
    $password = "";
    $dbname = "cs410";

// Create connection
    $conn = new mysqli($servername, $username, $password,$dbname);

// Check connection
    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }
    return $conn;
}
function getHistory($email){
    $conn = connect();
    $stmt = $conn->prepare("select drug , adr from  history where email=? order by timeS desc limit 30");
    $stmt->bind_param("s",  $email);

    if(!$stmt->execute()){
    }

    $result = $stmt->get_result();
    $arr =array();

    while ($row = $result->fetch_assoc()) {
        $arrs=array($row['drug'],$row['adr']);
        array_push($arr,$arrs);
    }



    $stmt->close();
    $conn->close();
    return $arr;
}


?>